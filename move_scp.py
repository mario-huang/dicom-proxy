from move_scu import moveScu
from share import ae_scp
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove, StudyRootQueryRetrieveInformationModelMove

from store_scu import storeScu

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelMove)

# Define a callback function to handle C-MOVE requests
def handle_move(event):
    ds = event.identifier
    move_destination = event.move_destination  # 客户端的 AE Title

    print(f"Received C-MOVE request with dataset: {ds} to {move_destination}")

    # Query/Retrieve Level
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

    # 向上级发起 C-MOVE 请求
    responses = moveScu(ds, query_model, "DicomProxy")
    for status, identifier in responses:
        if status in (0xFF00, 0xFF01):  # Pending 状态
            # print(f"Forwarding response: {identifier}")
            yield status, identifier

    # C-MOVE 完成后，将收到的图像发给客户端
    # 注意: 此处的 response 是上级返回的图像数据
    # if response:  # 确保有图像返回
    #     for ds in response:  # 假设 response 是一个 Dataset 对象的列表
    #         storeScu(ds, move_destination, "192.168.3.119", 4242)

    # 没有更多结果，返回成功状态
    yield 0x0000, None
