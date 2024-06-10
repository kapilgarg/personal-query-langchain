from collections import deque
import json
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.docstore.document import Document
import ntpath


class RedditLoader(BaseLoader):
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        data_json = json.loads(data)
        queue = deque(data_json)
        output = []
        subreddit = ""
        source = ntpath.basename(self.file_path)
        while queue:
            obj = queue.popleft()
            if isinstance(obj, dict):
                for key in obj:
                    if key == "subreddit":
                        subreddit = obj[key]
                    if key == 'body':
                        # output.append(Document(page_content=obj[key], metadata=dict(subreddit=subreddit, source=source)))
                        output.append(obj[key])
                    else:
                        if obj[key] and isinstance(obj[key], list):
                            for item in obj[key]:
                                queue.append(item)
                        elif obj[key] and isinstance(obj[key], dict):
                            queue.append(obj[key])
            elif obj and isinstance(obj, list):
                for item in obj:
                    queue.append(item)
        output = "\n".join(output)
        return [Document(page_content=output, metadata=dict(subreddit=subreddit, source=source))]
