from find_scu import find_scu
from scu_event import SCUEvent
from share import ae_scp
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelFind,
    CompositeInstanceRootRetrieveGet,
)

# Add the supported presentation context
ae_scp.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(StudyRootQueryRetrieveInformationModelFind)
ae_scp.add_supported_context(CompositeInstanceRootRetrieveGet)


# Implement the handler for evt.EVT_C_FIND
def handle_find(event):
    client_aet = event.assoc.requestor.ae_title
    print(f"handle_find, client_aet: {client_aet}")
    ds = event.identifier
    if "QueryRetrieveLevel" not in ds:
        # Failure
        yield (0xC000, None)
        return
    # print(f"Received C-FIND request with dataset: {ds}")
    # Query/Retrieve Level
    query_level = ds.QueryRetrieveLevel
    if query_level == "PATIENT":
        query_model = PatientRootQueryRetrieveInformationModelFind
    elif query_level in ["STUDY", "SERIES"]:
        query_model = StudyRootQueryRetrieveInformationModelFind
    elif query_level == "IMAGE":
        query_model = CompositeInstanceRootRetrieveGet

    # Call find_scu function to send the request to the upstream server
    scu_event = SCUEvent()
    scu_event.identifier = ds
    scu_event.query_model = query_model
    scu_event.client_aet = client_aet
    responses = find_scu(scu_event)
    for status, identifier in responses:
        if event.is_cancelled:
            scu_event.is_cancelled = True
            yield (0xFE00, None)
            return
        if status == 0x0000:
            # No more results, return success status
            print("C-FIND success")
        yield status, identifier
