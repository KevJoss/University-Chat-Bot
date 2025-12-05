# Yachay AI Assistant 🎓

**Yachay AI Assistant** is a Retrieval-Augmented Generation (RAG) agent designed to assist students and staff at Yachay Tech University. It provides instant, accurate answers regarding university services, administrative procedures, campus locations, and health resources by retrieving information from a curated knowledge base.

The system utilizes **LangGraph** for agent orchestration, allowing it to intelligently route user queries between a database search (for factual university info) and a general chat mode (for greetings and small talk).

---

## 🚀 Key Features

* **RAG Architecture:** Retrieves specific data from university documents (CSV) to answer questions about scholarships, medical attention, libraries, and more.
* **Intelligent Routing:** Uses a conditional **Router Node** to classify user intent.
    * *SEARCH Mode:* Queries the vector database for factual accuracy.
    * *CHAT Mode:* Handles casual conversation without wasting retrieval resources.
* **Local LLM Privacy:** Built on **Ollama** using `gemma3:4b`, running locally for data privacy and zero cost.
* **Vector Database:** Uses **ChromaDB** for efficient semantic similarity search.
* **Interactive UI:** A clean, chat-based web interface built with **Streamlit**.

---

## 🛠️ Architecture

The project follows a graph-based workflow using **LangGraph**:

1.  **Router:** Analyzes input -> Decides `SEARCH` vs `CHAT`.
2.  **Search Node:** If `SEARCH`, queries the ChromaDB vector store.
3.  **Generate Node:** Synthesizes the retrieved context into a helpful Spanish response.
4.  **Chat Node:** Handles general interaction if no search is needed.

![LangGraph Workflow](images/graph.png)

---

## 📦 Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.10+**
2.  **Ollama** (Running locally)
    * Download from [ollama.com](https://ollama.com)
    * Pull the required models via terminal:
        ```bash
        ollama pull gemma3:4b
        ollama pull nomic-embed-text
        ```

---

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/yachay-ai-assistant.git]
    cd yachay-ai-assistant
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, install the core libs manually)*:
    ```bash
    pip install streamlit langchain langchain-community langchain-ollama langchain-chroma langgraph pandas
    ```

---

## ▶️ How to Run the Application

The application consists of a backend logic graph and a Streamlit frontend. To launch the user interface:

1.  **Ensure Ollama is running** in the background.
2.  **Run the Streamlit app** from the project root:

    ```bash
    streamlit run app.py
    ```

3.  The application will open automatically in your web browser at `http://localhost:8501`.

### 🧪 Testing the Logic (Optional)
If you want to test the decision graph logic without the UI, you can run the graph script directly:
```bash
python src/graph.py
```

## 📁 Project Structure

```
├── chroma_db/         # Persistent Vector Database storage
├── data/
│   └── Grid Public.csv    # Raw data source (University services)
├── src/
│   ├── data_loader.py     # Script to ingest CSV and build ChromaDB
│   ├── graph.py           # Main LangGraph logic (Nodes & Edges)
│   ├── prompts.py         # Prompt templates for the LLM
│   ├── tools.py           # Search tools definition
├── app.py             # Streamlit Frontend Entry Point
├── requirements.txt   # Project dependencies
```

## 💡 Usage Examples

Once the app is running, try asking:

- **General:** "Hola, ¿cómo estás?" (Routes to Chat)
- **Specific:** "¿Dónde queda bienestar estudiantil?" (Routes to Search)
- **Procedures:** "¿Cómo aplico a una beca?" (Routes to Search)
- **Contacts:** "Dame el correo de soporte académico" (Routes to Search)

---

> **Note:**  
> **Author**: Kevin Sánchez **Course**: Intelligent Agents - Yachay Tech