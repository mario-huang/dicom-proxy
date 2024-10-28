from pynetdicom import AE, evt
from pynetdicom.sop_class import Verification
from share import ae_scp

ae_scp.add_supported_context(Verification)

# Implement a handler for evt.EVT_C_ECHO
def handle_echo(event):
    return 0x0000