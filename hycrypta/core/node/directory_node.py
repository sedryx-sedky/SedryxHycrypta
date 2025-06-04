from dataclasses import dataclass
from salts import Salts

@dataclass(frozen = True)
class HyNodeDirectory(HyNode):
	key1: bytes
	key2: bytes
	salts: Salts