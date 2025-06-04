from dataclasses import dataclass

@dataclass(frozen = True)
class Salts:
	password: bytes
	key: bytes
	file_lookup: bytes
	child_lookup: bytes