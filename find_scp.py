from find_scu import findScu
from scu_event import SCUEvent
from share import ae_scp
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelFind,
    CompositeInstanceRootRetrieveGet
)

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(CompositeInstanceRootRetrieveGet)

# Implement the handler for evt.EVT_C_FIND
def handle_find(event):
    ds = event.identifier
    if "QueryRetrieveLevel" not in ds:
        # Failure
        yield 0xC000, None
        return
    # print(f"Received C-FIND request with dataset: {ds}")
    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    query_model = ""
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelFind
    elif query_level in ["STUDY", "SERIES"]:
        query_model = StudyRootQueryRetrieveInformationModelFind
    elif query_level == "IMAGE":
        query_model = CompositeInstanceRootRetrieveGet

    # Call findScu function to send the request to the upstream server
    scu_event = SCUEvent()
    scu_event.identifier = ds
    scu_event.query_model = query_model
    responses = findScu(scu_event)
    for status, identifier in responses:
        if event.is_cancelled:
             scu_event.is_cancelled = True
             yield (0xFE00, None)
             return
        yield status, identifier
