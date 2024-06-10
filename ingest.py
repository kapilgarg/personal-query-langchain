import os
import logging
import loader
import openai
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

openai.api_key = os.environ['OPENAI_API_KEY']


def ingest(docs, source=None):
    if not isinstance(docs, list):
        docs = [docs]

    loaders = [loader.get_loader(doc, source) for doc in docs]

    loaded_docs = []
    for doc_loader in loaders:
        loaded_docs.extend(doc_loader.load())

    logger.info('splitting documents')
    splits = RecursiveCharacterTextSplitter().split_documents(loaded_docs)

    embedding = OpenAIEmbeddings()
    persist_directory = 'docs/chroma/'

    Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )


if __name__ == '__main__':
    paper_dir = r"data\pdf"
    paper_paths = [os.path.join(os.path.abspath(paper_dir), paper) for paper in os.listdir(paper_dir)]
    ingest(paper_paths)

    ingest(r"data\reddit\most_influential_books_you_ever_read.json", source='reddit')
    ingest("https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c")

