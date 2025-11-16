from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = self.__hash__()
        self.value = value

    def __hash__(self) -> int:
        return hash(self.key)
