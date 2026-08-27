"""Load and resolve the OOMWOO baseline scenario registry.

The registry (``config/scenario_registry.yaml``) encodes the §5.1 test-matrix
scenarios with fixed world, initial pose and random seed so every experiment
is reproducible. ``resolve_scenario`` is pure and unit-testable.
"""

from __future__ import annotations

from typing import Dict, List, Optional

try:  # yaml is available in ROS2; keep import lazy for unit tests.
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_registry(path: str) -> Dict:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required to load the scenario registry")
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def list_scenarios(registry: Dict) -> List[Dict]:
    return registry.get("scenarios", [])


def get_scenario(registry: Dict, scenario_id: str) -> Optional[Dict]:
    """Return the resolved scenario dict for ``scenario_id``.

    Merges ``default_seed`` when the scenario does not specify its own seed,
    and validates that the mandatory fields are present.
    """
    default_seed = registry.get("default_seed")
    for scen in registry.get("scenarios", []):
        if scen.get("id") == scenario_id:
            resolved = dict(scen)
            if resolved.get("seed") is None:
                resolved["seed"] = default_seed
            _validate(resolved)
            return resolved
    return None


def _validate(scenario: Dict) -> None:
    required = ("id", "name", "world", "initial_pose")
    missing = [k for k in required if k not in scenario or scenario.get(k) is None]
    if missing:
        raise ValueError(
            f"scenario {scenario.get('id')!r} missing required fields: {missing}"
        )
