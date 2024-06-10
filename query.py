from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.vectorstores.base import VectorStoreRetriever

embedding = OpenAIEmbeddings()


def get_vector_store():
    vectorstore = Chroma(
        persist_directory='docs/chroma/',
        embedding_function=embedding
    )
    return vectorstore


def load_retriever():
    vectorstore = get_vector_store()
    return VectorStoreRetriever(vectorstore=vectorstore)


retriever = load_retriever()
llm = ChatOpenAI()

system_prompt = (
    "You are provided system design papers and technical blogs.provide the response as per query. if you don't "
    "know the ans, don't make it up. Just say tha you don't know."
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
_chain = create_retrieval_chain(retriever, question_answer_chain)


def process_response(response):
    sources = set()
    for context in response['context']:
        sources.add(context.dict()['metadata']['source'])
    return sources, response['answer']


def invoke(query):
    response = _chain.invoke({"input": query})
    metadata, ans = process_response(response)
    return metadata, ans

# coll = vectordb.get()  # dict_keys(['ids', 'embeddings', 'documents', 'metadatas'])
#
# ids_to_del = []
#
# for idx in range(len(coll['ids'])):
#
#     id = coll['ids'][idx]
#     metadata = coll['metadatas'][idx]
#
#     if 'subreddit' in metadata and metadata['subreddit'] == "Entrepreneur":
#         ids_to_del.append(id)
#
# vectordb._collection.delete(ids_to_del)
