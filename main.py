from pynetdicom import debug_logger
from pynetdicom import evt
from find_scp import handle_find
from share import ae

# debug_logger()

# Register C-FIND request handling event
handlers = [(evt.EVT_C_FIND, handle_find)]

# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)