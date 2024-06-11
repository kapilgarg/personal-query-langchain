# Personal-Query-Langchain
Create a store of  your artifacts (pdf, blogs, text files) and query it like chatGpt

## Step 01 : Install requirements
```
pip install -r requirements.txt
```

## Step 02 : Set your open AI Key
```
export OPENAI_API_KEY=<your_key_here>
```

## Step 03 : Ingest your data 
```
from ingest import ingest
# Ingest from a directory
paper_dir = r"data\pdf"
paper_paths = [os.path.join(os.path.abspath(paper_dir), paper) for paper in os.listdir(paper_dir)]
ingest(paper_paths)

# ingest from a blog
ingest("https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c")

# ingest from a file
ingest(r"data\reddit\most_influential_books_you_ever_read.json", source='reddit')
```

## Step 04 : Query
Run ```app.py```

## Example
<img src="/examples/example (2).gif">
<img src="/examples/example (1).gif">






