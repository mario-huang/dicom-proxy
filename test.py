from pydicom import Dataset
from pynetdicom import AE, StoragePresentationContexts, QueryRetrievePresentationContexts
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelMove

# 设置 Application Entity (AE)
ae = AE()

# 添加 C-MOVE 所需的 Presentation Context
ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
# ae.add_requested_context(StoragePresentationContexts)

# 远程 PACS 的 AE Title, IP 地址 和 端口号
pacs_ae_title = 'UpstreamPacs'
pacs_ip = '192.168.3.100'
pacs_port = 4242

# 存储目标的 AE Title, IP 地址 和 端口号
store_ae_title = 'DicomProxy'
store_ip = '192.168.3.119'
store_port = 4000

# 连接到 PACS 并发送 C-MOVE 请求
assoc = ae.associate(pacs_ip, pacs_port, ae_title=pacs_ae_title)

if assoc.is_established:
    # 构造 C-MOVE 请求的 Dataset
    ds = Dataset()
    ds.QueryRetrieveLevel = 'STUDY'
    ds.PatientID = '1182080'
    ds.StudyInstanceUID = '1.2.840.113820.104.17979.120240909073857560'

    # 发送 C-MOVE 请求
    responses = assoc.send_c_move(ds, store_ae_title, StudyRootQueryRetrieveInformationModelMove)

    # 处理响应
    for (status, identifier) in responses:
        if status:
            print(f'C-MOVE Response Status: 0x{status.Status:04x}')
        else:
            print('Connection timed out, was aborted or received invalid response')

    # 释放连接
    assoc.release()

else:
    print('Failed to associate with PACS')
