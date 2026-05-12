from .BaseDataModel import BaseDataModel
from .db_schemas import Project
from .enums import DataBaseEnum

from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client)

        self.db_client = self.db_client


    @classmethod
    async def create_instance(cls, db_client):
        # we create this method and don't use the __init__ because we need to do async calls and __init__ can't be async
        instance = cls(db_client)
        return instance



    async def create_project(self, project: Project):
        
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()  # Commit the transaction to persist the changes
            await session.refresh(project)  # Refresh to get the updated project with ID

        return project
    


    async def get_project_or_create(self, project_id: str):
        
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = query.scalar_one_or_none()

                if result is None:
                    project = self.create_project(Project(project_id=project_id))
                    return project
                
                return result




    async def get_all_projects(self, page: int = 1, page_size: int = 10): # we do pagination here to avoid fetching too many records at once
        


        async with self.db_client() as session:
            async with session.begin():

                total_records = await session.execute(select(func.count(Project.project_id)))
                total_records = total_records.scalar_one() 

                total_pages = total_records // page_size
                if total_records % page_size > 0:
                    total_pages += 1

                skip = (page - 1) * page_size
                query = select(Project).offset(skip).limit(page_size)

                projects = await session.execute(query).scalars().all()

                return projects, total_pages
