from .BaseController import BaseController
from stores.llm.LLMEnums import DocumentTypeEnums
from models.db_schemas import Project, DataChunk
from typing import List
import json




class NLPController(BaseController):

    def __init__(self, vector_db_client, generation_client, embedding_client):
        super().__init__()

        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    
    def create_collection_name(self, project_id: str) -> str:
        return f"collection_{project_id}".strip()
    

    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vector_db_client.delete_collection(collection_name=collection_name)
        

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name=collection_name)

        return json.loads( # that usually solves the issue of non-serializable objects in the response (we actually get the error when we try to return the collection_info object in the response, so we convert it to json string and then parse it back to dict
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
        

    def index_into_db(self, project: Project, chunks: List[DataChunk], do_reset: bool = False, chunks_ids: List[str] = None) -> bool:
        
        # step 1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)


        # step 2: manage items
        texts = [chunk.chunk_text for chunk in chunks]
        metadatas = [chunk.chunk_metadata for chunk in chunks]

        vectors = [
            self.embedding_client.embed_text(text=text, document_type=DocumentTypeEnums.DOCUMENT.value) 
            for text in texts
        ]


        # step 3: create collection if not exists
        _ = self.vector_db_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )

        # step 4: insert items into collection
        _ = self.vector_db_client.insert_many(
            collection_name=collection_name,
            texts=texts, 
            vectors=vectors, 
            metadatas=metadatas,
            record_ids=chunks_ids
        )


        return True
    

    
    def search_vector_db_collection(self,
                                    project: Project,
                                    text: str,
                                    limit: int = 10):

        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get the text embedding vector
        query_vector = self.embedding_client.embed_text(text=text, document_type=DocumentTypeEnums.QUERY.value)
        if not query_vector:
            return None

        # step3: do semantic search
        search_results = self.vector_db_client.search_by_vector(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
        if not search_results:
            return None


        return search_results


    def answer_rag_query(self, project: Project, query: str, limit: int = 10):
        
        # step1: retrieve related chunks from vector db
        retrieved_chunks = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit
        )

        if not retrieved_chunks:
            return None


        # step2: construct prompt for generation client (LLM)
        system_prompt = """
            You are an assistant to generate a response for the user.

            You will be provided by a set of documents associated with the user's query.

            You have to generate a response based on the documents provided. Ignore the documents that are not relevant to the user's query.    
        
        """