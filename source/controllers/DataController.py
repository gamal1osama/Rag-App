from fastapi import UploadFile
from .BaseController import BaseController

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # 1 MB in bytes

    def validate_uploaded_file(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale: # Convert max size from MB to bytes
            return False
        
        return True