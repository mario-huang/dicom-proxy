from typing import Dict, List
from pynetdicom import AE
import json
from dataclasses import dataclass
from queue import Queue


# Define the AETConfig class to represent source and target
@dataclass
class AETConfig:
    aet: str
    address: str
    port: int


# Define the Config class to represent the entire JSON structure
@dataclass
class Config:
    debug: bool
    proxy: AETConfig
    server: AETConfig
    clients: List[AETConfig]
    
# Open and read the JSON file
with open("config.json", "r") as file:
    data_dict = json.load(file)

# Manually map the dictionary to a Config object
config = Config(
    debug=data_dict.get("debug", False),
    proxy=AETConfig(**data_dict["proxy"]),
    server=AETConfig(**data_dict["server"]),
    clients=[AETConfig(**client) for client in data_dict["clients"]],
)

# AE for receiving requests from clients
ae_scp = AE(config.proxy.aet)

# Queue used to store the status of the store operation
# store_queues = dict
# move_queue = Queue()
# total_images_queues = Queue()
store_queue_dict: Dict[str, Queue] = {}
total_images_queue_dict: Dict[str, Queue] = {}
