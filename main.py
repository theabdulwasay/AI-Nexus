"""
Main agent logic - Backend for the Agentic AI Assistant.
"""

from agent.planner import Planner
from agent.executor import Executor
from agent.memory import Memory
from tools.web_search import WebSearch
from tools.calculator import Calculator
from config_manager import ConfigManager
from logger import Logger
from typing import Dict, Any, List
import os


class AgenticAIAssistant:
    """Main agent class that orchestrates planning, execution, and memory."""
    VERSION = "3.2.0" # Bumped to force reload after simplification

    
    PERSONAS = {
        "Standard": "You are a helpful and efficient agentic assistant.",
        "Analyst": "You are a data-driven Analyst. Focus on statistics, trends, and detailed data summaries. Use pandas whenever possible.",
        "Researcher": "You are a thorough Researcher. Focus on exhaustive web searches, citing sources, and providing deep context.",
        "Creative": "You are a Creative assistant. Focus on brainstorming, innovative solutions, and engaging, descriptive responses."
    }

    def __init__(self):
        """Initialize the agent with all components."""
        self.config = ConfigManager()
        self.logger = Logger()
        
        self.logger.info("Initializing Nexus AI Agent (Phase 3)...")
        
        self.planner = Planner()
        self.executor = Executor()
        self.memory = Memory()
        
        # New Phase 2/3 Components
        from agent.knowledge_base import KnowledgeBase
        self.kb = KnowledgeBase()
        
        # Register available tools
        from tools.system_tools import SystemTool, FileTool
        from tools.web_search import WebSearch
        from tools.calculator import Calculator
        from tools.data_tools import DataTool
        
        self.tools = {
            "web_search": WebSearch(),
            "calculator": Calculator(),
            "system": SystemTool(),
            "file": FileTool(),
            "data": DataTool()
        }
        
        # Load memory
        self.memory.load_from_disk()
        
        # Load base system prompt
        self.base_system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file."""
        prompt_path = os.path.join("prompts", "system_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return "You are a helpful AI assistant that can plan and execute tasks."
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a user query through the advanced agent pipeline with persona and file context.
        """
        context = context or {}
        mode = context.get("mode", "Standard")
        file_data = context.get("file_context", "") # New for Phase 3: attached file content
        
        # Augment query if file context is present
        effective_query = query
        if file_data:
            effective_query = f"[File Context Attached]\n{query}\n\nRelevant Data:\n{file_data[:2000]}"
            self.logger.info(f"Processing query with {len(file_data)} bytes of file context")

        # Persona injection (simulated)
        persona_prompt = self.PERSONAS.get(mode, self.PERSONAS["Standard"])
        self.logger.info(f"Applying persona: {mode}")

        # Store query in memory
        self.memory.add_interaction("user", query, metadata={"mode": mode, "has_file": bool(file_data)})
        
        # Get available tools
        available_tools = list(self.tools.keys())
        
        # Create plan (Advanced Planner) - Pass mode for mode-aware planning
        plan = self.planner.create_plan(effective_query, available_tools, mode=mode)
        self.logger.info(f"Phase 3 Plan created with {len(plan)} steps for mode: {mode}")
        
        # Execute plan with cross-step context replacement
        execution_results = []
        step_results_map = {} 
        
        for step in plan:
            action = step.get("action")
            parameters = step.get("parameters", {})
            description = step.get("description")
            step_num = step.get("step")
            
            # Resolve dependencies: replace {{step1_result}} etc.
            resolved_params = self._resolve_parameters(parameters, step_results_map)
            
            self.logger.info(f"Executing step {step_num}: {action}")
            
            if action in self.tools:
                tool = self.tools[action]
                try:
                    # Pass file context if tool supports it (simulated)
                    if action == "data" and file_data:
                        resolved_params["temp_data"] = file_data 
                        
                    result = tool.execute(**resolved_params)
                    status = "success"
                except Exception as e:
                    result = str(e)
                    status = "error"
            else:
                if action == "general":
                    result = resolved_params.get("response", "I'm not sure how to help with that.")
                    status = "success"
                else:
                    result = f"Action '{action}' not supported"
                    status = "skipped"
            
            # Store result for dependency resolution in later steps
            step_results_map[str(step_num)] = str(result)
            
            execution_results.append({
                "step": step_num,
                "action": action,
                "description": description,
                "result": result,
                "status": status,
                "parameters": resolved_params 
            })
            
            if status == "error" and step.get("critical", False):
                break
        
        # Generate response (Simulate persona tone)
        response = self._generate_response(query, plan, execution_results, mode=mode)
        
        # Store response in memory
        self.memory.add_interaction("assistant", response)
        
        return {
            "query": query,
            "plan": plan,
            "execution_results": execution_results,
            "response": response,
            "mode": mode,
            "context": context
        }


    def _resolve_parameters(self, parameters: Dict[str, Any], results_map: Dict[str, str]) -> Dict[str, Any]:
        """Replace placeholders like {{step1_result}} with actual results."""
        import json
        params_str = json.dumps(parameters)
        
        for step_id, result in results_map.items():
            placeholder = f"{{{{step{step_id}_result}}}}"
            if placeholder in params_str:
                # Basic string replacement
                params_str = params_str.replace(placeholder, result.replace('\n', '\\n'))
        
        return json.loads(params_str)

    def _generate_response(self, query: str, plan: List[Dict], results: List[Dict], mode: str = "Standard") -> str:
        """Generate a natural language response (Phase 3 Simplified)"""
        if not results:
            if not plan:
                return "I couldn't identify any specific steps to execute for this query."
            return "I planned some steps but couldn't execute them successfully."
            
        # Join all results into a single clean response
        response_items = []
        for result in results:
            if result["status"] == "success":
                response_items.append(str(result["result"]))
        
        return "\n\n".join(response_items) if response_items else "No successful results were generated."
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history from memory."""
        return self.memory.get_history()
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()


if __name__ == "__main__":
    # Example usage
    agent = AgenticAIAssistant()
    
    # Test queries
    test_queries = [
        "Calculate 25 * 4 + 100",
        "Search for information about Python programming"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        result = agent.process_query(query)
        print(f"\nResponse:\n{result['response']}\n")

