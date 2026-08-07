"""Bounded governed execution engine for AION/Astra runtime candidates."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aion_governance_kernel.pipeline import run_pipeline
from astra_engineering_workbench.approvals import create_approval