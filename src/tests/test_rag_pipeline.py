from src.rag.rag_pipeline import RAGPipeline

rag = RAGPipeline()

query = "私は行きますか？"
answer = rag.run(query)

print("\nFinal Answer:\n")
print(answer)
