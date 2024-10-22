from typing import Iterator, Tuple
from pydicom.dataset import Dataset
from pynetdicom import AE
from scu_event import SCUEvent
from share import config

def findScu(scu_event: SCUEvent) -> Iterator[Tuple[int, Dataset | None]]:
    ae_scu = AE(config.proxy.aet)
    # Add the requested presentation context
    ae_scu.add_requested_context(scu_event.query_model)
    # Connect to the SCP server, port number 4242
    assoc = ae_scu.associate(config.server.ip, config.server.port)

    if assoc.is_established:
        print("C-FIND Connection to upstream server established.")
        # Send C-FIND request and receive responses
        responses = assoc.send_c_find(scu_event.ds, scu_event.query_model)
        for status, identifier in responses:
            if scu_event.is_cancelled:
                assoc.send_c_cancel()
            if status:
                # if status.Status in (0xFF00, 0xFF01):
                #     # Pending status
                #     # print(f"Forwarding response: {identifier}")
                #     yield status.Status, identifier
                # elif status.Status == 0x0000:
                #     # No more results, return success status
                #     print("C-FIND success")
                #     yield 0x0000, None
                yield status.Status, identifier
            else:
                print('Connection timed out, was aborted or received invalid response')
                yield 0xA700, None
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')
        yield 0xA700, None  # Status code 0xA700 表示操作失败
