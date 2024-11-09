from typing import Iterator, Tuple
from pydicom.dataset import Dataset

from pynetdicom import AE, build_role
from scu_event import SCUEvent
from share import config
from pynetdicom import debug_logger, evt
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    CTImageStorage
)

from store_scp import handle_store

handlers = [(evt.EVT_C_STORE, handle_store)]

def get_scu(scu_event: SCUEvent) -> Iterator[Tuple[int, Dataset | None]]:
    ae_scu = AE(scu_event.client_aet)
    ae_scu.add_requested_context(CTImageStorage)
    # Add the requested presentation contexts (QR SCU)
    ae_scu.add_requested_context(scu_event.query_model)
    # Create an SCP/SCU Role Selection Negotiation item for CT Image Storage
    role = build_role(CTImageStorage, scp_role=True)
    # Connect to the SCP server
    assoc = ae_scu.associate(config.server.address, config.server.port, ext_neg=[role], evt_handlers=handlers)

    if assoc.is_established:
        # Use the C-GET service to send the identifier
        responses = assoc.send_c_get(scu_event.identifier, scu_event.query_model)
        for status, identifier in responses:
            if status:
                print("C-GET query status: 0x{0:04x}".format(status.Status))
            else:
                print("Connection timed out, was aborted or received invalid response")

        # Release the association
        assoc.release()
    else:
        print("Association rejected, aborted or never connected")
