from pydicom import Dataset
from pynetdicom import AE, StoragePresentationContexts

def storeScu(ds: Dataset, addr: str, port: int) -> None:
    """将接收到的图像通过 C-STORE 发送给客户端"""
    ae_scu = AE()
    # 添加 Storage SCP 支持的 Presentation Context
    ae_scu.requested_contexts = StoragePresentationContexts

    # 与目标客户端建立关联
    assoc = ae_scu.associate(addr, port)
    if assoc.is_established:
        print(f"Connection established with {addr} for C-STORE.")
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds)
        # Check the status of the storage request
        if status:
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')