from typing import Tuple, List

def rag_query(user_query: str) -> Tuple[str, List[str], dict]:
    """
    Embed query using OpenAI, search Pinecone for relevant chunks, and return answer, sources, and chart data.
    """
    import openai
    import pinecone
    import os
    # Use environment variables for API keys and config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
    INDEX_NAME = os.getenv("PINECONE_INDEX", "rbi-guidebot-index")

    openai.api_key = OPENAI_API_KEY
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    index = pinecone.Index(INDEX_NAME)

    # Step 1: Embed the query
    try:
        embed_response = openai.Embedding.create(
            input=user_query,
            model="text-embedding-ada-002"
        )
        query_embedding = embed_response['data'][0]['embedding']
    except Exception as e:
        return f"Embedding error: {e}", [], None

    # Step 2: Search Pinecone for similar chunks
    try:
        search_response = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )
        matched_chunks = search_response['matches']
        context = "\n".join([chunk['metadata']['text'] for chunk in matched_chunks])
        sources = [chunk['metadata']['source'] for chunk in matched_chunks]
    except Exception as e:
        return f"Pinecone search error: {e}", [], None

    # Step 3: Generate answer using LLM (OpenAI GPT-4)
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert RBI compliance assistant for NBFCs."},
                {"role": "user", "content": f"Query: {user_query}\nContext: {context}"}
            ]
        )
        answer = completion['choices'][0]['message']['content']
    except Exception as e:
        return f"LLM error: {e}", sources, None

    # Step 4: (Optional) Detect numeric data for charting
    chart_data = None
    # Add logic to parse answer/context for numeric data if needed

    return answer, sources, chart_data
