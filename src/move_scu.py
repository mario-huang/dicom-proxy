from pynetdicom import AE
from scu_event import SCUEvent
from share import store_queue_dict, config, total_images_queue_dict

def move_scu(scu_event: SCUEvent) -> None:
    client_aet = scu_event.client_aet
    total_images_queue = total_images_queue_dict[client_aet]
    store_queue = store_queue_dict[client_aet]
    
    ae_scu = AE(client_aet)
    # Add a requested presentation context
    ae_scu.add_requested_context(scu_event.query_model)
    # Connect to the upstream SCP server
    assoc = ae_scu.associate(config.server.address, config.server.port)

    if assoc.is_established:
        # Use the C-MOVE service to send the identifier
        responses = assoc.send_c_move(scu_event.identifier, config.proxy.aet, scu_event.query_model)
        total_images = None
        for (status, identifier) in responses:
            if scu_event.is_cancelled:
                assoc.send_c_cancel()
            if status:
                # print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
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
                print('Connection timed out, was aborted or received invalid response')
                store_queue.put((0xA700, None))
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')
        total_images_queue.put(None)
