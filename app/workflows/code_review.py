"""Code Review Workflow Definition"""
from typing import Dict, Any, Tuple


def create_code_review_workflow() -> Tuple[Dict, Dict, Dict]:
    """
    Create a code review workflow with loop until quality threshold
    
    Returns:
        Tuple of (nodes, edges, conditional_edges)
    """
    
    nodes = {
        "extract_functions": {
            "function": "extract_functions",
            "description": "Extract function definitions from code"
        },
        "check_complexity": {
            "function": "check_complexity",
            "description": "Analyze code complexity"
        },
        "detect_issues": {
            "function": "detect_issues",
            "description": "Detect code issues"
        },
        "suggest_improvements": {
            "function": "suggest_improvements",
            "description": "Generate improvement suggestions"
        },
        "refine_code": {
            "function": "refine_code",
            "description": "Apply refinements to improve quality"
        }
    }
    
    # Simple sequential edges
    edges = {
        "START": "extract_functions",
        "extract_functions": "check_complexity",
        "check_complexity": "detect_issues",
        "detect_issues": "suggest_improvements",
        "suggest_improvements": "check_quality",
        "check_quality": "END",  # Default: end
        "refine_code": "suggest_improvements"  # Loop back
    }
    
    # Conditional routing: loop until quality_score >= 80
    conditional_edges = {
        "check_quality": {
            "continue_loop": {
                "field": "quality_score",
                "operator": "<",
                "value": 80,
                "target": "refine_code"
            },
            "finish": {
                "field": "quality_score",
                "operator": ">=",
                "value": 80,
                "target": "END"
            }
        }
    }
    
    return nodes, edges, conditional_edges