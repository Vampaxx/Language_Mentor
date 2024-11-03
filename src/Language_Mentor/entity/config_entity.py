from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    Model_name              : str 
    temperature             : int 
    api_key                 : Optional[str]