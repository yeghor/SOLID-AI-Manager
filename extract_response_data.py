from abc import ABC, abstractmethod
from base_interface import ModelInterface
from google.genai.types import GenerateContentResponse
from openai.types.chat import ChatCompletion
from get_interface_by_map import get_interface_by_map

class ModelExtractorInterface(ModelInterface):
    @abstractmethod
    def extract_text(response):
        """Extracting text field with prefered model logic"""

    @abstractmethod
    def extract_json_from_response(response):
        """Extracting HTTP response with prefered model logic"""

class GeminiExtractor(ModelExtractorInterface):
    def extract_text(response: GenerateContentResponse) -> str:
        return response.text
    
    def extract_json_from_response(response: GenerateContentResponse) -> str:
        try:
            return response.model_dump_json()  
        except Exception as e:
            raise Exception(f"Error while extracting json data: {e}")

class DeepSeekExtractor(ModelExtractorInterface):
    def extract_text(response: ChatCompletion) -> str:
        return response.choices[0].message.content

    def extract_json_from_response(response: ChatCompletion) -> str:
        try:
            return response.model_dump_json()
        except Exception as e:
            raise Exception(f"Error while extracting json data: {e}")

class ExtractorService(ABC):
    @abstractmethod
    def extract_text(self, response):
        """Calling protected method to choose right method to call to extract text"""

    @abstractmethod
    def extract_json_response(self, response):
        """Calling protected method to choose right method to call to extract HTTP response"""

class ResponseExtractorService(ExtractorService):
    def __init__(self, model, model_map: dict[str, ModelExtractorInterface] = { "gemini": GeminiExtractor, "deepseek": DeepSeekExtractor }):
        self.model = model
        self._model_map = model_map

    def extract_text(self, response):
        extractor: ModelExtractorInterface | None = self._model_map.get(self.model)
        extractor = extractor()
        if not extractor:
            raise ValueError("This model is not implemented")
        return extractor.extract_text(response)

    def extract_json_response(self, response):
        extractor: ModelExtractorInterface = get_interface_by_map(model_map=self._model_map, model=self.model)
        if not extractor:
            raise ValueError("This model is not implemented")
        return extractor.extract_json_from_response(response)