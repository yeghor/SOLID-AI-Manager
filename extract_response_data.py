from abc import ABC, abstractmethod

class extractHTTP(ABC):
    @abstractmethod
    def extract_text(response, model: str):
        """Extracting text field"""

    @abstractmethod
    def extract_http_response(response, model: str):
        """Extracting full HTTP response"""

class GeminiExtractorHTTP(extractHTTP):
    def __init__(self, model):
        self.model = model

    def extract_text(self, response):
        if self.model == "gemini":
            return response.text
        else:
            raise Exception("This model is not implemented yet")
    
    def extract_http_response(response):
        return response.json()

# =========================================

class ExtractResponseInterface(ABC):
    @abstractmethod
    def get_response_text(self):
        """Getting response text"""
    
    @abstractmethod
    def get_full_response(self):
        """Getting full HTTP Response"""

class ExtractGeminiResponse(ExtractResponseInterface):
    def __init__(self, model: str):
        self.model: str = model
        self._extractHTTP: extractHTTP = GeminiExtractorHTTP(model)

    def get_response_text(self, response):
        return self._extractHTTP.extract_text(response, self.model)
    
    def get_full_response(self, response):
        return self._extractHTTP.extract_http_response(response)