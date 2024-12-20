from pynetdicom import AllStoragePresentationContexts
from share import ae_scp, store_queue_dict

# Add the Storage SCP's supported presentation contexts
ae_scp.supported_contexts = AllStoragePresentationContexts


# Implement a handler for evt.EVT_C_STORE
def handle_store(event):
    client_aet = event.request.MoveOriginatorApplicationEntityTitle
    if client_aet is None:
        client_aet = event.assoc.requestor.ae_title
    store_queue = store_queue_dict[client_aet]
    print(f"handle_store, client_aet: {client_aet}")
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds = event.dataset
    # Add the File Meta Information
    ds.file_meta = event.file_meta
    # print(f"Received and forwarded image: {ds.SOPInstanceUID}")
    
    # Save the dataset using the SOP Instance UID as the filename
    # ds.save_as(ds.SOPInstanceUID, write_like_original=False)
    # 将数据集保存到临时文件
    # ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # 从文件中重新读取数据集
    # ds_copy = dcmread(ds.SOPInstanceUID)

    # 调用 storeScu
    # storeScu(ds_copy, "192.168.3.222", 6000)
    store_queue.put((0xFF00, ds))
    # 删除临时文件
    # os.remove(temp_filename)
    # Return a 'Success' status
    return 0x0000

    # return storeScu(ds, "192.168.3.222", 6000)
