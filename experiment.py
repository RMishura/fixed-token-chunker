import argparse
import json

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from fixed_token_chunker import FixedTokenChunker
from ranges_and_metrics import union_ranges, precision, recall
from search import get_chunks_and_metadata


def load_data_and_embedding_model(data_path: str):
    with open(f"{data_path}/state_of_the_union.md", "r", encoding="utf-8") as file:
        corpus = file.read()

    questions = pd.read_csv(f"{data_path}/questions_df.csv")
    questions['references'] = questions['references'].apply(json.loads)

    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return corpus, questions, embedding_model


def embedding_fn(texts: list[str], embedding_model: SentenceTransformer) -> np.ndarray:
    return embedding_model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def calculate_metrics(row, embeddings, ranges, num_chunks_to_retrieve, embedding_model) -> tuple[float, float]:
    question = row["question"]
    question_emb = embedding_fn([question], embedding_model)[0]

    similarities = cosine_similarity([question_emb], embeddings)[0]
    top_chunk_indices = similarities.argsort()[-num_chunks_to_retrieve:][::-1]

    retrieved_ranges = [ranges[i] for i in top_chunk_indices]
    reference_ranges = [(x["start_index"], x["end_index"]) for x in row["references"]]

    retrieved_ranges = union_ranges(retrieved_ranges)
    reference_ranges = union_ranges(reference_ranges)

    precision_score = precision(retrieved_ranges, reference_ranges)
    recall_score = recall(retrieved_ranges, reference_ranges)
    return precision_score, recall_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("chunk_sz", type=int)
    parser.add_argument("chunk_num", type=int)
    args = parser.parse_args()

    print("Loading data and embedding model...")
    corpus, questions, embedding_model = load_data_and_embedding_model("data")

    fixed_token_chunker = FixedTokenChunker(
        chunk_size=args.chunk_sz,
        chunk_overlap=10,
        encoding_name="cl100k_base"
    )

    chunks, ranges = get_chunks_and_metadata(fixed_token_chunker, corpus)
    embeddings = embedding_fn(chunks, embedding_model)

    print(f"Calculating metrics for number of retrieved chunks={args.chunk_num}, chunk_size={args.chunk_sz}, chunk_overlap=10...")

    precision_scores = []
    recall_scores = []

    for _, row in questions.iterrows():
        if row["corpus_id"] != "state_of_the_union":
            continue
        precision_scr, recall_scr = calculate_metrics(
            row,
            embeddings,
            ranges,
            args.chunk_num,
            embedding_model,
        )
        precision_scores.append(precision_scr)
        recall_scores.append(recall_scr)

    print("Average precision:", np.mean(precision_scores))
    print("Average recall:", np.mean(recall_scores))