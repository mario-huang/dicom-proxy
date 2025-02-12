from pynetdicom.sop_class import Verification
from echo_scu import echo_scu
from scu_event import SCUEvent
from share import ae_scp

ae_scp.add_supported_context(Verification)

# Implement a handler for evt.EVT_C_ECHO
def handle_echo(event):
    client_aet = event.assoc.requestor.ae_title
    print(f"handle_echo, client_aet: {client_aet}")
    
    scu_event = SCUEvent()
    scu_event.client_aet = client_aet
    return echo_scu(scu_event)