# GENAJA PLATINUM GOVERNANCE HOOK - DO NOT EDIT MANUALLY
# This module orchestrates metadata registration and system-wide versioning.
"""
Genaja Version Hook — Rastreabilidade de Versão por Módulo.

Uso em módulos essenciais:
    from version_hook import declare
    declare(__name__, __version__, "Módulo de governança selado (Padrão Platinum)")

Regra:
    - Se a versão registrada no JSON for diferente da declarada, um changelog é obrigatório.
    - Se for a primeira declaração, registra sem exigir changelog.
    - Mudança de versão SEM changelog levanta ValueError.
"""
import json
import os
from version import __version__

_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "module_versions.json")


def declare(module_name: str, version: str, changelog: str = "") -> None:
    """
    Registra a versão de um módulo no registry centralizado.

    Args:
        module_name: Nome do módulo (__name__ do arquivo).
        version:     Versão atual do módulo (ex: "0.7.1").
        changelog:   Obrigatório quando a versão muda. Descreve o que mudou.

    Raises:
        ValueError: Se a versão mudou e nenhum changelog foi fornecido.
    """
    registry = _load()
    previous = registry.get(module_name, {})
    prev_version = previous.get("version", "")

    if prev_version and prev_version != version:
        if not changelog:
            raise ValueError(
                f"\n[version_hook] VERSÃO ALTERADA SEM DESCRIÇÃO\n"
                f"  Módulo  : {module_name}\n"
                f"  Anterior: {prev_version}\n"
                f"  Nova    : {version}\n"
                f"  Ação    : declare('{module_name}', '{version}', changelog='descreva a mudança')"
            )

    registry[module_name] = {
        "version": version,
        "changelog": changelog if changelog else previous.get("changelog", "Versão inicial"),
    }
    _save(registry)


def _load() -> dict:
    if not os.path.exists(_REGISTRY_PATH):
        return {}
    try:
        with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(registry: dict) -> None:
    os.makedirs(os.path.dirname(_REGISTRY_PATH), exist_ok=True)
    with open(_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)

# --- Auto-declaração de Governança Platinum ---
declare(__name__, __version__, "Módulo mestre de governança e rastreabilidade de versão")
