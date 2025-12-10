from typing import Dict, Any, List, Tuple, Callable, Optional
import asyncio
from datetime import datetime


class WorkflowEngine:
    """Core workflow execution engine"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
    
    def register_tool(self, name: str, func: Callable):
        """Register a tool function"""
        self.tools[name] = func
    
    async def run_workflow(
        self,
        nodes: Dict[str, Dict[str, Any]],
        edges: Dict[str, str],
        conditional_edges: Dict[str, Dict[str, Any]],
        initial_state: Dict[str, Any],
        max_iterations: int = 10
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Execute a workflow from start to finish
        
        Args:
            nodes: Dictionary of node definitions
            edges: Simple edge mappings (node_name -> next_node_name)
            conditional_edges: Conditional routing rules
            initial_state: Starting state dictionary
            max_iterations: Maximum iterations to prevent infinite loops
        
        Returns:
            Tuple of (final_state, execution_log)
        """
        state = initial_state.copy()
        execution_log = []
        current_node = "START"
        iteration = 0
        
        while current_node != "END" and iteration < max_iterations:
            iteration += 1
            
            # Log step
            log_entry = {
                "iteration": iteration,
                "node": current_node,
                "timestamp": datetime.now().isoformat()
            }
            
            if current_node == "START":
                # Find the first real node
                current_node = edges.get("START")
                if not current_node:
                    break
                continue
            
            # Execute node function
            if current_node in nodes:
                node_def = nodes[current_node]
                func_name = node_def.get("function")
                
                if func_name and func_name in self.tools:
                    try:
                        # Execute the tool
                        result = await asyncio.to_thread(
                            self.tools[func_name],
                            state
                        )
                        
                        # Update state with result
                        if isinstance(result, dict):
                            state.update(result)
                        
                        log_entry["status"] = "success"
                        log_entry["output"] = result
                    except Exception as e:
                        log_entry["status"] = "error"
                        log_entry["error"] = str(e)
                        execution_log.append(log_entry)
                        break
                else:
                    log_entry["status"] = "skipped"
                    log_entry["reason"] = "No function defined"
            
            execution_log.append(log_entry)
            
            # Determine next node
            next_node = None
            
            # Check conditional edges first
            if current_node in conditional_edges:
                conditions = conditional_edges[current_node]
                
                for condition_key, condition_def in conditions.items():
                    field = condition_def.get("field")
                    operator = condition_def.get("operator")
                    value = condition_def.get("value")
                    target = condition_def.get("target")
                    
                    if self._evaluate_condition(state, field, operator, value):
                        next_node = target
                        break
            
            # Fall back to simple edges
            if next_node is None:
                next_node = edges.get(current_node, "END")
            
            current_node = next_node
        
        if iteration >= max_iterations:
            execution_log.append({
                "warning": "Max iterations reached",
                "timestamp": datetime.now().isoformat()
            })
        
        return state, execution_log
    
    def _evaluate_condition(
        self,
        state: Dict[str, Any],
        field: str,
        operator: str,
        value: Any
    ) -> bool:
        """Evaluate a conditional expression"""
        if field not in state:
            return False
        
        state_value = state[field]
        
        if operator == ">=":
            return state_value >= value
        elif operator == ">":
            return state_value > value
        elif operator == "<=":
            return state_value <= value
        elif operator == "<":
            return state_value < value
        elif operator == "==":
            return state_value == value
        elif operator == "!=":
            return state_value != value
        
        return False