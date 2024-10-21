from pydicom.dataset import Dataset
from pynetdicom import AE, evt, AllStoragePresentationContexts, debug_logger
from share import ae_scp
from store_scu import storeScu

# Add the Storage SCP's supported presentation contexts
ae_scp.supported_contexts = AllStoragePresentationContexts

def handle_store(event):
    """处理接收到的 C-STORE 请求"""
    ds = event.dataset
    print(f"Received and forwarded image: {ds.SOPInstanceUID}")
    # 直接将图像发送给客户端
    # 这里假设 move_destination、move_addr 和 move_port 是可用的
    storeScu(ds, "127.0.0.1", 4242)
    # for status, identifier in responses:
    #     if status in (0xFF00, 0xFF01):  # Pending 状态
    #         # print(f"Forwarding response: {identifier}")
    #         yield status, identifier
    #     yield status, identifier
    # yield identifier

    # 返回成功状态
    return 0x0000