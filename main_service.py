from make_request import RequestMakerService, RequestService
from extract_response_data import ResponseExtractorService, ExtractorService
from abc import ABC, abstractmethod

class MainAiInterface(ABC):
    @abstractmethod
    def query(self, prompt: str) -> str:
        """Making request, extracting data, returning procesed data to client"""

    @abstractmethod
    def chat_message(self, prompt: str) -> str:
        """Making chat request, extracting data, returning procesed data to client"""

class MainAiService(MainAiInterface):
    def __init__(self, model):
        self.model = model
        self._request_maker: RequestService = RequestMakerService(model=model)
        self._extractor: ExtractorService = ResponseExtractorService(model=model)
    
    def query(self, prompt: str, json:bool=False) -> str:
        response = self._request_maker.make_request(query_text=prompt)
        if json:
            return self._extractor.extract_json_response(response=response)
        return self._extractor.extract_text(response=response)
    
    def chat_message(self, prompt):
        response = self._request_maker.send_chat_message(query_text=prompt)
        return self._extractor.extract_text(response)

service = MainAiService("gemini")

print(service.query("How much os 2 times 2?", json=True))