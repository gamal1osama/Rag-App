from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from .enums import DataBaseEnum
from bson import ObjectId

from sqlalchemy.future import select
from sqlalchemy import delete



class AssetModel(BaseDataModel):
    
    def __init__(self, db_client):
        super().__init__(db_client)

        self.db_client = self.db_client

    @classmethod
    async def create_instance(cls, db_client):
        # we create this method and don't use the __init__ because we need to do async calls and __init__ can't be async
        instance = cls(db_client)
        return instance



    async def create_asset(self, asset: Asset):
        
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)
        return asset
    

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Asset).where(
                    Asset.asset_project_id == asset_project_id,
                    Asset.asset_type == asset_type
                )
                result = await session.execute(stmt)
                assets = result.scalars().all()
        return assets
        
    
    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Asset).where(
                    Asset.asset_project_id == asset_project_id,
                    Asset.asset_name == asset_name
                )
                result = await session.execute(stmt)
                asset = result.scalar_one_or_none()
        return asset
