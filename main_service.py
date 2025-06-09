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
        self.request_maker: RequestService = RequestMakerService(model=model)
        self.extractor: ExtractorService = ResponseExtractorService(model=model)
    
    def query(self, prompt: str) -> str:
        response = self.request_maker(query_text=prompt)
        return self.extractor.extract_text(response=response)
    
    def chat_message(self, prompt):
        response = self.request_maker.send_chat_message(query_text=prompt)
        return self.extractor.extract_text(response)

service = MainAiService("deepseek")

print(service.chat_message("What was my first request in this chat?"))