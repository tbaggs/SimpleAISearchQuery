import os
import sys
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.core.exceptions import HttpResponseError

def get_search_client():
    service_name = os.getenv("SEARCH_SERVICE_NAME")
    index_name = os.getenv("SEARCH_INDEX_NAME", "policies")
    if not service_name:
        print("ERROR: Set SEARCH_SERVICE_NAME environment variable.", file=sys.stderr)
        sys.exit(1)

    endpoint = f"https://{service_name}.search.windows.net"
    credential = DefaultAzureCredential()  # Supports managed identity, dev identity, etc.

    return SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

def simple_keyword_search(search_text: str, top: int = 5):
    client = get_search_client()
    try:
        results = client.search(
            search_text=search_text,
            top=top,
            query_type="simple"  # simple keyword (default); could omit
        )
        print(f"Top {top} results for '{search_text}':")
        for i, doc in enumerate(results):
            # Display key fields (customize per your schema)
            print(f"{i+1}. @search.score={doc.get('@search.score'):.4f} | id={doc.get('id')}")
    except HttpResponseError as e:
        print("Search request failed:", e.message, file=sys.stderr)
        # Optional: implement retry/backoff here for transient failures
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_policies.py \"keyword phrase\"", file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    simple_keyword_search(query)
