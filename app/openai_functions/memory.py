from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores.chroma import Document
import json

class Memory:
    def __init__(self, chroma_db: Chroma):
        """
        Initialize the Memory class with a Chroma database connection.
        """
        self.chroma_db = chroma_db
        
    def store(self, content):
        """
        Store a new document in the Chroma database.
        """
        # Create a Document object
        doc = Document(page_content=content)
        # Generate embedding for the document
        # doc_embedding = self.embedding_fn.embed_query([content])

        # Add document and its embedding to Chroma
        ids = self.chroma_db.add_documents(list([doc]))
        
        #save markdown file with 'content' under name ids[0].md 
        self.save_markdown_file(content, ids[0])

    def save_markdown_file(self, content, file_id):
        filename = f"./app/openai_functions/memories/{file_id}.md"
        with open(filename, 'w') as file:
            file.write(content)

    def search(self, search_string, k=5):
        """
        Search the Chroma database for similar documents to the provided string.
        Returns a list of document IDs.
        """
        # Generate embedding for the search string
        # search_embed = self.embedding_fn.embed_query(search_string)

        # Search Chroma for similar documents
        results = self.chroma_db.similarity_search(search_string, k=k)

        # Return document IDs of results
        return results


chroma_db = Chroma(
    collection_name='bi_dev_memory',
     embedding_function=OpenAIEmbeddings(),
     persist_directory='./app/openai_functions/memories/db'
)  # Create the Chroma database
memory = Memory(chroma_db)

def store_memory(markdown):
    memory.store(markdown)
    return json.dumps({"success": "true"})

def search_memory(query):
    docs = memory.search(query)
    return json.dumps([f"### Start of Knowledge Article\n{doc.page_content}\n### End of Knowledge Article" for doc in docs])