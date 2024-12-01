from typing import Iterator, Tuple
from pydicom.dataset import Dataset

from pynetdicom import AE, build_role
from scu_event import SCUEvent
from share import config
from pynetdicom import debug_logger, evt
from share import store_queue_dict, config, total_images_queue_dict
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    StudyRootQueryRetrieveInformationModelGet,
    CompositeInstanceRootRetrieveGet,
)


def get_scu(scu_event: SCUEvent) -> None:
    client_aet = scu_event.client_aet
    total_images_queue = total_images_queue_dict[client_aet]
    store_queue = store_queue_dict[client_aet]

    ae_scu = AE(scu_event.client_aet)
    # Add the requested presentation contexts (QR SCU)
    # ae_scu.add_requested_context(scu_event.query_model)
    ae_scu.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
    ae_scu.add_requested_context(StudyRootQueryRetrieveInformationModelGet)
    ds = Dataset()
    ds.QueryRetrieveLevel = 'PATIENT'
    # Unique key for PATIENT level
    ds.PatientID = '10180662'
    # Connect to the SCP server
    assoc = ae_scu.associate(config.server.address, config.server.port)
    role = build_role(CTImageStorage, scp_role=True)

    if assoc.is_established:
        # Use the C-GET service to send the identifier
        responses = assoc.send_c_get(ds, scu_event.query_model)
        total_images = None
        for status, identifier in responses:
            if scu_event.is_cancelled:
                assoc.send_c_cancel()
            if status:
                print(status.Status)
                if status.Status == 0xFF00 and total_images is None:
                    remaining = status.NumberOfRemainingSuboperations
                    completed = status.NumberOfCompletedSuboperations
                    failed = status.NumberOfFailedSuboperations
                    warnings = status.NumberOfWarningSuboperations
                    total_images = completed + remaining + failed + warnings
                    print(f"Total images to receive: {total_images}")
                    total_images_queue.put(total_images)
                if status.Status == 0x0000:
                    print("All images have been received.")
                    store_queue.put((0x0000, None))
            else:
                print("Connection timed out, was aborted or received invalid response")
                store_queue.put((0xA700, None))
        assoc.release()
    else:
        print("Association rejected, aborted or never connected")
        total_images_queue.put(None)