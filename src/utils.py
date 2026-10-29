"""
Health 360: Utility Functions & Logging Infrastructure
"""

import json
import logging
import os
import random
from pathlib import Path
from typing import Any, Dict, Optional
import numpy as np
import pandas as pd


def setup_logger(name: str = "health360", log_file: Optional[Path] = None, level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a standardized logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console Handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # Optional File Handler
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
    return logger


def set_seed(seed: int = 42) -> None:
    """Sets random seeds for reproducibility across random, numpy."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def load_json(filepath: Path) -> Dict[str, Any]:
    """Loads a JSON file with error handling."""
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """Saves dictionary to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)


def format_percentage(val: float, decimals: int = 2) -> str:
    """Formats float as percentage string."""
    return f"{val * 100:.{decimals}f}%"
