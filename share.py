from pynetdicom import AE
import json
from dataclasses import dataclass

# 定义 AETConfig 类来表示 source 和 target
@dataclass
class AETConfig:
    aet: str
    ip: str
    port: int

# 定义 Config 类来表示整个 JSON 结构
@dataclass
class Config:
    source: AETConfig
    target: AETConfig

# 打开并读取 JSON 文件
with open('config.json', 'r') as file:
    data_dict = json.load(file)

# 手动将字典映射为 Config 对象
config = Config(
    source=AETConfig(**data_dict['source']),
    target=AETConfig(**data_dict['target'])
)

# 打印 Config 对象
print(config)


# Separate AE configuration for SCP and SCU to avoid conflicts

# AE for receiving requests from clients
ae_scp = AE("DicomProxy")
