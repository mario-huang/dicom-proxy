from queue import Queue
import threading
from get_scu import get_scu
from scu_event import SCUEvent
from share import ae_scp, config, store_queue_dict, total_images_queue_dict
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    StudyRootQueryRetrieveInformationModelGet,
    CompositeInstanceRootRetrieveGet,
)


# Add a supported presentation context (QR Get SCP)
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelGet)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelGet)
ae_scp.add_supported_context(CompositeInstanceRootRetrieveGet)

# Implement the handler for evt.EVT_C_GET
def handle_get(event):
    client_aet = event.assoc.requestor.ae_title
    store_queue_dict[client_aet] = Queue()
    total_images_queue_dict[client_aet] = Queue()
    print(f"handle_get, client_aet: {client_aet}")

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
    
    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelGet
    elif query_level in ["STUDY", "SERIES"]:
        query_model = StudyRootQueryRetrieveInformationModelGet
    elif query_level == "IMAGE":
        query_model = CompositeInstanceRootRetrieveGet

    # Call get_scu function to send the request to the upstream server
    scu_event = SCUEvent()
    scu_event.identifier = ds
    scu_event.query_model = query_model
    scu_event.client_aet = client_aet
    get_scu_thread = threading.Thread(target=get_scu, args=(scu_event,))
    get_scu_thread.start()

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