from typing import Iterator, Tuple
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind, StudyRootQueryRetrieveInformationModelFind, PatientStudyOnlyQueryRetrieveInformationModelFind
from pydicom.dataset import Dataset
from pynetdicom import AE

def findScu(ds: Dataset) -> Iterator[Tuple[Dataset, Dataset | None]]:
    ae_scu = AE()
    # Add the requested presentation context
    ae_scu.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
    ae_scu.add_requested_context(StudyRootQueryRetrieveInformationModelFind)
    ae_scu.add_requested_context(PatientStudyOnlyQueryRetrieveInformationModelFind)
    # Connect to the SCP server, port number 4242 (according to actual SCP configuration)
    assoc = ae_scu.associate("192.168.3.100", 4242)

    if assoc.is_established:
        print("Connection to upstream server established.")

        # Send C-FIND request and receive responses
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)

        # Yield each response from the upstream server
        for status, identifier in responses:
            yield status, identifier

        # Release the association
        assoc.release()
    else:
        print("Failed to establish association with upstream SCP.")
        # Return failure status
        yield Dataset(), None
