"""Tool functions for workflow nodes"""
import re
from typing import Dict, Any, List


def extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    """Extract function definitions from code"""
    code = state.get("code", "")
    
    # Simple regex to find function definitions
    func_pattern = r'defs+(w+)s*([^)]*):'
    functions = re.findall(func_pattern, code)
    
    return {
        "functions": functions,
        "function_count": len(functions)
    }


def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    """Check code complexity (simplified)"""
    code = state.get("code", "")
    
    # Count lines
    lines = [l for l in code.split('
') if l.strip() and not l.strip().startswith('#')]
    line_count = len(lines)
    
    # Count control flow statements as proxy for complexity
    complexity_keywords = ['if', 'for', 'while', 'elif', 'else']
    complexity_score = sum(code.count(kw) for kw in complexity_keywords)
    
    return {
        "line_count": line_count,
        "complexity_score": complexity_score
    }


def detect_issues(state: Dict[str, Any]) -> Dict[str, Any]:
    """Detect basic code issues"""
    code = state.get("code", "")
    issues = []
    
    # Check for common issues
    if "except:" in code:
        issues.append("Bare except clause found")
    
    if "eval(" in code:
        issues.append("Use of eval() detected")
    
    if "global " in code:
        issues.append("Global variable usage detected")
    
    # Check line length
    long_lines = [i for i, line in enumerate(code.split('
'), 1) 
                  if len(line) > 100]
    if long_lines:
        issues.append(f"Lines exceed 100 characters: {long_lines[:3]}")
    
    return {
        "issues": issues,
        "issue_count": len(issues)
    }


def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest code improvements"""
    issues = state.get("issues", [])
    complexity_score = state.get("complexity_score", 0)
    
    suggestions = []
    
    if complexity_score > 10:
        suggestions.append("Consider breaking down complex functions")
    
    if len(issues) > 0:
        suggestions.append("Address detected code issues")
    
    if state.get("line_count", 0) > 100:
        suggestions.append("Consider modularizing code into smaller functions")
    
    # Calculate quality score
    quality_score = 100 - (len(issues) * 10) - (min(complexity_score, 5) * 5)
    quality_score = max(0, quality_score)
    
    return {
        "suggestions": suggestions,
        "quality_score": quality_score
    }


def refine_code(state: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate code refinement"""
    current_score = state.get("quality_score", 0)
    iteration = state.get("iteration", 0)
    
    # Simulate improvement
    improved_score = min(100, current_score + 15)
    
    return {
        "quality_score": improved_score,
        "iteration": iteration + 1,
        "refinement_applied": True
    }