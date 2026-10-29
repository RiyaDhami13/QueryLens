import os
import json
import ollama
from appwrite.query import Query

def translate_prompt_to_appwrite_queries(user_prompt: str, sample_columns: list) -> list:
    """
    Uses an LLM to translate natural language into Appwrite Query syntax.
    """
    system_prompt = f"""
    You are a database query expert for Appwrite. 
    Available columns in this table: {sample_columns}
    
    Translate the user's natural language request into a valid JSON list of filter rules.
    Choose from these operations:
    - "equal": [column, value]
    - "search": [column, keyword]
    - "greaterThan": [column, number]
    - "lessThan": [column, number]
    
    Return ONLY valid JSON format like this example:
    [ {{ "op": "equal", "field": "country", "value": "Nepal" }} ]
    If no filter is needed, return an empty list [].
    """
    
    try:
        response = ollama.chat(
            model='phi3',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            options={'temperature': 0.1}
        )
        
        content = response['message']['content'].strip()
        # Clean up markdown code blocks if returned by LLM
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        filters = json.loads(content)
        
        # Map JSON filters to Appwrite SDK Query objects
        appwrite_queries = []
        for f in filters:
            op = f.get("op")
            field = f.get("field")
            val = f.get("value")
            
            if op == "equal":
                appwrite_queries.append(Query.equal(field, val))
            elif op == "search":
                appwrite_queries.append(Query.search(field, str(val)))
            elif op == "greaterThan":
                appwrite_queries.append(Query.greaterThan(field, val))
            elif op == "lessThan":
                appwrite_queries.append(Query.lessThan(field, val))
                
        return appwrite_queries
    except Exception as e:
        print(f"Query generation fallback: {e}")
        return []