from pynetdicom import AE
from pynetdicom.sop_class import Verification
from share import config
from scu_event import SCUEvent

def echo_scu(scu_event: SCUEvent):
    ae_scu = AE(scu_event.client_aet) 
    # Add a requested presentation context
    ae_scu.add_requested_context(Verification)
    # Connect to the SCP server
    assoc = ae_scu.associate(config.server.address, config.server.port)

    if assoc.is_established:
        # Use the C-ECHO service to send the request
        # returns the response status a pydicom Dataset
        status = assoc.send_c_echo()

        # Check the status of the verification request
        if status:
            # If the verification request succeeded this will be 0x0000
            print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')