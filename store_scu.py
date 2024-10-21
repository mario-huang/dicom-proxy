from pydicom import Dataset
from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import CTImageStorage
from share import config

def storeScu(ds: Dataset, addr: str, port: int) -> None:
    """将接收到的图像通过 C-STORE 发送给客户端"""
    ae_scu = AE(config.proxy.aet)
    # 添加 Storage SCP 支持的 Presentation Context
    ae_scu.requested_contexts = StoragePresentationContexts
    # ae_scu.add_requested_context(CTImageStorage)

    # 与目标客户端建立关联
    assoc = ae_scu.associate(addr, port)
    # print(assoc.accepted_contexts)
    if assoc.is_established:
        print(f"Connection established with {addr} for C-STORE.")
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds)
        print("C-STORE response status:", status.Status)

        # Release the association
        assoc.release()
        # return status.State
    else:
        print('Association rejected, aborted or never connected')
        # return 0xA700