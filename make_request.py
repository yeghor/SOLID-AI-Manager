from abc import ABC, abstractmethod
from dotenv import load_dotenv
from dotenv_utils import get_dotenv_api_key_or_exception
from google import genai
from google.genai.errors import APIError
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

class ChatCapableRequestMaker(RequestMakerInterface):
    @abstractmethod
    def send_message_chat(self, chat_message):
        """Send message with chat history track"""

class GeminiRequestMaker(ChatCapableRequestMaker):
    def __init__(self, model,  specific_model_name: str = "gemini-2.0-flash"):
        self._client: genai.Client = genai.Client(api_key=get_dotenv_api_key_or_exception(key=model))
        self._chat = self._client.chats.create(model=specific_model_name)
        self.specific_model_name: str = specific_model_name

    def make_request(self, query_text) -> GenerateContentResponse:
        try:
            return self._client.models.generate_content(
                model=self.specific_model_name, contents=query_text
            )
        except Exception as e:
            if isinstance(e, APIError):
                raise Exception(f"Error occured while making request: {e.message}")
            raise Exception(f"Uknown error occured while making request: {e}")

    def send_message_chat(self, query_text) -> GenerateContentResponse:
        try:
            return self._chat.send_message(message=query_text)
        except Exception as e:
            if isinstance(e, APIError):
                raise Exception(f"Error error occured while making chat request: {e.message}")
            raise Exception(f"Uknown error occured ocured")

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

class RequestService(ABC):
    @abstractmethod
    def make_request(self, query_text: str):
        """Make request to model through RequestInterface class"""
        
    @abstractmethod
    def _get_request_maker(self) -> RequestMakerInterface:
        """Getting request maker interface by model map and name"""    

    @abstractmethod
    def send_chat_message(self, query_text: str):
        """Sending chat message. If model supports."""

class RequestMakerService(RequestService):
    def __init__(self, model: str, model_map: dict[RequestMakerInterface] = { "gemini": GeminiRequestMaker, "deepseek": DeepSeekRequestMaker }):
        self.model: str = model
        self._model_map = model_map

    def make_request(self, query_text: str):
        request_maker = self._get_request_maker()
        return request_maker.make_request(query_text)

    def _get_request_maker(self) -> RequestMakerInterface:
        request_maker: RequestMakerInterface = get_interface_by_map(model=self.model, model_map=self._model_map)
        return request_maker(model=self.model)       

    def send_chat_message(self, query_text):
        request_maker: RequestMakerInterface = self._get_request_maker()
        if not isinstance(request_maker, ChatCapableRequestMaker):
            raise Exception(f"Model - {self.model.title()} doesn't support chat interactions")
        return request_maker.send_message_chat(query_text=query_text)