from pynetdicom import AE
from scu_event import SCUEvent
from share import move_queue, config, total_images_queue

def moveScu(scu_event: SCUEvent) -> None:
    ae_scu = AE(config.proxy.aet)
    # Add a requested presentation context
    ae_scu.add_requested_context(scu_event.query_model)
    # Connect to the upstream SCP server
    assoc = ae_scu.associate(config.server.ip, config.server.port)

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
                # if status.Status == 0x0000:
                #     print("All images have been received.")
                #     move_queue.put(None)
            else:
                print('Connection timed out, was aborted or received invalid response')
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')