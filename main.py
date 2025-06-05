from make_request import RequestService, RequestMaker
from extract_response_data import ResponseExtractorInterface, ResponseExtractor
class AIManager:
    def __init__(self, model: str):
        self.model = model
        self.request_service: RequestService = RequestMaker(model=model)
        self.extract_data_service: ResponseExtractorInterface = ResponseExtractor(model=model)
