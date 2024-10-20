from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from share import ae_scu
from pydicom.dataset import Dataset

# Add the requested presentation context
ae_scu.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

def findScu(ds: Dataset):
    # 连接到 SCP 服务器，端口号为 4242（根据 SCP 实际配置）
    assoc = ae_scu.associate("192.168.3.100", 4242)

    if assoc.is_established:
        print("Connection to upstream server established.")

        # 发送 C-FIND 请求并接收响应
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)

        # 逐个返回上级服务器的响应
        for status, identifier in responses:
            if status.Status in (0xFF00, 0xFF01):  # Pending 状态，表示有响应结果
                print(f"Upstream response received: {identifier}")
            elif status.Status == 0x0000:  # Success 状态
                print("Upstream C-FIND query completed successfully.")
            yield status, identifier

        # 释放连接
        assoc.release()
    else:
        print("Failed to establish association with upstream SCP.")
        # 返回操作失败状态
        yield Dataset(), None
