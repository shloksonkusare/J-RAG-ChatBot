import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.embeddings.embedder import Embedder
from src.vector_db.chroma_client import ChromaClient

# 1. User query
query = "Explain the difference between は and が"

# 2. Embed the query
embedder = Embedder()
query_embedding = embedder.embed_texts([query])[0]

# 3. Search vector DB
db = ChromaClient()
results = db.similarity_search(query_embedding, top_k=5)

# 4. Print results
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("\n---")
    print(doc)
    print(meta)
