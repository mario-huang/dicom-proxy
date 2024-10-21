import asyncio
import threading
from pydicom import dcmread
from move_scu import moveScu
from share import ae_scp,store_status_queue, total_images_queue
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove, StudyRootQueryRetrieveInformationModelMove,CTImageStorage, MRImageStorage
from pynetdicom import StoragePresentationContexts

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelMove)

# Define a callback function to handle C-MOVE requests
def handle_move(event):
    ds = event.identifier
    move_destination = event.move_destination  # 客户端的 AE Title

    # print(f"Received C-MOVE request with dataset: {ds} to {move_destination}")

    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    query_model = ""
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelMove
    elif query_level == "STUDY":
        query_model = StudyRootQueryRetrieveInformationModelMove
    elif query_level == "SERIES":
        query_model = ""
    elif query_level == "IMAGE":
        query_model = ""

    # Call moveScu function to send the request to the upstream server
    move_scu_thread = threading.Thread(target=moveScu, args=(ds, query_model))
    move_scu_thread.start()
    # matching = [dcmread("1.3.46.670589.33.1.63860889761311629200001.5332995544705962259"), dcmread("1.3.46.670589.33.1.63860889761291576400001.5476309447054557379")]
    
    # 返回目标 AE 的地址、端口和 presentation contexts
    yield ("192.168.3.222", 6000, {"contexts": StoragePresentationContexts})

    # Yield the total number of C-STORE sub-operations required
    total_images = total_images_queue.get()
    print("total_images", total_images)
    yield total_images

    while True:
        item = store_status_queue.get()  # 等待handle_store处理结果
        # print(f"store_status_queue: ")
        if item is None:
            print("All images have been sent.")
            yield (0x0000, None)
        # Pending
        yield (0xFF00, item)
        
