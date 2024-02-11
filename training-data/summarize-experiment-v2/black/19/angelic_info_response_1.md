Case 1:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool

Case 2:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool

Case 3:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool
  - newlines, type: int

Case 4:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool

Case 5:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool

Case 6:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool
  - newlines, type: int

Case 7:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - self.previous_defs, type: list
  - self, type: EmptyLineTracker
  - is_decorator, type: bool

Case 8:
- current_line.depth, type: int
- current_line, type: Line
- current_line.leaves, type: list
- self.previous_defs, type: list
- self, type: EmptyLineTracker
- current_line.is_decorator, type: bool
- Expected:
  - max_allowed, type: int
  - first_leaf, type: Leaf
  - before, type: int
  - first_leaf.prefix, type: str
  - depth, type: int
  - is_decorator, type: bool