import os
from appwrite.client import Client
from appwrite.services.vectors_db import VectorsDB

def get_vectors_client():
    client = Client()
    client.set_endpoint(os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1"))
    client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
    client.set_key(os.getenv("APPWRITE_API_KEY"))
    return VectorsDB(client)

def search_schema_context(query_text: str, collection_id: str):
    """
    Searches Appwrite VectorsDB for relevant table schemas based on user query.
    """
    vectors_db = get_vectors_client()
    # Perform vector similarity search on database fields/schemas
    try:
        results = vectors_db.query_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=collection_id,
            query=query_text
        )
        return results
    except Exception as e:
        print(f"Vector search fallback: {e}")
        return []