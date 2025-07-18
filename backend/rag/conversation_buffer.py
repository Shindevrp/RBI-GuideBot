from collections import deque
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from creds import openai_key, PINECONE_API_KEY, index_name

class ConversationSummaryBufferMemory:
    def __init__(self, openai_key, index_name, pinecone_api_key, text_key, buffer_size=5):
        self.openai_key = openai_key
        self.index_name = index_name
        self.pinecone_api_key = pinecone_api_key
        self.text_key = text_key
        self.buffer_size = buffer_size
        self.conversation_buffer = deque(maxlen=self.buffer_size)

    def _retrieve_metadata(self, question):
        embeddings = OpenAIEmbeddings(api_key=self.openai_key, model="text-embedding-ada-002")
        query_embedding = embeddings.embed_query(question)
        vectorstore = PineconeVectorStore(index_name=self.index_name, embedding=embeddings,
                                          pinecone_api_key=self.pinecone_api_key, text_key=self.text_key)
        vector_response = vectorstore.similarity_search_by_vector_with_score(embedding=query_embedding, k=3)
        meta_data_list = [i[0].page_content for i in vector_response]
        return meta_data_list

    def _generate_answer(self, llm, question, context_data):
        template = self._prompt_template(context_data=context_data)
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = question
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        response = llm.invoke(
            chat_prompt.format_prompt(context_data=context_data, question=question).to_messages())
        return response.content

    def _prompt_template(self, context_data):
        return (
            '''consider the provided context data and question from the user and answer accordingly.
            context data : ''' + str(context_data)
        )

    def process_conversation(self, question):
        metadata = self._retrieve_metadata(question)
        chat = ChatOpenAI(temperature=0, openai_api_key=self.openai_key, model="gpt-3.5-turbo-0125")
        answer = self._generate_answer(llm=chat, question=question, context_data=metadata)
        self.conversation_buffer.append((question, answer))
        return answer

    def get_recent_conversations(self):
        return self.conversation_buffer

if __name__ == "__main__":
    conversation_summary_buffer_memory = ConversationSummaryBufferMemory(openai_key=openai_key,
                                                                         index_name=index_name,
                                                                         pinecone_api_key=PINECONE_API_KEY,
                                                                         text_key="chunk")

    while True:
        user_question = input("Enter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break
        if user_question.lower() == 'recent':
            recent_conversations = conversation_summary_buffer_memory.get_recent_conversations()
            print("\nRecent Conversations:")
            for idx, (question, response) in enumerate(recent_conversations, 1):
                print(f"{idx}. Question:", question)
                print("   Response:", response)
            continue
        response = conversation_summary_buffer_memory.process_conversation(question=user_question)
        print("Response:", response)
