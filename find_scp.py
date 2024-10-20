from pydicom.dataset import Dataset
from find_scu import FindScu


# 定义一个处理 C-FIND 请求的回调函数
def handle_find(event):
    ds = event.identifier

    # 创建一个数据集作为响应
    response = Dataset()
    response.PatientName = 'TEST^PATIENT'
    response.PatientID = '123456'
    response.QueryRetrieveLevel = ds.QueryRetrieveLevel

    find_scp = FindScu()

    # 返回找到的结果数据集
    yield 0xFF00, response  # 0xFF00 表示还有更多结果

    # 没有更多结果了，返回成功状态
    yield 0x0000, None


