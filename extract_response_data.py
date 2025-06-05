from abc import ABC, abstractmethod

class ModelExtractor(ABC):
    @abstractmethod
    def extract_text(resposne):
        """Extracting text field with prefered model logic"""

    @abstractmethod
    def extract_http_response(response):
        """Extracting HTTP response with prefered model logic"""

class GeminiExtractor(ModelExtractor):
    def extract_text(response):
        return response.text
    
    def extract_http_response(response):
        return response.json()  

# =========================================

class ResponseExtractorInterface(ABC):
    @abstractmethod
    def extract_text(self, response):
        """Calling protected method to choose right method to call to extract text"""

    @abstractmethod
    def extract_http_response(self, response):
        """Calling protected method to choose right method to call to extract HTTP response"""

class ResponseExtractor(ResponseExtractorInterface):
    def __init__(self, model, model_map: dict[str, ModelExtractor]):
        self.model = model
        self._model_map = model_map

    def extract_text(self, response):
        extractor: ModelExtractor = self._model_map.get(self.model) 
        if not extractor:
            raise ValueError("This model is not implemented")
        return extractor.extract_text(response)

    def extract_http_response(self, response):
        extractor: ModelExtractor = self._model_map.get(self.model) 
        if not extractor:
            raise ValueError("This model is not implemented")
        return extractor.extract_http_response(response)