# ⚛️ Physics-Informed Research Agent

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange.svg)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)

A **Multi-Modal RAG (Retrieval-Augmented Generation) System** engineered to handle the mathematical density of scientific literature.

Standard LLM pipelines can be unreliable when faced with dense physics notation or long technical context. This project combines document retrieval with symbolic tooling so the agent can **read** scientific papers, **extract** relevant context, and route supported mathematical expressions to a deterministic solver.

## 🚀 Key Features

* **Physics-Aware Ingestion Pipeline:** Custom ETL logic (`SectionTracker`, `MathClassifier`) that processes mathematical PDFs, preserving equation integrity and logical document structure (e.g., Introduction, Methodology) during chunking.
* **Autonomous Tool-Use Agent:** A "Router-Retriever-Solver" architecture. The agent analyzes a user query and decides whether to *search* the vector database for conceptual answers or use the math tool for a supported calculation.
* **Symbolic Math Engine:** Integrates `SymPy` for deterministic symbolic computation on supported expressions, reducing reliance on LLM-generated arithmetic. Solver correctness still depends on the expression being parsed and represented correctly.
* **Citation-Backed Responses:** Conceptual answers are grounded in retrieved PDF chunks, providing explicit traceability to source context.

## 🛠️ Tech Stack

* **LLM & Orchestration:** Google Gemini 2.5 Flash, Native Function Calling
* **Retrieval (RAG):** FAISS (Facebook AI Similarity Search), Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Data Processing:** `pdf2image`, NLTK, sliding-window semantic chunking
* **Math Engine:** SymPy, LaTeX parsing transformations
* **Backend & Testing:** Python 3.13, PyTest
* **Frontend:** Streamlit

## 🧠 System Architecture

The agent operates across three specialized layers:

1. **Ingestion Layer:** Converts PDFs to raw text, applies noise-reduction filters, and splits text using context-preserving overlapping windows. Chunks are enriched with metadata regarding their source section and mathematical density.
2. **Retrieval Layer:** Projects text into a 384-dimensional dense vector space. User queries perform a k-Nearest Neighbors (k-NN) search against the FAISS index to retrieve the most semantically relevant chunks.
3. **Agentic Layer:** The core routing layer dynamically chooses between:
   * *Conceptual Query* → `SearchTool` → retrieved context → grounded response.
   * *Calculation Query* → `MathTool` → symbolic computation → returned roots/values when supported.

## 💻 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MeghnaB12/physics-research-agent.git
   cd physics-research-agent
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Environment Variables**

   Create a `.env` file in the root directory and add your Google Gemini API key:

   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## 🏃‍♂️ How to Run

1. **Ingest Data (Build the Knowledge Base)**

   ```bash
   python backend/app/main.py
   ```

2. **Build the Vector Index**

   ```bash
   python backend/app/retrieval/build_index.py
   ```

3. **Launch the Application**

   ```bash
   streamlit run frontend/app.py
   ```

## 🧪 Testing

The test suite covers ingestion logic, vector retrieval, and tool execution.

```bash
pytest backend/tests
```
