from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse

from .schemas.nlp import PushRequest
from ..models import ProjectModel

import logging



logger = logging.getLogger(__name__)




nlp_router = APIRouter(
    prefix="api/v1/nlp", 
    tags=["api_v1", "nlp"]
)




@nlp_router.post("/index/push/{project_id}")
async def index_project(project_id: str, request: Request, push_request: PushRequest):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create(project_id=project_id)

    pass

    
