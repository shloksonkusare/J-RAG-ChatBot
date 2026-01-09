from src.rag.rag_pipeline import RAGPipeline

rag = RAGPipeline()

query = "What is the Japanese Alphabet for A？"
answer = rag.run(query)

print("\nFinal Answer:\n")
print(answer)
