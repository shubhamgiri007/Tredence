import re
from typing import Dict


class AutocompleteService:
    """Service for providing mocked AI autocomplete suggestions"""

    PYTHON_PATTERNS = {
        r"def\s+\w*$": "def function_name(param1, param2):\n    pass",
        r"class\s+\w*$": "class ClassName:\n    def __init__(self):\n        pass",
        r"if\s+\w*$": "if condition:\n    pass",
        r"for\s+\w*$": "for item in iterable:\n    pass",
        r"while\s+\w*$": "while condition:\n    pass",
        r"try\s*:?\s*$": "try:\n    pass\nexcept Exception as e:\n    pass",
        r"import\s+\w*$": "import numpy as np",
        r"from\s+\w*$": "from module import function",
        r"print\s*\(\s*$": 'print("Hello, World!")',
        r"return\s+\w*$": "return result",
    }

    JAVASCRIPT_PATTERNS = {
        r"function\s+\w*$": "function functionName(params) {\n  return null;\n}",
        r"const\s+\w*$": "const variableName = value;",
        r"let\s+\w*$": "let variableName = value;",
        r"if\s*\(\s*$": "if (condition) {\n  // code\n}",
        r"for\s*\(\s*$": "for (let i = 0; i < array.length; i++) {\n  // code\n}",
    }

    @staticmethod
    def get_suggestion(code: str, cursor_position: int, language: str = "python") -> Dict[str, any]:
        """
        Generate a mocked autocomplete suggestion based on the current code context
        
        Args:
            code: The current code content
            cursor_position: Current cursor position
            language: Programming language
            
        Returns:
            Dictionary containing suggestion, confidence, and type
        """
        lines = code[:cursor_position].split('\n')
        current_line = lines[-1] if lines else ""

        patterns = AutocompleteService.PYTHON_PATTERNS if language == "python" else AutocompleteService.JAVASCRIPT_PATTERNS

        for pattern, suggestion in patterns.items():
            if re.search(pattern, current_line):
                return {
                    "suggestion": suggestion,
                    "confidence": 0.85,
                    "type": "snippet"
                }

        if language == "python":
            if "[" in current_line and "for" not in current_line:
                return {
                    "suggestion": "[x for x in iterable if condition]",
                    "confidence": 0.75,
                    "type": "snippet"
                }

            if "    def " in current_line or "\tdef " in current_line:
                return {
                    "suggestion": "def method_name(self, param):\n        pass",
                    "confidence": 0.8,
                    "type": "method"
                }

            if current_line.strip().startswith("import") or current_line.strip().startswith("from"):
                return {
                    "suggestion": "from typing import List, Dict, Optional",
                    "confidence": 0.7,
                    "type": "import"
                }

        common_suggestions = {
            "python": "# TODO: Implement this function",
            "javascript": "// TODO: Implement this function",
            "typescript": "// TODO: Implement this function",
        }

        return {
            "suggestion": common_suggestions.get(language, "# Add your code here"),
            "confidence": 0.5,
            "type": "comment"
        }
