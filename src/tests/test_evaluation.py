from src.rag.rag_pipeline import RAGPipeline
from src.evaluation.hallucination_check import hallucination_check
from src.evaluation.quality_checks import (
    retrieval_type_check,
    response_structure_check
)


def run_evaluation():
    rag = RAGPipeline()

    query = "は と が の違いは何ですか？"

    # Run pipeline
    results = rag.db.similarity_search(
        rag.embedder.embed_texts([query])[0],
        where={"type": "grammar"}
    )

    contexts = results["documents"][0]
    metadatas = results["metadatas"][0]

    answer = rag.run(query)

    print("\n--- ANSWER ---\n")
    print(answer)

    print("\n--- EVALUATION RESULTS ---")

    print("✔ Structure valid:",
          response_structure_check(answer))

    print("✔ Retrieval type valid:",
          retrieval_type_check(metadatas, expected_type="grammar"))

    print("✔ Hallucination check passed:",
          hallucination_check(answer, contexts))


if __name__ == "__main__":
    run_evaluation()
