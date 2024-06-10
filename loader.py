from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from reddit_loader import RedditLoader
import validators
import os

custom_loader = {
    'reddit': RedditLoader
}


def get_loader(doc, source=None):
    """
    returns loader object for document.
    :param doc: file path or url
    :param source: this is required for custom loader.
    :return: loader object
    """
    if source:
        return custom_loader[source]

    if validators.url(doc):
        return WebBaseLoader(doc)

    if os.path.isfile(doc):
        extn = doc.split(".")[-1].lower()
        if extn == 'pdf':
            return PyPDFLoader(doc)
    raise Exception("not implemented")