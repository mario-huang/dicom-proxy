from typing import Iterator, Tuple
from pydicom.dataset import Dataset

from pynetdicom import AE, build_role
from scu_event import SCUEvent
from share import config
from pynetdicom import debug_logger, evt
from pynetdicom import AllStoragePresentationContexts
from share import store_queue_dict, config, total_images_queue_dict

from store_scp import handle_store


def get_scu(scu_event: SCUEvent) -> Iterator[Tuple[int, Dataset | None]]:
    client_aet = scu_event.client_aet
    total_images_queue = total_images_queue_dict[client_aet]
    store_queue = store_queue_dict[client_aet]

    ae_scu = AE(scu_event.client_aet)
    # Add the requested presentation contexts (QR SCU)
    ae_scu.add_requested_context(scu_event.query_model)
    ae_scu.supported_contexts = AllStoragePresentationContexts
    # Create an SCP/SCU Role Selection Negotiation item for CT Image Storage
    # role = build_role(AllStoragePresentationContexts, scp_role=True)
    # Connect to the SCP server
    assoc = ae_scu.associate(config.server.address, config.server.port, evt_handlers=[(evt.EVT_C_STORE, handle_store)])

    if assoc.is_established:
        # Use the C-GET service to send the identifier
        responses = assoc.send_c_get(scu_event.identifier, scu_event.query_model)
        total_images = None
        for status, identifier in responses:
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

        # Release the association
        assoc.release()
    else:
        print("Association rejected, aborted or never connected")
        total_images_queue.put(None)