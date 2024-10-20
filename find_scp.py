from find_scu import findScu
from share import ae_scp
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

# 定义一个处理 C-FIND 请求的回调函数
def handle_find(event):
    ds = event.identifier
    print(f"Received C-FIND request with dataset: {ds}")

    # 调用 findScu 函数将请求发送到上级服务器
    for status, response in findScu(ds):
        if status.Status in (0xFF00, 0xFF01):  # Pending 状态
            print(f"Forwarding response: {response}")
            yield status.Status, response

    # 没有更多结果了，返回成功状态
    yield 0x0000, None
