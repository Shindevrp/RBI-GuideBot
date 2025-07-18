import openai
from backend.core.config import settings
from backend.agents.retrieval import retrieve_context

openai.api_key = settings.OPENAI_API_KEY

def generate_final_answer(query: str, context: str, sources: list) -> str:
    """Generates a comprehensive answer using the retrieved context."""
    system_prompt = (
        "You are an expert RBI compliance and NBFC lending assistant. "
        "Answer the user's query based on the provided context. "
        "Be clear, concise, and professional. "
        "At the end of your response, list all the source documents you used, prefixed with 'Sources:'."
    )
    
    user_content = f"Query: {query}\n\nContext:\n{context}"

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        answer = completion.choices[0].message['content']
        
        if sources:
            sources_text = "\n\nSources:\n- " + "\n- ".join(sources)
            answer += sources_text
            
        return answer
    except Exception as e:
        print(f"LLM error during answer generation: {e}")
        return "I encountered an error while generating a response. Please try again later or contact support shinde."

def coordinate_response(intent: str, query: str) -> str:
    """
    Coordinates the retrieval and response generation based on classified intent.
    """
    context, sources = "", []

    if intent == "RBI_REGULATION":
        context, sources = retrieve_context(query, settings.RBI_PINECONE_INDEX)
    elif intent == "NBFC_LENDING":
        context, sources = retrieve_context(query, settings.LENDING_PINECONE_INDEX)
    elif intent == "COMBINED":
        rbi_context, rbi_sources = retrieve_context(query, settings.RBI_PINECONE_INDEX)
        lending_context, lending_sources = retrieve_context(query, settings.LENDING_PINECONE_INDEX)
        context = f"RBI Regulations Context:\n{rbi_context}\n\nNBFC Lending Process Context:\n{lending_context}"
        sources = list(set(rbi_sources + lending_sources))
    else: # OTHER
        return "Thank you for your email. This query is outside the scope of our automated assistant. A team member will get back to you shortly. Please check back later."

    if not context:
        return "I could not find relevant information to answer your query. A team member will review your request. Please check back later."

    final_answer = generate_final_answer(query, context, sources)
    
    # Optional: Add a disclaimer
    final_answer += "\n\n---\nDisclaimer: This response is AI-generated and for informational purposes only. Please consult with a compliance officer for official guidance. This response does not constitute legal advice."
    
    return final_answer