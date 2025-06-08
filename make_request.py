from abc import ABC, abstractmethod
from dotenv import load_dotenv
from dotenv_utils import get_dotenv_api_key_or_exception
from google import genai
from google.genai.types import GenerateContentResponse
from base_interface import ModelInterface
from get_interface_by_map import get_interface_by_map
from openai import APIError
from openai import OpenAI
load_dotenv()

class RequestMakerInterface(ModelInterface):
    @abstractmethod
    def make_request(self, query_text):
        """Direct logic of making request to diferent types of models"""

class GeminiRequestMaker(RequestMakerInterface):
    def __init__(self, model,  specific_model_name: str = "gemini-2.0-flash"):
        self._client: genai.Client = genai.Client(api_key=get_dotenv_api_key_or_exception(key=model))
        self.specific_model_name: str = specific_model_name

    def make_request(self, query_text) -> GenerateContentResponse:
        return self._client.models.generate_content(
            model=self.specific_model_name, contents=query_text
        )

class DeepSeekRequestMaker(RequestMakerInterface):
    def __init__(self, model: str, specific_model: str = "deepseek-chat"):
        self._client = OpenAI(api_key=get_dotenv_api_key_or_exception(key=model), base_url="https://api.deepseek.com")
        self.specific_model_name: str = specific_model 
        
    def make_request(self, query_text):
        try:
            return self._client.chat.completions.create(
                model=self.specific_model_name,
                messages=[
                    {"role": "user", "content": query_text},
                ],
                stream=False
            )
        except Exception as e:
            if isinstance(e, APIError):
                print(e.body["message"])
                if e.body["message"] == "Insufficient Balance":
                    raise Exception("Your billing plan exceeded.")
                raise Exception(f"Error while making request: {e.message}")
            raise e

#=======================
class RequestService(ABC):
    @abstractmethod
    def make_request(self, query_text: str):
        """Make request to model through RequestInterface class"""

class RequestMakerServicre(RequestService):
    def __init__(self, model: str, model_map: dict[RequestMakerInterface] = { "gemini": GeminiRequestMaker, "deepseek": DeepSeekRequestMaker }):
        self.model: str = model
        self._model_map = model_map

    def make_request(self, query_text: str):
        request_maker: RequestMakerInterface = get_interface_by_map(model=self.model, model_map=self._model_map)
        request_maker: RequestMakerInterface = request_maker(model=self.model)
        
        return request_maker.make_request(query_text)