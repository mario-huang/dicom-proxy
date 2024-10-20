from move_scu import moveScu
from share import ae_scp
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove, StudyRootQueryRetrieveInformationModelMove

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelMove)

# Define a callback function to handle C-MOVE requests
def handle_move(event):
    ds = event.identifier
    move_destination = event.move_destination  # Destination AE Title (where to move data)
    print(f"Received C-MOVE request with dataset: {ds} to {move_destination}")

    # Query/Retrieve Level
    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    query_model = ""
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelMove
    elif query_level == "STUDY":
        query_model = StudyRootQueryRetrieveInformationModelMove
    elif query_level == "SERIES":
        query_model = ""
    elif query_level == "IMAGE":
        query_model = ""

    # Call moveScu function to send the request to the upstream server
    for status, response in moveScu(ds, query_model, move_destination):
        if status.Status in (0xFF00, 0xFF01):  # Pending status
            print(f"Forwarding response: {response}")
            yield status.Status, response

    # No more results, return success status
    yield 0x0000, None
