from dataclasses import dataclass
from abc import ABC

@dataclass(frozen = True)
class HyNode(ABC):
	id: bytes
	name: str

	@property
	def is_file(self):
		return isinstance(self, HyNodeFile)

	@property
	def is_dir(self):
		return isinstance(self, HyNodeDirectory)