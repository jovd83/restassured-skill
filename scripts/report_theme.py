#!/usr/bin/env python3
"""Shared HTML reporting theme helpers for the Rest Assured skill family."""

from __future__ import annotations

from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def report_theme_path() -> Path:
    return skill_root() / "documentation" / "report-bundle" / "assets" / "report-theme.css"


def load_report_theme_css() -> str:
    return report_theme_path().read_text(encoding="utf-8")
