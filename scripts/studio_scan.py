#!/usr/bin/env python3
"""Scan repository state for Studio Director metrics and sprint planning."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def count_files(directory: Path, pattern: str) -> int:
    if not directory.exists():
        return 0
    return len(list(directory.rglob(pattern)))


def read_manifest_tiles() -> dict:
    manifest = ROOT / "data/tilesets/environment_base_pack_01_manifest.json"
    generated = ROOT / "data/tilesets/environment_base_pack_01_generated.json"
    result = {"manifest_total": 0, "generated_total": 0, "complete": False}
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        categories = data.get("categories", {})
        total = 0
        for category in categories.values():
            for tile in category.get("tiles", []):
                variants = tile.get("variants", data.get("variants_per_tile", {}).get("default", 1))
                if isinstance(variants, dict):
                    variants = variants.get("default", 1)
                total += int(variants) if variants else 1
        result["manifest_total"] = total or data.get("tile_count", 155)
    if generated.exists():
        data = json.loads(generated.read_text(encoding="utf-8"))
        items = data.get("generated", data.get("tiles", []))
        result["generated_total"] = len(items) if isinstance(items, list) else 0
    result["complete"] = result["generated_total"] >= result["manifest_total"] > 0
    return result


def detect_phase() -> str:
    cargo = ROOT / "Cargo.toml"
    maps = count_files(ROOT / "data/maps", "*.json")
    rust = count_files(ROOT / "src", "*.rs")
    if not cargo.exists():
        return "preproduction"
    if maps == 0 or rust < 10:
        return "vertical_slice"
    return "vertical_slice"


def scan_features() -> dict:
    features_dir = ROOT / "features"
    result = {}
    if not features_dir.exists():
        return result
    for feature_path in sorted(features_dir.iterdir()):
        if not feature_path.is_dir():
            continue
        readme = feature_path / "README.md"
        status = "unknown"
        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            match = re.search(r"\*\*Status:\*\*\s*(\w+)", text)
            if match:
                status = match.group(1).lower()
        tasks_file = feature_path / "TASKS.md"
        if not tasks_file.exists():
            tasks_file = feature_path / "tasks.md"
        open_tasks = 0
        if tasks_file.exists():
            open_tasks = len(re.findall(r"^- \[ \]", tasks_file.read_text(encoding="utf-8"), re.M))
        status_file = feature_path / "STATUS.md"
        lifecycle = status
        if status_file.exists():
            text = status_file.read_text(encoding="utf-8")
            match = re.search(r"\*\*Current:\*\*\s*`?(\w+)`?", text)
            if match:
                lifecycle = match.group(1).lower()
        result[feature_path.name] = {"status": status, "lifecycle": lifecycle, "open_tasks": open_tasks}
    return result


def main() -> None:
    env_png = count_files(ROOT / "assets/environment", "*.png")
    tiles = read_manifest_tiles()
    rust_files = count_files(ROOT / "src", "*.rs")
    maps = count_files(ROOT / "data/maps", "*.json")
    vehicle_parts = count_files(ROOT / "assets/vehicles", "*.png")
    props = count_files(ROOT / "assets/props", "*.png")
    characters = count_files(ROOT / "assets/characters", "*.png")

    blockers = []
    if not (ROOT / "Cargo.toml").exists():
        blockers.append({"id": "B-001", "severity": "critical", "message": "No Bevy/Rust project (Cargo.toml missing)"})
    if maps == 0:
        blockers.append({"id": "B-002", "severity": "critical", "message": "No playable maps in data/maps/"})
    if vehicle_parts == 0:
        blockers.append({"id": "B-003", "severity": "high", "message": "No vehicle part assets"})
    if props == 0:
        blockers.append({"id": "B-004", "severity": "medium", "message": "No props pack"})
    if not tiles.get("complete"):
        blockers.append({"id": "B-005", "severity": "low", "message": "Environment tiles incomplete vs manifest"})
    blockers.append({"id": "B-006", "severity": "info", "message": "Environment QA formal scoring pending"})

    registry_path = ROOT / "production/branches/registry.json"
    branches = {"active": 0, "planned": 0, "merged": 0}
    if registry_path.exists():
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        branches["active"] = len(reg.get("active_branches", []))
        branches["planned"] = len(reg.get("planned_branches", []))
        branches["merged"] = len(reg.get("merged_branches", []))

    bevy_exists = (ROOT / "Cargo.toml").exists()
    tools_count = sum(1 for p in (ROOT / "tools").iterdir() if p.is_dir()) if (ROOT / "tools").exists() else 0

    studio_health = {
        "documentacion": {"status": "green", "note": f"{count_files(ROOT / 'docs', '*.md')} docs"},
        "arte": {"status": "green" if tiles.get("complete") else "yellow", "note": f"{env_png} env PNGs"},
        "runtime": {
            "status": "green" if bevy_exists and maps > 0 else ("yellow" if bevy_exists else "red"),
            "note": "Foundation Runtime Sprint 01",
        },
        "gameplay": {"status": "red", "note": "No playable loop yet"},
        "herramientas": {"status": "yellow" if tools_count >= 6 else "red", "note": f"{tools_count} tool dirs"},
        "qa": {"status": "yellow", "note": "Env QA formal pending"},
        "produccion": {"status": "green" if tiles.get("complete") else "yellow", "note": "Environment pack done"},
        "riesgo_tecnico": {
            "status": "yellow" if not bevy_exists else "green",
            "note": "Bevy not initialized" if not bevy_exists else "Runtime in progress",
        },
    }

    state = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": detect_phase(),
        "brand_adr": "proposed",
        "bevy_project": (ROOT / "Cargo.toml").exists(),
        "assets": {
            "environment_png": env_png,
            "environment_tiles_manifest": tiles["manifest_total"],
            "environment_tiles_generated": tiles["generated_total"],
            "environment_complete": tiles["complete"],
            "vehicle_parts": vehicle_parts,
            "props": props,
            "characters": characters,
            "qa_scored": 0,
            "qa_rejected": 0,
        },
        "code": {
            "rust_files": rust_files,
            "maps": maps,
        },
        "world": {
            "neighborhoods": 0,
            "pois_defined": 11,
            "circuits": 0,
        },
        "features": scan_features(),
        "branches": branches,
        "studio_health": studio_health,
        "blockers": blockers,
        "documentation": {
            "agents": count_files(ROOT / "agents", "*.md"),
            "docs": count_files(ROOT / "docs", "*.md"),
            "adrs": count_files(ROOT / "decisions", "ADR-*.md"),
            "lore": count_files(ROOT / "lore", "*.md"),
        },
    }

    metrics_dir = ROOT / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    (metrics_dir / "project_state.json").write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (metrics_dir / "studio_health.json").write_text(
        json.dumps(studio_health, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    dashboard = f"""# Project Dashboard

**Generated:** {state["generated_at"]}  
**Phase:** `{state["phase"]}`  
**Scan:** `python scripts/studio_scan.py`

## Studio Health

| Métrica | Estado | Nota |
|---|---|---|
"""
    labels = {
        "documentacion": "Documentación",
        "arte": "Arte",
        "runtime": "Runtime",
        "gameplay": "Gameplay",
        "herramientas": "Herramientas",
        "qa": "QA",
        "produccion": "Producción",
        "riesgo_tecnico": "Riesgo técnico",
    }
    icons = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    for key, label in labels.items():
        h = studio_health[key]
        icon = icons.get(h["status"], "⚪")
        dashboard += f"| {label} | {icon} | {h['note']} |\n"

    dashboard += f"""
## Runtime

| Metric | Value |
|---|---|
| Bevy project | {"✅" if state["bevy_project"] else "❌"} |
| Rust files | {rust_files} |
| Playable maps | {maps} |
| Environment PNGs | {env_png} |
| Tiles generated | {tiles["generated_total"]}/{tiles["manifest_total"]} |

## Blockers

"""
    for blocker in blockers:
        dashboard += f"- **{blocker['severity'].upper()}** [{blocker['id']}] {blocker['message']}\n"

    dashboard += f"""
## Branches (registry)

| Type | Count |
|---|---|
| Active | {branches['active']} |
| Planned | {branches['planned']} |
| Merged | {branches['merged']} |

## Features

| Feature | Lifecycle | Open tasks |
|---|---|---|
"""
    for name, info in state["features"].items():
        lifecycle = info.get("lifecycle", info.get("status", "?"))
        dashboard += f"| {name} | {lifecycle} | {info['open_tasks']} |\n"

    (metrics_dir / "dashboard.md").write_text(dashboard, encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
