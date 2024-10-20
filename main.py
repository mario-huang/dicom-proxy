from pynetdicom import debug_logger, evt
from find_scp import handle_find
from move_scp import handle_move
from share import ae_scp

# debug_logger()

# Register C-FIND request handling event
handlers = [(evt.EVT_C_FIND, handle_find), (evt.EVT_C_MOVE, handle_move)]

# Start listening for incoming association requests
ae_scp.start_server(("0.0.0.0", 11112), evt_handlers=handlers)
