from pynetdicom import debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from pynetdicom import AE, evt, StoragePresentationContexts, AllStoragePresentationContexts
from find_scp import handle_find
from share import ae

# debug_logger()

# 为 C-FIND 操作添加支持的 Presentation Context
ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

# 注册 C-FIND 请求处理事件
handlers = [(evt.EVT_C_FIND, handle_find)]

# 启动 SCP，监听端口 11112
ae.start_server(('0.0.0.0', 11112), evt_handlers=handlers)