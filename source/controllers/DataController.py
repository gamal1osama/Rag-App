from fastapi import UploadFile
from models import ResponseSignal
from .BaseController import BaseController

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale_MB2b = 1024 * 1024  # 1 MB in bytes

    def validate_uploaded_file(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale_MB2b: # Convert max size from MB to bytes
            return False , ResponseSignal.FILE_SIZE_EXCEEDS_LIMIT.value
        
        return True , ResponseSignal.FILE_VALIDATION_SUCCESS.value