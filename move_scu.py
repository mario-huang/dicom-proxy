from typing import Iterator, Tuple
from pydicom.dataset import Dataset
from pynetdicom import AE

def moveScu(ds: Dataset, query_model: str, destination_aet: str) -> Iterator[Tuple[Dataset, Dataset | None]]:
    ae_scu = AE()

    # Add the requested presentation context for C-MOVE
    ae_scu.add_requested_context(query_model)

    # Connect to the upstream SCP server, port number 4242 (adjust according to your SCP configuration)
    assoc = ae_scu.associate("192.168.3.100", 4242)

    if assoc.is_established:
        print(f"Connection to upstream server established for C-MOVE to {destination_aet}.")

        # Send C-MOVE request and receive responses
        responses = assoc.send_c_move(ds, destination_aet, query_model)

        # Yield each response from the upstream server
        for status, identifier in responses:
            yield status, identifier

        # Release the association
        assoc.release()
    else:
        print("Failed to establish association with upstream SCP for C-MOVE.")
        # Return failure status
        yield Dataset(), None
