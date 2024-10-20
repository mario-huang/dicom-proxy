from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage
from typing import Dict
from pydicom.dataset import Dataset

def send_stored_images(ds: Dataset, destination_aet: str, addr: str, port: int) -> None:
    """将接收到的图像通过 C-STORE 发送给客户端"""
    ae_scu = AE()

    # 添加 Storage SCP 支持的 Presentation Context
    ae_scu.add_requested_context(CTImageStorage)

    # 与目标客户端建立关联
    assoc = ae_scu.associate(addr, port)
    if assoc.is_established:
        print(f"Connection established with {destination_aet} for C-STORE.")
        
        # 发送图像
        status = assoc.send_c_store(ds)
        print(f"Sent image {ds.SOPInstanceUID} with status {status}")

        # 释放关联
        assoc.release()
    else:
        print(f"Failed to establish association with {destination_aet}")
