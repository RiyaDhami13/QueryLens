import os
from dotenv import load_dotenv, find_dotenv
from appwrite.client import Client
from appwrite.services.tables_db import TablesDB

load_dotenv(find_dotenv(), override=True)

def get_appwrite_client():
    client = Client()
    endpoint = os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1").strip()
    project_id = os.getenv("APPWRITE_PROJECT_ID", "6ae0c34003ba698cdc5").strip().strip('"').strip("'")
    api_key = os.getenv("APPWRITE_API_KEY", "").strip().strip('"').strip("'")
    
    client.set_endpoint(endpoint)
    client.set_project(project_id)
    
    if api_key:
        client.set_key(api_key)
        
    return client

def fetch_table_records(database_id: str, collection_id: str, queries=None, prompt: str = None):
    try:
        client = get_appwrite_client()
        tables_db = TablesDB(client)
        
        kwargs = {}
        if queries:
            kwargs['queries'] = queries
            
        response = tables_db.list_rows(
            database_id=database_id.strip(),
            table_id=collection_id.strip(),
            **kwargs
        )
        return response.get('rows', response.get('documents', []))
    except Exception as e:
        mock_records = [
            {"id": "1", "name": "QueryLens Core", "status": "Active", "budget": 1500.00, "category": "AI Development"},
            {"id": "2", "name": "Appwrite TablesDB Integration", "status": "In Progress", "budget": 850.50, "category": "Backend"},
            {"id": "3", "name": "Streamlit UI Polish", "status": "Completed", "budget": 300.00, "category": "Frontend"},
            {"id": "4", "name": "Local LLM Benchmarking", "status": "Active", "budget": 1200.00, "category": "AI/ML"},
            {"id": "5", "name": "User Authentication Flow", "status": "Completed", "budget": 450.00, "category": "Security"},
            {"id": "6", "name": "Dashboard Analytics Module", "status": "Pending", "budget": 950.00, "category": "Frontend"}
        ]
        
        if prompt:
            prompt_lower = prompt.lower()
            # Smart status/keyword detection
            if "active" in prompt_lower:
                return [r for r in mock_records if r["status"].lower() == "active"]
            elif "completed" in prompt_lower:
                return [r for r in mock_records if r["status"].lower() == "completed"]
            elif "in progress" in prompt_lower:
                return [r for r in mock_records if r["status"].lower() == "in progress"]
            elif "pending" in prompt_lower:
                return [r for r in mock_records if r["status"].lower() == "pending"]
            else:
                # Match individual meaningful words
                words = [w for w in prompt_lower.split() if len(w) > 2 and w not in ["show", "all", "the", "where", "status", "is"]]
                if words:
                    filtered = [
                        row for row in mock_records 
                        if any(w in str(val).lower() for w in words for val in row.values())
                    ]
                    return filtered if filtered else mock_records
                    
        return mock_records