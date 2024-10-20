from typing import Iterator, Tuple
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove, StudyRootQueryRetrieveInformationModelMove, PatientStudyOnlyQueryRetrieveInformationModelMove
from pydicom.dataset import Dataset
from pynetdicom import AE

def moveScu(ds: Dataset) -> Iterator[Tuple[Dataset, Dataset | None]]:
    ae_scu = AE()
    # Add the requested presentation context
    ae_scu.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
    ae_scu.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
    ae_scu.add_requested_context(PatientStudyOnlyQueryRetrieveInformationModelMove)
    # Connect to the SCP server, port number 4242 (according to actual SCP configuration)
    assoc = ae_scu.associate("192.168.3.100", 4242)

    if assoc.is_established:
        print("Connection to upstream server established.")

        # Send C-FIND request and receive responses
        responses = assoc.send_c_move(ds, 'STORE_SCP', PatientRootQueryRetrieveInformationModelMove)

        # Yield each response from the upstream server
        for status, identifier in responses:
            yield status, identifier

        # Release the association
        assoc.release()
    else:
        print("Failed to establish association with upstream SCP.")
        # Return failure status
        yield Dataset(), None
