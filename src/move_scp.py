import threading
from move_scu import moveScu
from scu_event import SCUEvent
from share import ae_scp, config, store_queue, total_images_queue
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
    ds = event.identifier
    move_destination = event.move_destination  # 客户端的 AE Title

    if "QueryRetrieveLevel" not in ds:
        # Failure
        yield (0xC000, None)
        return

    client = config.clients[move_destination]
    if client is None:
        # Unknown destination AE
        yield (None, None)
        return
    # Yield the IP address and listen port of the destination AE
    yield (client.ip, client.port, {"contexts": StoragePresentationContexts})

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
    move_scu_thread = threading.Thread(target=moveScu, args=(scu_event))
    move_scu_thread.start()

    # Yield the total number of C-STORE sub-operations required
    total_images = total_images_queue.get()
    if total_images is None:
        yield (0xA700, None)
        return
    print("total_images", total_images)
    yield total_images

    # Yield the matching instances
    while True:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        status, instance = store_queue.get()
        if status == 0x0000:
            print("All images have been sent.")
            # yield (0x0000, None)
            return
        elif status == 0xFF00:
            yield (0xFF00, None)
            return
        else:
            # Pending
            yield (status, instance)
        