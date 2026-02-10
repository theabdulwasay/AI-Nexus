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
