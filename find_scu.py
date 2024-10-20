from pydicom.dataset import Dataset
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from share import ae

def findScu() -> None:
    # 创建 C-FIND 请求的数据集
    ds = Dataset()
    ds.PatientName = "*"  # 使用通配符查找所有患者
    ds.QueryRetrieveLevel = "PATIENT"  # 查询级别：PATIENT

    # 连接到 SCP 服务器，端口号为 11112（根据 SCP 实际配置）
    assoc = ae.associate("127.0.0.1", 11112)

    if assoc.is_established:
        # 发送 C-FIND 请求并接收响应
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)

    # 处理接收到的响应
    for status, identifier in responses:
        if status:
            if status.Status in (0xFF00, 0xFF01):  # Pending 状态，表示有响应结果
                print(f"Response received:\n{identifier}")
            elif status.Status == 0x0000:  # Success 状态
                print("C-FIND query completed successfully.")
        else:
            print("Connection failed or no response from SCP.")

        # 释放连接
        assoc.release()
    else:
        print("Failed to establish association with SCP.")
