"""
Comprehensive AgentBridge Rebrand Script
"""
import os
import re
import shutil
from pathlib import Path

ROOT = Path(r"d:\github\ai-gateway")

def update_file(p: Path, fn):
    if not p.exists():
        print(f"Skipping missing: {p}")
        return
    text = p.read_text(encoding="utf-8")
    new_text = fn(text)
    if new_text != text:
        p.write_text(new_text, encoding="utf-8")
        print(f"Updated: {p}")
    else:
        print(f"Unchanged: {p}")

def rebrand_py_content(content: str) -> str:
    # Package imports and modules
    content = content.replace("from ai_gateway.", "from agentbridge.")
    content = content.replace("from ai_gateway import", "from agentbridge import")
    content = content.replace("import ai_gateway.", "import agentbridge.")
    content = content.replace("import ai_gateway", "import agentbridge")
    content = content.replace('"ai_gateway.', '"agentbridge.')
    content = content.replace("'ai_gateway.", "'agentbridge.")
    content = content.replace('"ai_gateway:', '"agentbridge:')
    content = content.replace("'ai_gateway:", "'agentbridge:")
    content = content.replace("ai_gateway:migrations", "agentbridge:migrations")
    content = content.replace("ai_gateway.app:create_app", "agentbridge.app:create_app")
    content = content.replace("ai_gateway.cli", "agentbridge.cli")
    content = content.replace("ai_gateway.admin", "agentbridge.admin")
    content = content.replace("ai_gateway.migrate", "agentbridge.migrate")
    content = content.replace("ai-gateway", "agentbridge")
    content = content.replace("AI Gateway", "AgentBridge")
    content = content.replace("ai_gateway", "agentbridge")
    return content

# 1. Process all Python files in src/agentbridge, tests, bench, examples
for folder in ["src/agentbridge", "tests", "bench", "examples"]:
    for py_file in (ROOT / folder).rglob("*.py"):
        update_file(py_file, rebrand_py_content)

# 2. Update config files: create agentbridge.yaml, agentbridge.example.yaml, agentbridge.bench.yaml
if (ROOT / "config" / "gateway.yaml").exists():
    gw_yaml = (ROOT / "config" / "gateway.yaml").read_text(encoding="utf-8")
    (ROOT / "config" / "agentbridge.yaml").write_text(gw_yaml, encoding="utf-8")
if (ROOT / "config" / "gateway.example.yaml").exists():
    gw_ex_yaml = (ROOT / "config" / "gateway.example.yaml").read_text(encoding="utf-8")
    (ROOT / "config" / "agentbridge.example.yaml").write_text(gw_ex_yaml, encoding="utf-8")
if (ROOT / "bench" / "gateway.bench.yaml").exists():
    gw_b_yaml = (ROOT / "bench" / "gateway.bench.yaml").read_text(encoding="utf-8")
    (ROOT / "bench" / "agentbridge.bench.yaml").write_text(gw_b_yaml, encoding="utf-8")

# 3. Update alembic.ini
def update_alembic_ini(text: str) -> str:
    text = text.replace("script_location = ai_gateway:migrations", "script_location = agentbridge:migrations")
    text = text.replace("ai-gateway", "agentbridge")
    return text
update_file(ROOT / "alembic.ini", update_alembic_ini)

# 4. Update pyproject.toml
def update_pyproject(text: str) -> str:
    text = text.replace('name = "ai-gateway"', 'name = "agentbridge"')
    text = text.replace(
        'description = "Self-hosted OpenAI-compatible LLM gateway: routing, fallback, caching, quotas, metering"',
        'description = "Enterprise AI infrastructure and agent orchestration platform: intelligent routing, resilience, caching, quotas, telemetry"'
    )
    text = text.replace(
        'authors = [\n    { name = "Chaitanya Mhetre", email = "mhetrechaitanya06@gmail.com" }\n]',
        'authors = [\n    { name = "AgentBridge Platform Team", email = "platform@agentbridge.io" }\n]'
    )
    text = text.replace('ai-gateway = "ai_gateway.cli:main"', 'agentbridge = "agentbridge.cli:main"\nai-gateway = "agentbridge.cli:main"')
    text = text.replace('ai_gateway', 'agentbridge')
    return text
update_file(ROOT / "pyproject.toml", update_pyproject)

# 5. Update Makefile
def update_makefile(text: str) -> str:
    text = text.replace("ai_gateway.app:create_app", "agentbridge.app:create_app")
    text = text.replace("ai-gateway", "agentbridge")
    return text
update_file(ROOT / "Makefile", update_makefile)

# 6. Update Dockerfile
def update_dockerfile(text: str) -> str:
    text = text.replace('CMD ["ai-gateway", "serve"', 'CMD ["agentbridge", "serve"')
    text = text.replace('ai-gateway', 'agentbridge')
    return text
update_file(ROOT / "Dockerfile", update_dockerfile)

# 7. Update docker-compose.yml
def update_compose(text: str) -> str:
    text = text.replace('command: ["ai-gateway", "migrate"]', 'command: ["agentbridge", "migrate"]')
    text = text.replace('command: ["ai-gateway", "usage-worker"]', 'command: ["agentbridge", "usage-worker"]')
    text = text.replace('ai-gateway', 'agentbridge')
    return text
update_file(ROOT / "docker-compose.yml", update_compose)

# 8. Update .github/workflows/ci.yml
def update_ci(text: str) -> str:
    text = text.replace("uv run ai-gateway migrate", "uv run agentbridge migrate")
    text = text.replace("ai-gateway:ci", "agentbridge:ci")
    text = text.replace("ai-gateway", "agentbridge")
    return text
update_file(ROOT / ".github" / "workflows" / "ci.yml", update_ci)

# 9. Update .env.example
def update_env(text: str) -> str:
    text = text.replace("ai-gateway migrate", "agentbridge migrate")
    text = text.replace("ai-gateway create-admin", "agentbridge create-admin")
    return text
update_file(ROOT / ".env.example", update_env)

# 10. Update Grafana & Prometheus deployment files
if (ROOT / "deploy" / "grafana" / "dashboards" / "ai-gateway.json").exists():
    dash = (ROOT / "deploy" / "grafana" / "dashboards" / "ai-gateway.json").read_text(encoding="utf-8")
    dash = dash.replace('"uid": "ai-gateway"', '"uid": "agentbridge"')
    dash = dash.replace('"title": "AI Gateway"', '"title": "AgentBridge Operations"')
    dash = dash.replace('ai-gateway', 'agentbridge')
    (ROOT / "deploy" / "grafana" / "dashboards" / "agentbridge.json").write_text(dash, encoding="utf-8")
    # remove old ai-gateway.json
    (ROOT / "deploy" / "grafana" / "dashboards" / "ai-gateway.json").unlink()

def update_dashboards_yml(text: str) -> str:
    text = text.replace("name: ai-gateway", "name: agentbridge")
    text = text.replace("ai-gateway", "agentbridge")
    return text
update_file(ROOT / "deploy" / "grafana" / "provisioning" / "dashboards" / "dashboards.yml", update_dashboards_yml)

def update_prometheus_yml(text: str) -> str:
    text = text.replace("job_name: ai-gateway", "job_name: agentbridge")
    text = text.replace("ai-gateway", "agentbridge")
    return text
update_file(ROOT / "deploy" / "prometheus.yml", update_prometheus_yml)

# 11. Update examples/quickstart.sh
def update_quickstart(text: str) -> str:
    text = text.replace("ai-gateway create-admin", "agentbridge create-admin")
    text = text.replace("ai-gateway", "agentbridge")
    return text
update_file(ROOT / "examples" / "quickstart.sh", update_quickstart)

# 12. Update tests/fixtures/README.md
def update_fixtures_readme(text: str) -> str:
    text = text.replace("ai-gateway", "agentbridge")
    text = text.replace("ai_gateway", "agentbridge")
    return text
update_file(ROOT / "tests" / "fixtures" / "README.md", update_fixtures_readme)

print("Pass 1 completed successfully.")

