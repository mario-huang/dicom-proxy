from typing import Iterator, Tuple
from pydicom.dataset import Dataset
from pynetdicom import AE

def findScu(ds: Dataset, query_model: str) -> Iterator[Tuple[int, Dataset | None]]:
    ae_scu = AE()
    # Add the requested presentation context
    ae_scu.add_requested_context(query_model)
    # Connect to the SCP server, port number 4242 (according to actual SCP configuration)
    assoc = ae_scu.associate("192.168.3.100", 4242)

    if assoc.is_established:
        print("C-FIND Connection to upstream server established.")
        # Send C-FIND request and receive responses
        responses = assoc.send_c_find(ds, query_model)
        # 将上级服务器返回的每个响应发送回客户端
        for status, identifier in responses:
            if status and status.Status in (0xFF00, 0xFF01):  # Pending 状态
                yield status.Status, identifier
            elif status.Status == 0x0000:  # 完成
                yield 0x0000, None
        assoc.release()
    else:
        # 如果连接上级服务器失败，返回失败状态
        yield 0xA700, None  # Status code 0xA700 表示操作失败
