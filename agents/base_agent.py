from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        print(f"[{self.name}] Initialized as {self.role}")

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def log(self, message: str):
        print(f"[{self.name}] {message}")
