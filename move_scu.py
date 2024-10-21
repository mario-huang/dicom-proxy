from typing import Iterator, Tuple
from pydicom.dataset import Dataset
from pynetdicom import AE
from share import store_status_queue, config, total_images_queue

def moveScu(ds: Dataset, query_model: str) -> None:
    ae_scu = AE(config.proxy.aet)
    # Add the requested presentation context for C-MOVE
    ae_scu.add_requested_context(query_model)
    # Connect to the upstream SCP server, port number 4242
    assoc = ae_scu.associate(config.server.ip, config.server.port)

    if assoc.is_established:
        # Send C-MOVE request and receive responses
        responses = assoc.send_c_move(ds, config.proxy.aet, query_model)
        total_images = None  # 仅获取一次影像总数
        for (status, identifier) in responses:
            if status:
                # print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
                # 第一次 Pending 状态
                if status.Status == 0xFF00 and total_images is None:
                    remaining = status.NumberOfRemainingSuboperations
                    completed = status.NumberOfCompletedSuboperations
                    failed = status.NumberOfFailedSuboperations
                    warnings = status.NumberOfWarningSuboperations
                    # 总影像数 = 已完成 + 剩余 + 失败 + 警告
                    total_images = completed + remaining + failed + warnings
                    print(f"Total images to receive: {total_images}")
                    total_images_queue.put(total_images)
                # 判断是否所有影像已经传输完毕
                if status.Status == 0x0000:  # Success 状态码
                    print("All images have been received.")
                    store_status_queue.put(None)
            else:
                print('Connection timed out, was aborted or received invalid response')
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')
        # yield 0xA700, None  # Status code 0xA700 表示操作失败
