"""
Executor module for executing planned actions.
"""

from typing import Dict, Any, List, Callable
import traceback


class Executor:
    """Executes planned actions using available tools."""
    
    def __init__(self):
        """Initialize the executor."""
        self.execution_history = []
        self.tool_registry = {}
    
    def register_tool(self, name: str, tool: Callable):
        """
        Register a tool for execution.
        
        Args:
            name: Tool name
            tool: Tool function or callable object
        """
        self.tool_registry[name] = tool
    
    def execute_step(self, step: Dict[str, Any], tools: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a single plan step.
        
        Args:
            step: Plan step dictionary with action and parameters
            tools: Dictionary of available tools
            
        Returns:
            Execution result dictionary
        """
        action = step.get("action")
        parameters = step.get("parameters", {})
        description = step.get("description", "")
        
        # Use provided tools or registered tools
        available_tools = tools if tools else self.tool_registry
        
        if action not in available_tools:
            return {
                "success": False,
                "result": f"Tool '{action}' not found",
                "error": f"Unknown action: {action}"
            }
        
        try:
            tool = available_tools[action]
            
            # Check if tool has execute method (for tool classes)
            if hasattr(tool, "execute"):
                result = tool.execute(**parameters)
            elif callable(tool):
                result = tool(**parameters)
            else:
                return {
                    "success": False,
                    "result": f"Tool '{action}' is not callable",
                    "error": "Invalid tool type"
                }
            
            execution_record = {
                "step": step.get("step"),
                "action": action,
                "description": description,
                "parameters": parameters,
                "success": True,
                "result": result,
                "error": None
            }
            
            self.execution_history.append(execution_record)
            return execution_record
            
        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            execution_record = {
                "step": step.get("step"),
                "action": action,
                "description": description,
                "parameters": parameters,
                "success": False,
                "result": None,
                "error": error_msg,
                "traceback": error_trace
            }
            
            self.execution_history.append(execution_record)
            return execution_record
    
    def execute_plan(self, plan: List[Dict[str, Any]], tools: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute a complete plan.
        
        Args:
            plan: List of plan steps
            tools: Dictionary of available tools
            
        Returns:
            List of execution results
        """
        results = []
        
        for step in plan:
            result = self.execute_step(step, tools)
            results.append(result)
            
            # Stop execution if a critical step fails
            if not result["success"] and step.get("critical", False):
                break
        
        return results
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history."""
        return self.execution_history
    
    def clear_history(self):
        """Clear the execution history."""
        self.execution_history = []

