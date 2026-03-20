"""
Promptfoo Shim for EU AI Act Classifier

This shim bridges Promptfoo's evaluation engine with our LangGraph-based
EU AI Act classifier application.

Promptfoo calls call_api(prompt, options, context) for each test case.
We parse the prompt (expected format: "product_name | description"),
invoke our classifier graph, and return the result in Promptfoo's format.

Usage in promptfooconfig.yaml:
  providers:
    - id: 'file://promptfoo_shim.py'
"""

import json
import sys
import os

# Make sure our app module is importable
sys.path.insert(0, os.path.dirname(__file__))


def call_api(prompt: str, options: dict, context: dict) -> dict:
    """
    Promptfoo shim entry point.

    Args:
        prompt: The test prompt from promptfooconfig.yaml.
                Expected format: "product_name | description"
        options: Promptfoo options (temperature, etc.) — not used here
        context: Promptfoo context (vars, test metadata)

    Returns:
        dict with 'output' key (required by Promptfoo) containing
        the JSON classification result.
    """
    try:
        # Support both pipe-separated format and structured vars from context
        vars_ = context.get("vars", {}) if context else {}

        product_name = vars_.get("product_name", "")
        description = vars_.get("description", "")

        # Fallback: parse from prompt string "product_name | description"
        if not product_name and "|" in prompt:
            parts = prompt.split("|", 1)
            product_name = parts[0].strip()
            description = parts[1].strip()
        elif not product_name:
            product_name = "Unknown Product"
            description = prompt.strip()

        # Import and invoke our LangGraph classifier
        from app import graph

        result = graph.invoke(
            {
                "messages": [],
                "product_name": product_name,
                "description": description,
                "classification": "",
                "reasoning": "",
                "confidence": 0.0,
            }
        )

        output = {
            "product_name": product_name,
            "classification": result["classification"],
            "reasoning": result["reasoning"],
            "confidence": result["confidence"],
        }

        # Promptfoo requires output to be a string or dict
        return {"output": json.dumps(output)}

    except Exception as e:
        return {"error": str(e)}
