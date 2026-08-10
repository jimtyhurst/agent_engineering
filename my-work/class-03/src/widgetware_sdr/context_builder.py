import os
from pathlib import Path
import yaml
from widgetware_sdr.instructions import get_system_instructions


def build_context(
    account: dict,
    objective: str,
    evidence: list[dict],
    state: dict | None = None,
) -> dict:
    return {
        "system_instructions": get_system_instructions(),
        "business_context": {
            "products": load_products("."),
            "icp": load_icp("."),
            "policies": load_policies("."),
        },
        "task_context": {
            "account": account,
            "objective": objective,
        },
        "retrieved_evidence": evidence,
        "state": state if state is not None else {},
    }
    
def load_yaml_config(path: str) -> dict:
    """Load a YAML file and return its parsed content."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_products(base_dir: str) -> dict:
    """Load the WidgetWare products configuration."""
    path = os.path.join(base_dir, 'config', 'products.yaml')
    return load_yaml_config(path)

def load_icp(base_dir: str) -> dict:
    """Load the Ideal Customer Profile configuration."""
    path = os.path.join(base_dir, 'config', 'icp.yaml')
    return load_yaml_config(path)

def load_policies(base_dir: str) -> dict:
    """Load sales and safety policies."""
    path = os.path.join(base_dir, 'config', 'policies.yaml')
    return load_yaml_config(path)
