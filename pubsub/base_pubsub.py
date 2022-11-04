from abc import ABC, abstractmethod
from typing import Union


class BasePubSub(ABC):
    def __init__(self, client_type: str = "producer", *args, **kwargs) -> None:
        self.client_type = client_type
        super().__init__()
        if client_type not in ["producer", "consumer"]:
            raise ValueError("client_type must be either 'producer' or 'consumer'")
        self.client_type = client_type

    @abstractmethod
    def send(self, message: str = "Test") -> None:
        """Send a message to the topic."""
        pass

    @abstractmethod
    def receive(self):
        """Receive a message from a topic."""
        pass
