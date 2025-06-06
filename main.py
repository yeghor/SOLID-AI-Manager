from make_request import RequestService, RequestMaker
from extract_response_data import ResponseExtractorService, ResponseExtractorService
class AIManager:
    def __init__(self, model: str):
        self.model = model
        self.request_service: RequestService = RequestMaker(model=model)
        self.extract_data_service: ResponseExtractorService = ResponseExtractorService(model=model)
