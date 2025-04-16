import os
from sentence_transformers import SentenceTransformer, util
import torch

# Combine lines into multi-line chunks
def chunk_lines(lines, window_size=3):
    chunks = []
    indices = []
    for i in range(len(lines) - window_size + 1):
        chunk = lines[i:i + window_size]
        chunks.append(" ".join(chunk))
        indices.append((i, i + window_size))  # start, end index
    return chunks, indices

# Read text files and prepare chunks
def read_text_files_from_directory(directory_path, chunk_size=3):
    chapters = []
    original_lines = {}  # for retrieving original text

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            chapter_name = os.path.splitext(filename)[0]
            filepath = os.path.join(directory_path, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    lines = f.readlines()

            clean_lines = [line.strip() for line in lines if line.strip()]
            original_lines[chapter_name] = clean_lines
            line_chunks, chunk_indices = chunk_lines(clean_lines, window_size=chunk_size)
            chapters.append((chapter_name, line_chunks, chunk_indices))

    return chapters, original_lines

# Encode all chapter chunks
def encode_chapters(model, chapters):
    encoded_chapters = []
    for chapter_name, chunks, indices in chapters:
        embeddings = model.encode(chunks, convert_to_tensor=True)
        encoded_chapters.append((chapter_name, chunks, indices, embeddings))
    return encoded_chapters

# Find best match and highlight best line
def find_best_match(query, encoded_chapters, original_lines, model):
    query_embedding = model.encode(query, convert_to_tensor=True)

    best_score = 0
    best_chunk = ""
    best_line = ""
    best_chapter = ""
    best_lines_range = (0, 0)

    for chapter_name, chunks, indices, embeddings in encoded_chapters:
        cosine_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
        best_score_idx = torch.argmax(cosine_scores).item()
        score = cosine_scores[best_score_idx].item()

        if score > best_score:
            best_score = score
            best_chunk = chunks[best_score_idx]
            best_lines_range = indices[best_score_idx]
            best_chapter = chapter_name

    # Now, find best matching individual line within the best chunk
    start, end = best_lines_range
    lines_in_chunk = original_lines[best_chapter][start:end]
    line_embeddings = model.encode(lines_in_chunk, convert_to_tensor=True)
    line_scores = util.pytorch_cos_sim(query_embedding, line_embeddings)[0]
    best_line_idx = torch.argmax(line_scores).item()
    best_line = lines_in_chunk[best_line_idx]

    return lines_in_chunk, best_line, best_chapter, best_score

# Main
if __name__ == "__main__":
    directory_path = "chapters"
    query = input("Enter your query: ")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    chapters, original_lines = read_text_files_from_directory(directory_path, chunk_size=3)
    encoded_chapters = encode_chapters(model, chapters)

    lines_in_chunk, best_line, best_chapter, score = find_best_match(query, encoded_chapters, original_lines, model)

    print(f"\n📖 Best match from: {best_chapter}")
    print("🧩 Context:")
    for line in lines_in_chunk:
        if line == best_line:
            print(f">>> {line}  <<<")  # Highlight the best line
        else:
            print(line)
    print(f"\n🔍 Similarity: {score * 100:.2f}%")








'''
import os
from sentence_transformers import SentenceTransformer, util
import torch

# Read chapter text files
def read_text_files_from_directory(directory_path):
    chapters = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            chapter_name = os.path.splitext(filename)[0]
            filepath = os.path.join(directory_path, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    lines = f.readlines()

            content_lines = [line.strip() for line in lines if line.strip()]
            chapters.append((chapter_name, content_lines))

    return chapters

# Precompute embeddings for all chapter lines
def encode_chapters(model, chapters):
    encoded_chapters = []
    for chapter_name, lines in chapters:
        embeddings = model.encode(lines, convert_to_tensor=True)
        encoded_chapters.append((chapter_name, lines, embeddings))
    return encoded_chapters

# Find best match for query
def find_best_match(query, encoded_chapters, model):
    query_embedding = model.encode(query, convert_to_tensor=True)

    best_line = ""
    best_score = 0
    best_chapter = ""

    for chapter_name, lines, embeddings in encoded_chapters:
        cosine_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
        best_score_idx = torch.argmax(cosine_scores).item()
        score = cosine_scores[best_score_idx].item()

        if score > best_score:
            best_score = score
            best_line = lines[best_score_idx]
            best_chapter = chapter_name

    return best_line, best_chapter, best_score

# Main execution
if __name__ == "__main__":
    directory_path = "chapters"
    query = input("Enter your query: ")

    # Always use CPU
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Step 1: Load and encode all chapters only once
    chapters = read_text_files_from_directory(directory_path)
    encoded_chapters = encode_chapters(model, chapters)

    # Step 2: Process the query
    best_line, best_chapter, score = find_best_match(query, encoded_chapters, model)

    # Step 3: Display result
    print(f"Best match from {best_chapter}:\n{best_line}\nSimilarity: {score * 100:.2f}%")

'''
