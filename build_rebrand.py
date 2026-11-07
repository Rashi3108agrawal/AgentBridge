"""
AgentBridge Rebrand and Architecture Transformation Script.
"""

import os
import re
from pathlib import Path

ROOT = Path(r"d:\github\ai-gateway")

def update_file(path: Path, transform_fn):
    if not path.exists():
        print(f"Skipping missing: {path}")
        return
    text = path.read_text(encoding="utf-8")
    new_text = transform_fn(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated: {path}")
    else:
        print(f"Unchanged: {path}")

def general_replacements(text: str) -> str:
    # Package imports
    text = text.replace("from ai_gateway.", "from agentbridge.")
    text = text.replace("from ai_gateway import", "from agentbridge import")
    text = text.replace("import ai_gateway.", "import agentbridge.")
    text = text.replace("import ai_gateway", "import agentbridge")
    text = text.replace('"ai_gateway.', '"agentbridge.')
    text = text.replace("'ai_gateway.", "'agentbridge.")
    text = text.replace('"ai_gateway:', '"agentbridge:')
    text = text.replace("'ai_gateway:", "'agentbridge:")
    text = text.replace("ai_gateway:migrations", "agentbridge:migrations")
    text = text.replace("ai_gateway.app:create_app", "agentbridge.app:create_app")
    text = text.replace("ai_gateway.cli", "agentbridge.cli")
    text = text.replace("ai_gateway.admin", "agentbridge.admin")
    text = text.replace("ai_gateway.migrate", "agentbridge.migrate")
    return text

print("Starting rebrand pass...")

