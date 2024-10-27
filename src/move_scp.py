from queue import Queue
import threading
from move_scu import move_scu
from scu_event import SCUEvent
from share import ae_scp, config, store_queue_dict, total_images_queue_dict
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelMove,
    StudyRootQueryRetrieveInformationModelMove,
    CompositeInstanceRootRetrieveMove,
)
from pynetdicom import StoragePresentationContexts

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelMove)
ae_scp.add_supported_context(CompositeInstanceRootRetrieveMove)


# Implement the evt.EVT_C_MOVE handler
def handle_move(event):
    client_aet = event.move_destination
    store_queue_dict[client_aet] = Queue()
    total_images_queue_dict[client_aet] = Queue()
    print(f"handle_move, move_destination: {client_aet}")

    ds = event.identifier
    if "QueryRetrieveLevel" not in ds:
        # Failure
        yield (0xC000, None)
        return

    client = None
    for c in config.clients:
        if c.aet == client_aet:
            client = c
    if client is None:
        # Unknown destination AE
        yield (None, None)
        return
    # Yield the address and listen port of the destination AE
    yield (client.address, client.port, {"contexts": StoragePresentationContexts})

    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelMove
    elif query_level in ["STUDY", "SERIES"]:
        query_model = StudyRootQueryRetrieveInformationModelMove
    elif query_level == "IMAGE":
        query_model = CompositeInstanceRootRetrieveMove

    # Call moveScu function to send the request to the upstream server
    scu_event = SCUEvent()
    scu_event.identifier = ds
    scu_event.query_model = query_model
    scu_event.client_aet = client_aet
    move_scu_thread = threading.Thread(target=move_scu, args=(scu_event,))
    move_scu_thread.start()

    # Yield the total number of C-STORE sub-operations required
    total_images = total_images_queue_dict[client_aet].get()
    if total_images is None:
        yield (0xA700, None)
        return
    # print("total_images", total_images)
    yield total_images

    # Yield the matching instances
    while True:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        status, instance = store_queue_dict[client_aet].get()
        if status == 0x0000:
            print("All images have been sent.")
            # yield (0x0000, None)
            return
        elif status == 0xA700:
            yield (0xA700, None)
            return
        else:
            # Pending
            yield (status, instance)
        