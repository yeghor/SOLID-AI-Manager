from make_request import RequestMakerServicre, RequestService
from extract_response_data import ResponseExtractorService, ExtractorService
from abc import ABC, abstractmethod

class MainAiInterface(ABC):
    @abstractmethod
    def query(self, prompt: str) -> str:
        """Making request, extracting data, returning procesed data to client"""

class MainAiService(MainAiInterface):
    def __init__(self, model):
        self.model = model
        self.request_maker: RequestService = RequestMakerServicre(model=model)
        self.extractor: ExtractorService = ResponseExtractorService(model=model)
    
    def query(self, prompt: str) -> str:
        response = self.request_maker.make_request(query_text=prompt)
        return self.extractor.extract_text(response=response)
    