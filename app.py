"""
Streamlit GUI for the Nexus AI.
"""

import streamlit as st
from main import AgenticAIAssistant
import json
import uuid
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Nexus AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, premium look
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3 {
        color: #58A6FF;
    } 
    
    /* Chat Input Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    .stChatInputContainer textarea {
        background-color: #1F242C;
        color: #FAFAFA;
        border: 1px solid #30363D;
        border-radius: 12px;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #58A6FF;
        box-shadow: 0 0 0 1px #58A6FF;
    }
    
    /* Message Container Styling */
    .stChatMessage {
        background-color: transparent; 
        border: none;
    }
    
    .stChatMessage[data-testid="stChatMessageAvatar"] {
        background-color: #1F242C;
        border: 1px solid #30363D;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #1F242C;
        color: #FAFAFA;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2EA043;
    }
    
    .stButton > button:active {
        background-color: #238636;
    }
    
    /* Title Gradient */
    .nexus-title {
        background: -webkit-linear-gradient(45deg, #58A6FF, #A371F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .nexus-subtitle {
        color: #8B949E;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Stat Cards */
    .stat-card {
        background-color: #1F242C;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #58A6FF;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #8B949E;
    }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = AgenticAIAssistant()
else:
    # Force reload if version doesn't match
    if not hasattr(st.session_state.agent, 'VERSION') or st.session_state.agent.VERSION != "3.2.0":
        st.session_state.agent = AgenticAIAssistant()
        st.toast("Nexus AI upgraded to Phase 3.2! 🚀")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_mode" not in st.session_state:
    st.session_state.agent_mode = "Standard"

def render_chat():
    """Render the main chat interface. (Phase 3 Enhanced)"""
    st.markdown('<div class="nexus-title">Nexus AI Chat</div>', unsafe_allow_html=True)
    
    # Simplified Chat Interface
    file_content = ""
    st.session_state.agent_mode = "Standard"

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])
            if "details" in message and message["details"]:
                with st.expander("Explore Execution Details"):
                    st.markdown(message["details"])

    # Chat input
    if prompt := st.chat_input("How can I assist you today?"):
        process_prompt(prompt, file_content)

def process_prompt(prompt, file_context=""):
    """Handle processing of a prompt (either from input or chips)."""
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt, 
        "avatar": "👤",
        "metadata": {"mode": st.session_state.agent_mode}
    })
    
    # Force a rerun to show user message immediately if needed, 
    # but normally we handle it in the same run.
    
    with st.chat_message("assistant", avatar="🌌"):
        # Phase 3: Use st.status for better feedback
        with st.status("Thinking and Executing...", expanded=True) as status:
            try:
                # Get response from the agent
                result = st.session_state.agent.process_query(
                    prompt, 
                    context={
                        "mode": st.session_state.agent_mode,
                        "file_context": file_context
                    }
                )
                response_text = result['response']
                
                # Show execution feedback in status but skip verbose logs
                if result.get('plan') or result.get('execution_results'):
                    pass # Keep quiet for a cleaner experience

                status.update(label="Execution Complete!", state="complete", expanded=False)
                
                # Show final response
                st.markdown(response_text)
                
                # Save assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text, 
                    "avatar": "🌌"
                })
                
            except Exception as e:
                status.update(label="Error Occurred", state="error")
                st.error(f"An error occurred: {str(e)}")
                st.session_state.agent.logger.error(f"UI Error: {str(e)}")

def render_dashboard():
    """Render the analytics dashboard. (Phase 2 Enhanced)"""
    st.markdown('<div class="nexus-title">Agent Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="nexus-subtitle">Deep insights into agent reasoning and performance.</div>', unsafe_allow_html=True)
    
    # Get stats from memory (assuming we will implement get_stats in memory.py)
    # For now, simulate some data or use basic history
    history = st.session_state.agent.memory.get_history()
    
    total_interactions = len(history)
    user_msgs = sum(1 for m in history if m['role'] == 'user')
    agent_msgs = sum(1 for m in history if m['role'] == 'assistant')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_interactions}</div>
            <div class="stat-label">Total Interactions</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{user_msgs}</div>
            <div class="stat-label">User Queries</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{agent_msgs}</div>
            <div class="stat-label">Agent Responses</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Activity Chart (Simulated for Demo if no real timestamps, but we have timestamps in memory)
    if history:
        df = pd.DataFrame(history)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            daily_counts = df.groupby('date').size().reset_index(name='counts')
            
            fig = px.bar(daily_counts, x='date', y='counts', title='Daily Activity',
                         labels={'date': 'Date', 'counts': 'Interactions'},
                         template="plotly_dark")
            fig.update_traces(marker_color='#58A6FF')
            st.plotly_chart(fig, use_container_width=True)
            
    st.markdown("### Recent Activity Log")
    if history:
        for item in reversed(history[-10:]):
            with st.expander(f"{item['timestamp']} - {item['role'].upper()}"):
                st.write(item['content'])
    else:
        st.info("No activity recorded yet.")

def render_settings():
    """Render the settings page."""
    st.markdown('<div class="nexus-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="nexus-subtitle">Configure your Nexus AI experience.</div>', unsafe_allow_html=True)
    
    st.subheader("General Settings")
    
    theme = st.selectbox("Theme", ["Dark (Default)", "Light", "System"])
    st.info("Theme changes require a page reload to fully take effect.")
    
    st.subheader("Memory Management")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Memory Usage", f"{len(st.session_state.agent.memory.get_history())} items")
    
    with col2:
        if st.button("🗑️ Clear Memory", type="primary"):
            st.session_state.agent.clear_memory()
            st.session_state.messages = []
            st.toast("Memory cleared successfully!")
            st.rerun()
            
    st.subheader("Export Data")
    if st.button("Download Conversation History"):
        history_json = json.dumps(st.session_state.agent.memory.get_history(), indent=2)
        st.download_button(
            label="Download JSON",
            data=history_json,
            file_name="nexus_ai_history.json",
            mime="application/json"
        )

def render_help():
    """Render the help/documentation page."""
    st.markdown('<div class="nexus-title">Help & Documentation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Getting Started
    Nexus AI is designed to be intuitive. Just type your request in the chat bar.
    
    ### 🛠️ Available Tools
    - **Web Search**: Automatically triggered for questions about news, facts, or data.
    - **Calculator**: Triggered for math expressions.
    - **System**: Ask for time, date, or OS info.
    - **Files**: Ask to "list files" or "read [filename]".
    
    ### 💡 Pro Tips
    - **Multi-tasking**: You can ask multiple things at once by using quotes.
      > `"What time is it?" "Search for AI news"`
    - **Context**: The agent remembers previous messages in the conversation.
    
    ### ❓ FAQ
    **Q: Can it write code?**
    A: It can plan coding tasks, but currently its primary tools are for information retrieval and system inspection.
    
    **Q: Is my data saved?**
    A: Yes, conversation history is saved locally in `memory.json`.
    """)

def main():
    """Main Nexus AI application. (Phase 2 Enhanced)"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1 style='color: #58A6FF;'>🌌 Nexus AI</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        page = st.radio("Navigation", ["Chat", "Knowledge Base", "Analytics", "Settings", "Help"], label_visibility="collapsed")
        
        st.markdown("---")
        
        # Quick Stats in Sidebar
        st.info(f"🧠 Memory: {len(st.session_state.agent.memory.get_history())} items")
        st.success(f"📂 KB: {len(st.session_state.agent.kb.get_all())} items")
        
        st.markdown("---")
        st.markdown("<small style='color: #8B949E;'>Nexus AI v2.2.0 (Phase 2)</small>", unsafe_allow_html=True)
    
    # specific page rendering
    if page == "Chat":
        render_chat()
    elif page == "Knowledge Base":
        render_kb_explorer()
    elif page == "Analytics":
        render_dashboard()
    elif page == "Settings":
        render_settings()
    elif page == "Help":
        render_help()

def render_kb_explorer():
    """Phase 2: Explore the agent's internal knowledge."""
    st.markdown('<div class="nexus-title">Knowledge Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="nexus-subtitle">Manage and search through the agent\'s learned knowledge.</div>', unsafe_allow_html=True)
    
    kb = st.session_state.agent.kb
    knowledge_data = kb.get_all()
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Add Knowledge")
        source = st.text_input("Source Name (e.g., project_rules.txt)")
        content = st.text_area("Content")
        if st.button("Learn Information"):
            if source and content:
                kb.learn(source, content)
                st.success(f"Learned about {source}!")
                st.rerun()
            else:
                st.warning("Please provide both source and content.")

    with col1:
        st.subheader("Internal Knowledge Map")
        if not knowledge_data:
            st.info("Knowledge base is currently empty. Use the 'Add Knowledge' tool to teach the agent.")
        else:
            search_query = st.text_input("🔍 Search KB", "")
            for source, info in knowledge_data.items():
                if search_query.lower() in source.lower() or search_query.lower() in info["content"].lower():
                    with st.expander(f"📄 {source}"):
                        st.markdown(f"**Learned on:** {datetime.fromtimestamp(info.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
                        st.text(info["content"])

# --- Modify render_chat to show plan details better ---
# (Already done in previous steps but ensuring integration)


if __name__ == "__main__":
    main()
