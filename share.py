from pynetdicom import AE

# AE 实体配置分为 SCP 和 SCU 两部分，避免冲突

# SCP 用于接收来自客户端的请求
ae_scp = AE()

# SCU 用于与上级 PACS/DICOM 服务器通信
ae_scu = AE()
