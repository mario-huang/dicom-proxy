from typing import Iterator, Tuple
from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage
from pydicom.dataset import Dataset

def storeScu(ds: Dataset, destination_aet: str, addr: str, port: int) -> Iterator[Tuple[Dataset, Dataset | None]]:
    """将接收到的图像通过 C-STORE 发送给客户端"""
    ae_scu = AE()

    # 添加 Storage SCP 支持的 Presentation Context
    ae_scu.add_requested_context(CTImageStorage)

    # 与目标客户端建立关联
    assoc = ae_scu.associate(addr, port)
    if assoc.is_established:
        print(f"Connection established with {destination_aet} for C-STORE.")
        
        # 发送图像
        responses = assoc.send_c_store(ds)
        # Yield each response from the upstream server
        for status, identifier in responses:
            print(status, identifier)
            yield status, identifier

        # Release the association
        assoc.release()
    else:
        print(f"Failed to establish association with {destination_aet}")
        # Return failure status
        yield Dataset(), None
