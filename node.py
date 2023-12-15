import datetime
import threading
from abc import ABC, abstractmethod

from node_logger import NodeLogger


class Node(ABC):

    def __init__(self, node_id):
        self.node_id = node_id
        self.satellites = []
        self.completed_satellites = []
        self.data_gravity = None
        self.data_gravity_receiver_thread = None
        self.stop_data_gravity_receiver_flag = threading.Event()
        self.satellite_receiver_thread = None
        self.stop_satellite_receiver_flag = threading.Event()
        self.satellite_lock = threading.Lock()
        self.logger = NodeLogger(node_id).getLogger()

    @abstractmethod
    def compute_data_gravity(self):
        pass

    @abstractmethod
    def request_data_gravity(self):
        pass

    @abstractmethod
    def respond_data_gravity(self):
        pass

    @abstractmethod
    def create_satellite(self, satellite_id, trip, jobs):
        pass

    @abstractmethod
    def train_satellite(self, satellite):
        pass

    @abstractmethod
    def receive_satellite(self):
        pass

    @abstractmethod
    def send_satellite(self, satellite):
        pass
