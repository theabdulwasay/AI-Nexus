<img width="1903" height="840" alt="Screenshot 2026-02-10 224810" src="https://github.com/user-attachments/assets/91eb8fe5-8e7d-4ede-b09c-46b251c65295" />
<img width="1903" height="815" alt="Screenshot 2026-02-10 224648" src="https://github.com/user-attachments/assets/d0f46702-e64d-4267-b307-f49d2bbb044c" />
<img width="1916" height="842" alt="Screenshot 2026-02-10 224628" src="https://github.com/user-attachments/assets/7edfef67-c10d-4b1e-a42e-cd6943d7d240" />
<img width="1902" height="829" alt="Screenshot 2026-02-10 224618" src="https://github.com/user-attachments/assets/81a8a478-d77c-46c7-9676-6c2422e0d878" />
<img width="1521" height="562" alt="Screenshot 2026-02-10 224608" src="https://github.com/user-attachments/assets/100b103a-a9b5-47c2-b54d-1e7993a8b75a" />
<img width="1896" height="490" alt="Screenshot 2026-02-10 224559" src="https://github.com/user-attachments/assets/07d09f23-d437-4adc-a2e2-19bb46ba4025" />
<img width="1913" height="853" alt="Screenshot 2026-02-10 224542" src="https://github.com/user-attachments/assets/7fef5caa-5cd7-404b-8715-9303d8bfe264" />
<img width="1903" height="832" alt="Screenshot 2026-02-10 224530" src="https://github.com/user-attachments/assets/21fbea89-eee6-495c-a9c2-86128d07d6bf" />
<img width="1919" height="1005" alt="Screenshot 2026-02-10 224346" src="https://github.com/user-attachments/assets/edb7ffbb-7dee-4d7a-bad2-8157c3db712e" />

# 🌌 Nexus AI - Advanced Agentic Assistant (Phase 3.1.0)

Nexus AI is a powerful, modular, and extensible Agentic AI framework designed to orchestrate complex tasks through intelligent planning and tool execution. It features a modern Streamlit frontend and a robust FastAPI backend.

![Nexus AI Banner](https://img.shields.io/badge/Phase-3.1.0-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## 🚀 Overview

Nexus AI goes beyond simple chatbots by implementing a full **Plan-Execute-Verify** cycle. It can analyze user intent, break down complex requests into discrete steps, select the appropriate tools, and synthesize a final response based on execution results.

### Core Capabilities:
- **🧠 Advanced Planning**: Decomposes high-level goals into executable tool calls.
- **🛠️ Extensible Toolset**: Built-in support for Web Search, Data Analysis, System Inspection, and File Operations.
- **💾 Persistent Memory**: Long-term conversation history and context awareness using localized storage.
- **📚 Knowledge Base (KB)**: A dedicated system for storing and retrieving domain-specific knowledge.
- **📊 Real-time Analytics**: Built-in dashboard for monitoring agent performance and interaction history.

---

## 🏗️ Architecture

Nexus AI is built with a decoupled architecture to ensure scalability and ease of integration.

### Component Breakdown:
- **`AgenticAIAssistant` (`main.py`)**: The central orchestrator that coordinates between the Planner, Executor, and Memory.
- **`Planner` (`agent/planner.py`)**: A rule-based (expandable to LLM-based) engine that generates a structured execution plan.
- **`Executor` (`agent/executor.py`)**: Safely executes planned actions using a registry of registered tools.
- **`Memory` (`agent/memory.py`)**: Manages conversation flow and persistence in `memory.json`.
- **`KnowledgeBase` (`agent/knowledge_base.py`)**: Handles long-term information storage in `knowledge_base.json`.
- **`FastAPI Backend` (`api.py`)**: Exposes the agent's capabilities via a RESTful API.
- **`Streamlit Frontend` (`app.py`)**: A premium, high-fidelity UI for user interaction and system management.

---

## 🛠️ Tool System

Nexus AI comes equipped with several core tools:

| Tool | Action | Description |
| :--- | :--- | :--- |
| **Web Search** | `web_search` | Real-time information retrieval via DuckDuckGo API. |
| **Calculator** | `calculator` | Safe mathematical expression evaluation. |
| **System** | `system` | Retrieves OS info, time, and date. |
| **File Tool** | `file` | Securely lists and reads local files within the project root. |
| **Data Tool** | `data` | Performs CSV analysis and provides statistical summaries using Pandas. |

---

## 🚦 Getting Started

### Prerequisites
- Python 3.9+
- Virtual Environment (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-nexus.git
   cd ai-nexus
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project
You can run both the backend and frontend simultaneously using the provided batch script:
```bash
run_project.bat
```

Or start them manually:

**1. Start the API (Backend):**
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8001
```

**2. Start the UI (Frontend):**
```bash
python -m streamlit run app.py
```

---

## 🔌 API Documentation

Once the backend is running, you can access the interactive API docs at `http://localhost:8001/docs`.

### Key Endpoints:
- `POST /query`: Send a prompt to the agent and get a planned response.
- `GET /history`: Retrieve conversation logs.
- `GET /health`: Check system status.
- `POST /kb/learn`: Teach the agent new facts.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ by the Nexus AI Team.


