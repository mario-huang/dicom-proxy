from find_scu import findScu
from share import ae
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

# Add the supported presentation context
ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

# 定义一个处理 C-FIND 请求的回调函数
def handle_find(event):
    print(event)
    ds = event.identifier
    print(ds)
    # 创建一个数据集作为响应
    response = findScu(ds)

    # 返回找到的结果数据集
    yield 0xFF00, response  # 0xFF00 表示还有更多结果

    # 没有更多结果了，返回成功状态
    yield 0x0000, None


