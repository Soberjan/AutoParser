from abc import abstractmethod
from examples.w9.data_manager import DataManager
from utils.logger import create_logger


class BaseController:
    def __init__(self) -> None:
        self._dm = DataManager()
        self.logger = create_logger()

    @abstractmethod
    async def get_objects(self):...
    
    @abstractmethod
    async def get_object(self, obj_id):...
    