# fixed-token-chunker
# Chunking Evaluation on the "State of the Union" Corpus

This repository contains an implementation of a pipeline for splitting the **"state_of_union"** corpus into chunks of different sizes and evaluating this chunking using various numbers of retrieved chunks. The embedding model used is **all-MiniLM-L6-v2**.

## File Structure

1. **`fixed_token_chunker.py`** and **`base_chunker.py`** are fully copied from:  
   [brandonstarxel/chunking_evaluation](https://github.com/brandonstarxel/chunking_evaluation)

2. **`ranges_and_metrics.py`**:
   - Contains copied implementations of:  
     `sum_of_ranges()`, `union_ranges()`, `intersect_two_ranges()`
   - Also includes custom implementations:
     - `intersect_two_lists_of_ranges()` — used for metric calculation
     - `precision()` and `recall()` metrics

3. **`search.py`**:
   - Includes copied functions from the same repository for locating chunk positions within the corpus

4. **`experiment.py`**:
   - Main script that runs the evaluation
   - Usage:

     ```bash
     python experiment.py <chunk_size> <num_chunks>
     ```

     Example:
     ```bash
     python experiment.py 200 5
     ```
     ```
     Loading data and embedding model...
     Calculating metrics for number of retrieved chunks=5, chunk_size=200, chunk_overlap=10...
     Average precision: 0.03982913308934815
     Average recall: 0.9518411836692183
     ```
---

## Table

| Chunk Size | Retrieved Chunks = 5        | Retrieved Chunks = 10       |
|------------|-----------------------------|------------------------------|
| 200        | Precision: 0.039, Recall: 0.95 | Precision: 0.020, Recall: 0.99 |
| 400        | Precision: 0.016, Recall: 0.84 | Precision: 0.009, Recall: 0.94 |

---

## Interpretation

The table shows that with the given parameter settings, recall values are high, which indicates that the reference excerpts are almost completely covered by the retrieved chunks. At the same time, precision values are low, suggesting that the total length of the retrieved chunks is significantly greater than the length of the excerpts. It is also evident that increasing the chunk size leads to a drop in precision by more than half. This can be explained by the fact that the total length of the chunks covering the excerpts approximately doubles. Moreover, when moving from a chunk size of 200 to 400, recall also decreases, which may indicate that the embedding model struggles to effectively process overly large chunks.
