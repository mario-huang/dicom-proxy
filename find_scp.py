from find_scu import findScu
from share import ae_scp
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind, StudyRootQueryRetrieveInformationModelFind, PatientStudyOnlyQueryRetrieveInformationModelFind

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(PatientStudyOnlyQueryRetrieveInformationModelFind)

# Define a callback function to handle C-FIND requests
def handle_find(event):
    ds = event.identifier
    print(f"Received C-FIND request with dataset: {ds}")

    # Call findScu function to send the request to the upstream server
    for status, response in findScu(ds):
        if status.Status in (0xFF00, 0xFF01):  # Pending status
            print(f"Forwarding response: {response}")
            yield status.Status, response

    # No more results, return success status
    yield 0x0000, None
