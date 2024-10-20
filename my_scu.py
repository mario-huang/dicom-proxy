from pynetdicom import AE

ae = AE()
ae.add_requested_context("1.2.840.10008.1.1")
assoc = ae.associate("127.0.0.1", 11112)
if assoc.is_established:
    print("Association established with Echo SCP!")
    status = assoc.send_c_echo()
    assoc.release()
else:
    # Association rejected, aborted or never connected
    print("Failed to associate")
