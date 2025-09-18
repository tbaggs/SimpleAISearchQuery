import os
import sys
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

service_name = os.getenv("SEARCH_SERVICE_NAME")
index_name = os.getenv("SEARCH_INDEX_NAME") or "policies"
if not service_name:
    raise ValueError("SEARCH_SERVICE_NAME not set.")

endpoint = f"https://{service_name}.search.windows.net"
credential = DefaultAzureCredential()
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

query = sys.argv[1] if len(sys.argv) > 1 else "covid"

results = client.search(search_text=query)
for i, result in enumerate(results, start=1):
    score = result.get("@search.score")
    doc_id = result.get("id")
    print(f"{i}. Score={score:.4f} id={doc_id}")