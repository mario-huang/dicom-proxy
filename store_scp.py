from pydicom.dataset import Dataset
from pynetdicom import AE, evt, StoragePresentationContexts, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove
from share import ae_scp
from store_scu import storeScu

# Add a requested presentation context
ae_scp.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

# Add the Storage SCP's supported presentation contexts
ae_scp.supported_contexts = StoragePresentationContexts

def handle_store(event):
    """处理接收到的 C-STORE 请求"""
    ds = event.dataset

    # 直接将图像发送给客户端
    # 这里假设 move_destination、move_addr 和 move_port 是可用的
    # for status, response in storeScu(ds, "DicomProxy", "192.168.3.119", 4242):
    #     yield status, response

    # 返回成功状态
    return 0x0000
