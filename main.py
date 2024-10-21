from pynetdicom import debug_logger, evt
from find_scp import handle_find
from move_scp import handle_move
from share import ae_scp
from store_scp import handle_store

# debug_logger()

# Register C-FIND request handling event
handlers = [(evt.EVT_C_FIND, handle_find), (evt.EVT_C_MOVE, handle_move), (evt.EVT_C_STORE, handle_store)]

# Start listening for incoming association requests
ae_scp.start_server(("0.0.0.0", 104), evt_handlers=handlers)
