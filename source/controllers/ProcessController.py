from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ProcessingEnums

import os

from langchain_community.document_loaders import TextLoader, PyMuPDFLoader


class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)

    def get_file_extension(self, file_id: str) -> str:
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id: str):

        file_ext = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id)

        if file_ext == ProcessingEnums.TXT.value:
            return TextLoader(file_path=file_path, encoding='utf-8') # we use utf-8 encoding because if the file contain arabic caracters
        
        elif file_ext == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path=file_path)
        
        return None
    
    def get_file_content(self, file_id: str) -> str:
        loader = self.get_file_loader(file_id)

        return loader.load()