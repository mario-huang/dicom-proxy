from pynetdicom import AE

# Separate AE configuration for SCP and SCU to avoid conflicts

# AE for receiving requests from clients
ae_scp = AE()

# AE for communicating with upstream PACS/DICOM server
ae_scu = AE()
