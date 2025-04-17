
**Storybook AI - Variable and Function Explanation Document**

This document provides a detailed explanation of key variables, inputs, and their purposes within the Storybook AI chatbot script for the Harry Potter series.

---

### 1. **query**
- **Type:** `str`
- **Purpose:** The question or sentence the user inputs asking about the Harry Potter books.
- **Used In:** `find_best_matches()`, `format_response()`, `format_structured_response()`, `generate_analysis()`
- **Function:** It acts as the main search string that gets compared with chunks of text from the books to find the most relevant match using sentence embeddings.

### 2. **user_input**
- **Type:** `str`
- **Purpose:** The actual input entered by the user in the command-line interface.
- **Used In:** `main()`
- **Function:** It controls the flow of interaction. It is parsed to detect commands like 'exit' or mode change or sent to the AI for answering.

### 3. **matches**
- **Type:** `list` of `dict`
- **Purpose:** Top-matching chunks from the Harry Potter books based on similarity with the query.
- **Used In:** `format_response()`, `format_freeform_response()`, `format_structured_response()`
- **Function:** Contains results like chapter name, context, best-matching line, and similarity score.

### 4. **chapters**
- **Type:** `list` of tuples
- **Purpose:** Holds processed text chunks from each chapter with their indices.
- **Used In:** `read_text_files_from_directory()`
- **Function:** Stores chapter name, list of text chunks, and the corresponding line index ranges.

### 5. **original_lines**
- **Type:** `dict`
- **Purpose:** Stores original lines from each chapter.
- **Used In:** `read_text_files_from_directory()`, `find_best_matches()`
- **Function:** Allows lookup of the full context from the original files using the indices.

### 6. **encoded_chapters**
- **Type:** `list`
- **Purpose:** Encoded embeddings of chapter chunks using the SentenceTransformer model.
- **Used In:** `find_best_matches()`
- **Function:** Used to compute cosine similarity with the query embedding to find relevant sections.

### 7. **response_mode**
- **Type:** `str`
- **Purpose:** Determines the response format: "freeform" or "structured"
- **Used In:** `format_response()`
- **Function:** Decides whether the AI gives a conversational or a formatted/structured answer.

### 8. **templates**
- **Type:** `dict`
- **Purpose:** Predefined response formats for different types of questions.
- **Used In:** `format_response()`, `format_freeform_response()`, `format_structured_response()`
- **Function:** Makes AI responses more natural and informative.

### 9. **model**
- **Type:** `SentenceTransformer`
- **Purpose:** Pretrained transformer model used to generate sentence embeddings.
- **Used In:** `encode_chapters()`, `find_best_matches()`
- **Function:** Converts text chunks and queries into numerical representations for similarity comparison.

---

### Function Roles Summary

- **chunk_lines():** Breaks chapter text into overlapping chunks for better semantic context.
- **read_text_files_from_directory():** Loads and prepares chapter text from `.txt` files.
- **encode_chapters():** Encodes chunks using the model.
- **find_best_matches():** Finds top-matching text segments for the query.
- **load_response_templates():** Loads or creates response templates.
- **format_response():** Picks the response format and builds the output.
- **summarize_context():** Cleans and compresses matched text to concise context.
- **generate_analysis():** Adds analytical commentary in structured mode.

---

### Main Class: `StorybookAI`

- **__init__():** Initializes the model, reads data, encodes it, and loads templates.
- **set_response_mode():** Sets either freeform or structured response format.
- **answer():** Accepts a query and returns the AI's formatted answer.

### User Interaction Flow

- The `main()` function handles CLI interaction.
- Prompts user to input queries or change mode.
- Sends input to the `StorybookAI` class.
- Displays a formatted response.

---
