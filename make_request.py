from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from dotenv_utils import get_dotenv_variable_or_exception
from google import genai

load_dotenv()

class RequestInterface(ABC):
    @abstractmethod
    def make_request(self):
        """Direct logic of making request to diferent types of models"""

class DirectModelRequester(RequestInterface):
    def __init__(self, model: str, api_key):
        self.model: str = model
        self.api_key: str = api_key
        self._model_map = {
            "gemini": self._make_gemini_request
        }

    def make_request(self, query_text):
        for model_name, request_method in self._model_map.items():
            if self.model == model_name:
                return request_method(quert_text=query_text)
        raise ValueError("This model is not implemented yet")

    def _make_gemini_request(self, query_text):
        client = genai.Client(api_key=self.api_key)

        return client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query_text,
        )

#=======================

class RequestService(ABC):
    @abstractmethod
    def make_request(self, query_text: str):
        """Make request to model through RequestInterface class"""

class RequestMaker(RequestService):
    def __init__(self, model: str):
        self.model: str = model
        self._api_key: str = get_dotenv_variable_or_exception(model)
        self._request_interface: RequestInterface = DirectModelRequester(model=model, api_key=self._api_key)

    def make_request(self, query_text: str):
        return self._request_interface.make_request(query_text)