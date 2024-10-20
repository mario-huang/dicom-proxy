from pydicom.dataset import Dataset
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from share import ae

# Add the supported presentation context
ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

def findScu(ds: Dataset) -> Dataset:
    # 创建 C-FIND 请求的数据集

    # 连接到 SCP 服务器，端口号为 11112（根据 SCP 实际配置）
    assoc = ae.associate("192.168.3.100", 4242)

    if assoc.is_established:
        # 发送 C-FIND 请求并接收响应
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        # 释放连接
        # assoc.release()
        return responses
    # else:
        # 释放连接
        # assoc.release()
