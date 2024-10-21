from typing import Iterator, Tuple
from pydicom.dataset import Dataset
from pynetdicom import AE

def moveScu(ds: Dataset, query_model: str) -> Iterator[Tuple[int, Dataset | None]]:
    ae_scu = AE()
    # Add the requested presentation context for C-MOVE
    ae_scu.add_requested_context(query_model)
    # Connect to the upstream SCP server, port number 4242
    assoc = ae_scu.associate("192.168.3.100", 4242)

    if assoc.is_established:
        print("C-MOVE Connection to upstream server established.")
        # Send C-MOVE request and receive responses
        responses = assoc.send_c_move(ds, "DicomProxy", query_model)
        for status, identifier in responses:
            if status:
                if status.Status in (0xFF00, 0xFF01):
                    # Pending status
                    print(f"Forwarding response: {identifier}")
                    yield status.Status, identifier
                elif status.Status == 0x0000:
                    # No more results, return success status
                    yield 0x0000, None
            else:
                print('Connection timed out, was aborted or received invalid response')
                yield 0xA700, None
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')
        yield 0xA700, None  # Status code 0xA700 表示操作失败
