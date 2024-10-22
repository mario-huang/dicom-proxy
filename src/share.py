from typing import List
from pynetdicom import AE
import json
from dataclasses import dataclass
from queue import Queue

# 定义 AETConfig 类来表示 source 和 target
@dataclass
class AETConfig:
    aet: str
    ip: str
    port: int

# 定义 Config 类来表示整个 JSON 结构
@dataclass
class Config:
    proxy: AETConfig
    server: AETConfig
    clients: List[AETConfig]

# 打开并读取 JSON 文件
with open('config.json', 'r') as file:
    data_dict = json.load(file)

# 手动将字典映射为 Config 对象
config = Config(
    proxy=AETConfig(**data_dict['proxy']),
    server=AETConfig(**data_dict['server']),
    clients=[AETConfig(**client) for client in data_dict['clients']]
)

# Separate AE configuration for SCP and SCU to avoid conflicts

# AE for receiving requests from clients
ae_scp = AE(config.proxy.aet)

# 用于存储 store 操作的状态队列
move_queue = Queue()
total_images_queue = Queue()