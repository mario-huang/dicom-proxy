from typing import List
from pynetdicom import AE
import json
from dataclasses import dataclass
from queue import Queue


# Define the AETConfig class to represent source and target
@dataclass
class AETConfig:
    aet: str
    ip: str
    port: int


# Define the Config class to represent the entire JSON structure
@dataclass
class Config:
    proxy: AETConfig
    server: AETConfig
    clients: List[AETConfig]


# Open and read the JSON file
with open("config.json", "r") as file:
    data_dict = json.load(file)

# Manually map the dictionary to a Config object
config = Config(
    proxy=AETConfig(**data_dict["proxy"]),
    server=AETConfig(**data_dict["server"]),
    clients=[AETConfig(**client) for client in data_dict["clients"]],
)

# AE for receiving requests from clients
ae_scp = AE(config.proxy.aet)

# Queue used to store the status of the store operation
store_queue = Queue()
# move_queue = Queue()
total_images_queue = Queue()
