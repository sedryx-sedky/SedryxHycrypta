from dataclasses import dataclass
from typing import Optional

@dataclass(frozen = True)
class HyNodeFile(HyNode):
	entension: str
	encrypted_path: Path
	path: Optional[Path] = None