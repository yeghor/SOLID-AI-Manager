from abc import ABC, abstractmethod
from dotenv import load_dotenv
from dotenv_utils import get_dotenv_variable_or_exception
from google import genai
from google.genai.types import GenerateContentResponse
from base_interface import ModelInterface

load_dotenv()

class RequestMakerInterface(ModelInterface):
    @abstractmethod
    def make_request(self, query_text):
        """Direct logic of making request to diferent types of models"""

class GeminiRequestMaker(RequestMakerInterface):
    def __init__(self, model,  specific_model_name: str = "gemini-2.0-flash"):
        self.client: genai.Client = genai.Client(api_key=get_dotenv_variable_or_exception(model))
        self.model_name: str = specific_model_name

    def make_request(self, query_text) -> GenerateContentResponse:
        return self.client.models.generate_content(
            model=self.model_name, contents=query_text
        )

#=======================

class RequestService(ABC):
    @abstractmethod
    def make_request(self, query_text: str):
        """Make request to model through RequestInterface class"""

class RequestMakerServicre(RequestService):
    def __init__(self, model: str, model_map: dict[RequestMakerInterface] = { "gemini": ModelInterface }):
        self.model: str = model
        self._api_key: str = get_dotenv_variable_or_exception(model)
        self._model_map = model_map

    def make_request(self, query_text: str):
        request_maker: ModelInterface | None = self._model_map.get(self.model)
        if not request_maker:
            raise ValueError("This model is not implemented yet")
        
        return request_maker.make_request(query_text)