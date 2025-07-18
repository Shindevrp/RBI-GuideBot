from typing import Tuple, List
import openai
import pinecone
from backend.core.config import settings

# Initialize clients once
openai.api_key = settings.OPENAI_API_KEY
pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV)


def retrieve_context(user_query: str, index_name: str) -> Tuple[str, List[str]]:
    """
    Embeds a query, searches a specified Pinecone index for relevant text chunks,
    and returns the context and sources. This is a pure retrieval step.
    """
    if not index_name:
        raise ValueError("Pinecone index name must be provided.")

    index = pinecone.Index(index_name)

    # Step 1: Embed the query
    try:
        embed_response = openai.Embedding.create(
            input=user_query,
            model="text-embedding-ada-002"
        )
        query_embedding = embed_response['data'][0]['embedding']
    except Exception as e:
        print(f"Embedding error: {e}")
        return f"Error creating embedding for query: {e}", []

    # Step 2: Search Pinecone for similar chunks
    try:
        search_response = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )
        matched_chunks = search_response.get('matches', [])
        context = "\n---\n".join([chunk['metadata']['text'] for chunk in matched_chunks])
        sources = list(set([chunk['metadata']['source'] for chunk in matched_chunks]))
    except Exception as e:
        print(f"Pinecone search error: {e}")
        return f"Error searching Pinecone index '{index_name}': {e}", []

    return context, sources