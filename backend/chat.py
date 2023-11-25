from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vertexai
from langchain.llms import VertexAI
import os
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.embeddings import VertexAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'smart-portfolio-401206-5657d2c792f3.json'
# GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
vertexai.init(project="smart-portfolio-401206", location="us-central1")
app = FastAPI()
template = """

You are a helpful cricket coach assistant that assists in strategies and other decisions of players based on the context. 
You should only provide answers to questions related to cricket, and if any irrelevant questions unrelated to cricket are asked,
 clearly state that you are only responsible for assisting with cricket-related decisions or information. 
 Additionally, you should only provide answers in the English language.
 You should not show chat history in answer or direct context as it is , think before you give result it should be always in explanatory format
------
<ctx>
{context}
</ct
------

{question}
Answer:
"""
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)
url = os.environ.get('url')
username = os.environ.get('username')
password = os.environ.get('password')
neo4j_vector = Neo4jVector.from_existing_index(
    VertexAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    index_name="cric-gpt",
    text_node_property="info",  # Need to define if it is not default
)
qa = RetrievalQA.from_chain_type(
    llm=VertexAI(temperature=0.2),
    chain_type='stuff',
    retriever=neo4j_vector.as_retriever(search_kwargs={'k': 6}),
    chain_type_kwargs={
        "prompt": prompt,
    #     "memory": ConversationBufferWindowMemory(
    #         k=2,
    #         memory_key="history",
    #         input_key="question"),
    # 
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

class ChatInput(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat")
async def chat_with_model(chat_input: ChatInput):
    try:
        response=qa.run(chat_input.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chatbot: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
