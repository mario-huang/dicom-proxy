from find_scu import findScu
from share import ae_scp
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind, StudyRootQueryRetrieveInformationModelFind

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelFind)

# Define a callback function to handle C-FIND requests
def handle_find(event):
    ds = event.identifier
    print(f"Received C-FIND request with dataset: {ds}")
    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    query_model = ""
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelFind
    elif query_level == "STUDY":
        query_model = StudyRootQueryRetrieveInformationModelFind
    elif query_level == "SERIES":
        query_model = ""
    elif query_level == "IMAGE":
        query_model = ""

    # Call findScu function to send the request to the upstream server
    for status, response in findScu(ds, query_model):
        if status in (0xFF00, 0xFF01):  # Pending status
            # print(f"Forwarding response: {response}")
            yield status, response

    # No more results, return success status
    yield 0x0000, None
