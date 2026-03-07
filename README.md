# ⚛️ Physics-Informed Research Agent

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-orange.svg)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)

A **Multi-Modal RAG (Retrieval-Augmented Generation) System** engineered to handle the mathematical density of scientific literature. 

Standard LLM pipelines often hallucinate when faced with complex physics equations or deep technical context. This project bridges the gap between data science and the physical sciences by deploying an autonomous agent that can **read** scientific papers, **extract** context, and **deterministically solve** embedded mathematical equations.

## 🚀 Key Features

* **Physics-Aware Ingestion Pipeline:** Custom ETL logic (`SectionTracker`, `MathClassifier`) that processes mathematical PDFs, preserving equation integrity and logical document structure (e.g., Introduction, Methodology) during chunking.
* **Autonomous Tool-Use Agent:** A "Router-Retriever-Solver" architecture. The agent intelligently analyzes a user query and decides whether to *search* the vector database for conceptual answers or *write and execute code* to solve a math problem.
* **Symbolic Math Engine:** Integrates `SymPy` as a deterministic tool. When the agent identifies an equation in the text, it offloads the calculation to the symbolic solver, guaranteeing 100% arithmetic precision and eliminating LLM hallucination.
* **Citation-Backed Responses:** Conceptual answers are strictly grounded in retrieved PDF chunks, providing explicit traceability (e.g., `[Result 1, 3]`).

## 🛠️ Tech Stack

* **LLM & Orchestration:** Google Gemini 1.5 Flash, Native Function Calling
* **Retrieval (RAG):** FAISS (Facebook AI Similarity Search), Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Data Processing:** `pdf2image`, NLTK, sliding-window semantic chunking
* **Math Engine:** SymPy, LaTeX parsing transformations
* **Backend & Testing:** Python 3.13, PyTest
* **Frontend:** Streamlit

## 🧠 System Architecture

The agent operates across three specialized layers:

1. **Ingestion Layer:** Converts PDFs to raw text, applies noise-reduction filters, and splits text using context-preserving overlapping windows. Chunks are enriched with metadata regarding their source section and mathematical density.
2. **Retrieval Layer:** Projects text into a 384-dimensional dense vector space. User queries perform a k-Nearest Neighbors (k-NN) search against the FAISS index to retrieve the most semantically relevant chunks.
3. **Agentic Layer:** The core reasoning engine. It dynamically routes queries:
   * *Conceptual Query* $\rightarrow$ Triggers `SearchTool` $\rightarrow$ Synthesizes retrieved context.
   * *Calculation Query* $\rightarrow$ Triggers `MathTool` $\rightarrow$ Computes symbolic solution $\rightarrow$ Returns exact roots/values.

## 💻 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/MeghnaB12/physics-research-agent.git](https://github.com/MeghnaB12/physics-research-agent.git)
   cd physics-research-agent
   ~~~

   Install Dependencies
Bash
pip install -r requirements.txt
Set up Environment Variables
Create a .env file in the root directory and add your Google Gemini API key:
Bash
GOOGLE_API_KEY=your_actual_api_key_here
🏃‍♂️ How to Run
1. Ingest Data (Build the Knowledge Base)
Processes the raw PDF, cleans the text, and chunks it with rich metadata.

Bash
PYTHONPATH=backend/app python backend/app/main.py
2. Build the Vector Index
Embeds the chunks and constructs the FAISS index for high-speed retrieval.

Bash
PYTHONPATH=backend/app python backend/app/retrieval/build_index.py
3. Launch the Application
Starts the interactive Streamlit chat interface.

Bash
PYTHONPATH=backend/app streamlit run frontend/app.py
🧪 Testing
The system includes a robust test suite covering the ingestion logic, vector retrieval, and tool execution.

Bash
PYTHONPATH=backend/app pytest backend/tests
