import threading
from move_scu import moveScu
from share import ae_scp, store_status_queue, total_images_queue, config
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
        yield 0xC000, None
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
        query_model = "CompositeInstanceRootRetrieveMove"

    # Call moveScu function to send the request to the upstream server
    move_scu_thread = threading.Thread(target=moveScu, args=(ds, query_model))
    move_scu_thread.start()    

    # Yield the total number of C-STORE sub-operations required
    total_images = total_images_queue.get()
    print("total_images", total_images)
    yield total_images

    # Yield the matching instances
    while True:
        item = store_status_queue.get()
        # print(f"store_status_queue: ")
        if item is None:
            print("All images have been sent.")
            yield (0x0000, None)
        # Pending
        yield (0xFF00, item)
