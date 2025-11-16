from typing import Hashable, Any

from app.node import Node
from copy import deepcopy


class Dictionary:
    initial_capacity = 8
    load_factor = 2 / 3

    def __init__(self) -> None:
        self.current_capacity = Dictionary.initial_capacity
        self.nodes = [None] * self.current_capacity
        self.size = 0

    def find_slot(self, key: Hashable) -> int:

        index = self.calculate_index(key)
        start_index = index

        while True:
            node = self.nodes[index]
            if node is None:
                return index

            if node.key == key:
                return index

            index = (index + 1) % self.current_capacity
            if index == start_index:
                raise RuntimeError("Hashtable is full (probing failed)")

    def search_item(self, key: Hashable) -> int:
        index = self.calculate_index(key)
        start_index = index

        while True:
            node = self.nodes[index]
            if node is None:
                raise KeyError(f"No such key as {key}")
            if node.key == key:
                return index
            index = (index + 1) % self.current_capacity
            if index == start_index:
                raise KeyError(f"No such key as {key}")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.is_reached_resize():
            self.resize()
        slot = self.find_slot(key)
        node = self.nodes[slot]
        if node is None:
            self.size += 1
        self.nodes[slot] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Node:
        index = self.search_item(key)
        return self.nodes[index].value

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self.search_item(key)
        self.nodes[index] = None
        self.size -= 1

    def pop(self, key: Hashable, default: Any | None = None) -> Node:
        try:
            index = self.search_item(key)
        except KeyError:
            if default is not None:
                return default
            raise

        node = self.nodes[index]
        self.nodes[index] = None
        self.size -= 1
        return node.value

    def resize(self) -> None:
        nodes_copy = deepcopy(self.nodes)
        self.nodes = [None] * (self.current_capacity * 2)
        self.current_capacity = len(self.nodes)
        self.size = 0
        for node in nodes_copy:
            if isinstance(node, Node):
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        self.current_capacity = Dictionary.initial_capacity
        self.nodes = [None] * self.current_capacity
        self.size = 0

    def is_reached_resize(self) -> bool:
        return self.size == int(self.current_capacity * Dictionary.load_factor)

    def calculate_index(self, key: Hashable) -> int:
        return hash(key) % self.current_capacity
