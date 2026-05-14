# Chatbot-RAG-PostgreSQL
Local Chatbot implementing RAG (Retrieval-Augmented Generation) and PostgreSQL database connection using:

- LLM: `llama3` via `Ollama`
- Embeddings: `mxbai-embed-large` via Ollama
- Vector store: `Qdrant` (before `FAISS`)
- Conversational memory in JSON file

Requirements: 12 GB RAM memory at least, no GPU needed.

## 🌎 Repository Structure
```bash
Chatbot-RAG-PostgreSQL/
├── main.py
├── .gitignore
├── env/                    # Virtual enviroment (not provided)
└── requirements.txt
└── src                     # Contains all needed files (Python package)
    └── __init__.py         # Specifies that folder 'src' is a Python package
    └── build_index.py      # To convert data to emdeddings
    └── config.py           # Set your configuration variables here
    └── document_loader.py  # To transform PDF to text
    └── memory.py           # To save the conversation into a JSON file
    └── ollama_client.py    # To launch the model
    └── rag.py              # RAG configuration. SYSTEM_INSTRUCTIONS are here
    └── text_splitter.py    # To split the text into many chunks
    └── vector_store.py     # To manage the FAISS indexes
└── data
    └── docs                # Paste your documents `.txt`, `.md` or `.pdf` here
    └── indexes/main        # To save the vector DB indexes
    └── memory              # JSON file to save the conversation
```

## 🚀 How to run locally
1. Clone this repository:
```bash
git clone https://github.com/departamentoIA/Chatbot-RAG-PostgreSQL.git
```
2. Set virtual environment and install dependencies.

For Windows:
```bash
python -m venv env
env/Scripts/activate
pip install -r requirements.txt
```
For Linux:
```bash
python -m venv env && source env/bin/activate && pip install -r requirements.txt
```
3. Download and install Ollama from: https://ollama.com/download.
4. Download the model and the embedder. In a terminal run:
```bash
ollama pull llama3.2:1b
ollama pull mxbai-embed-large
```
5. Paste your documents `.txt`, `.md` or `.pdf` in "./data/docs".
6. Build the FAISS indexes. In the root of this project, run:
```bash
python -m src.build_index --docs-dir data/docs --index-dir data/indexes/main
```
The input arguments 'docs-dir' and 'index-dir' specify the documents source path and the vector DB indexes, respectively.


7. Run "main.py" with the following command:
```bash
python -m main --index-dir data/indexes/main
```
The conversational memory is saved automatically in "./data/memory/conversation.json", which is used as context with the fragments recovered from FAISS to answer the questions.

In order to delete the previous conversation, run:
```bash
python -m src.chat --index-dir data/indexes/main --clear-memory
```
or delete manually the file "data/memory/conversation.json".
