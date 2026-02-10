"""
Planner module for breaking down complex tasks into actionable steps.
"""

from typing import List, Dict, Any
import json


class Planner:
    """Plans and breaks down complex tasks into executable steps."""
    
    def __init__(self):
        self.plan_history = []
    
    def create_plan(self, task: str, available_tools: List[str], mode: str = "Standard") -> List[Dict[str, Any]]:
        """
        Create a plan for executing a task with mode awareness. (Phase 3)
        """
        # Enhanced rule-based planner with confidence scoring
        plan = []
        
        # 0. Handle multiple quoted tasks (e.g. "Task A" "Task B")
        import re
        if '"' in task:
            subtasks = re.findall(r'"([^"]*)"', task)
            if subtasks:
                for idx, subtask in enumerate(subtasks):
                    # Add steps for each subtask
                    self._add_steps_for_task(subtask, plan, step_offset=len(plan), mode=mode)
                
                self.plan_history.append({"task": task, "plan": plan, "mode": mode})
                return plan

        # Single task processing
        self._add_steps_for_task(task, plan, mode=mode)
        
        self.plan_history.append({
            "task": task,
            "plan": plan,
            "mode": mode
        })
        
        return plan

    def _add_steps_for_task(self, task: str, plan: List[Dict[str, Any]], step_offset: int = 0, mode: str = "Standard"):
        """Helper to add steps with mode-based intelligence. (Phase 3)"""
        task_lower = task.lower().strip()
        
        # 1. Analyst Mode Enhancements
        if mode == "Analyst" and ("data" in task_lower or "summary" in task_lower or "csv" in task_lower or "analyze" in task_lower):
            plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "data",
                "description": "Perform statistical analysis in Analyst mode",
                "parameters": {"operation": "summarize_csv", "path": "data.csv" if "." not in task_lower else task.split(".")[-2].split()[-1] + ".csv"},
                "confidence": 0.95,
                "reasoning": "Analyst mode prioritizes data tools"
            })
            return

        # 2. Researcher Mode Enhancements
        if mode == "Researcher" and any(kw in task_lower for kw in ["find", "search", "who", "what", "news"]):
             plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "web_search",
                "description": "Deep research via Web Search",
                "parameters": {"query": task},
                "confidence": 0.99,
                "reasoning": "Researcher mode maximizes search depth"
            })
             # Add a summary step for researcher
             plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "general",
                "description": "Synthesize research findings",
                "parameters": {"response": "I've completed the research. Based on the search results, here is a detailed synthesis..."},
                "confidence": 0.8,
                "reasoning": "Researchers always synthesize information"
            })
             return

        # 1. Greetings & Persona
        if task_lower in ["hi", "hello", "hey", "greetings", "who are you?", "who are you", "what are you?"]:
            plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "general",
                "description": "Reply to greeting/persona",
                "parameters": {"response": f"I am Nexus AI Phase 3, currently operating in {mode} mode. How can I help?"},
                "confidence": 1.0,
                "reasoning": "Detected greeting/persona content"
            })
            return

        # 2. Multi-step Search & Analysis (New in Phase 2)
        if "analyze" in task_lower and ("file" in task_lower or "data" in task_lower):
             # Task: "List files and analyze requirements.txt"
             if "list" in task_lower:
                plan.append({
                    "step": len(plan) + step_offset + 1,
                    "action": "file",
                    "description": "List files for inventory",
                    "parameters": {"operation": "list", "path": "."},
                    "confidence": 0.9,
                    "reasoning": "User asked to list and analyze"
                })
             
             # We can't really "analyze" without a real LLM, but we can simulate a deep read
             plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "file",
                "description": "Read file for analysis",
                "parameters": {"operation": "read", "path": "requirements.txt"}, # Default to requirements for demo
                "confidence": 0.8,
                "reasoning": "Analysis requires reading file content"
            })
             
             plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "general",
                "description": "Summarize analysis",
                "parameters": {"response": "I've analyzed the files. The requirements.txt contains the project dependencies. Let me know if you need specific details from them."},
                "confidence": 0.7,
                "reasoning": "Providing summary of read operation"
            })
             return

        # 3. System Queries (Time/Date)
        if "time" in task_lower:
            plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "system",
                "description": "Get current time",
                "parameters": {"action": "time"},
                "confidence": 0.95,
                "reasoning": "Keyword 'time' found"
            })
        if "date" in task_lower:
            plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "system",
                "description": "Get current date",
                "parameters": {"action": "date"},
                "confidence": 0.95,
                "reasoning": "Keyword 'date' found"
            })
            
        # 4. File Operations
        if any(x in task_lower for x in ["list file", "show file", "ls", "files in"]):
            plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "file",
                "description": "List files in current directory",
                "parameters": {"operation": "list", "path": "."},
                "confidence": 0.9,
                "reasoning": "Detected file listing intent"
            })
        elif any(x in task_lower for x in ["read", "content of", "show content", "cat "]):
            words = task.split()
            filename = None
            for word in words:
                if "." in word and len(word) > 2:
                    filename = word.strip('"\'')
                    break
            if not filename: filename = words[-1].strip('"\'')

            plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "file",
                "description": f"Read file: {filename}",
                "parameters": {"operation": "read", "path": filename},
                "confidence": 0.85,
                "reasoning": f"Detected read intent for {filename}"
            })

        # 5. Search
        elif any(kw in task_lower for kw in ["search", "find", "look up", "google", "who is", "what is", "news", "how to"]):
            if not ("time" in task_lower or "date" in task_lower):
                clean_query = task.replace('"', '').replace("Search for", "").strip()
                plan.append({
                    "step": len(plan) + step_offset + 1,
                    "action": "web_search",
                    "description": f"Search the web for: {clean_query}",
                    "parameters": {"query": clean_query},
                    "confidence": 0.8,
                    "reasoning": "Detected informational query"
                })
            
        # 6. Calculation
        elif any(op in task for op in ["+", "-", "*", "/", "sqrt", "pow"]):
             if not any(c in task_lower for c in ["search", "time", "date"]):
                clean_expr = task.replace('"', '').replace("Calculate", "").strip()
                plan.append({
                    "step": len(plan) + step_offset + 1,
                    "action": "calculator",
                    "description": f"Calculate: {clean_expr}",
                    "parameters": {"expression": clean_expr},
                    "confidence": 0.9,
                    "reasoning": "Detected mathematical expression"
                })
            
        # 7. Fallback
        if len(plan) == step_offset:
             plan.append({
                "step": len(plan) + step_offset + 1,
                "action": "general",
                "description": "General response",
                "parameters": {"response": f"Nexus AI Phase 3 ({mode}): I couldn't map '{task}' to a tool. I can deep research, analyze data, and manage your files."},
                "confidence": 0.1,
                "reasoning": "No specific intent matched"
            })



    
    def refine_plan(self, plan: List[Dict[str, Any]], feedback: str) -> List[Dict[str, Any]]:
        """
        Refine a plan based on feedback.
        
        Args:
            plan: Current plan
            feedback: Feedback to incorporate
            
        Returns:
            Refined plan
        """
        # Add feedback-based refinement logic here
        return plan
    
    def get_plan_history(self) -> List[Dict[str, Any]]:
        """Get the history of all plans created."""
        return self.plan_history

