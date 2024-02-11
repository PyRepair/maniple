## Short Version of Runtime Input and Output Value Pair

### Case 1
- Input:
  - current_line.depth: 0
  - current_line: Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=Leaf(NAME, 'property'), ...inside_brackets=False)
  - current_line.leaves: [Leaf(AT, '@'), Leaf(NAME, 'property')]
  - self.previous_defs: []
  - current_line.is_decorator: True

- Variables at Return:
  - max_allowed: 2
  - first_leaf: Leaf(AT, '@')
  - before: 0
  - first_leaf.prefix: ''
  - depth: 0
  - is_decorator: True

### Case 2
- Input:
  - current_line.depth: 0
  - current_line: Line(depth=0, leaves=[Leaf(153, '# TODO: X')], comments=[], bracket_tracker=BracketTracker(depth=0, bracket_match={}, delimiters={}, previous=None, ...inside_brackets=False)
  - current_line.leaves: [Leaf(153, '# TODO: X')]
  - self.previous_defs: []
  - current_line.is_decorator: False

- Variables at Return:
  - max_allowed: 2
  - first_leaf: Leaf(153, '# TODO: X')
  - before: 0
  - first_leaf.prefix: ''
  - depth: 0
  - is_decorator: False

### Case 7
- Input:
  - current_line.depth: 0
  - current_line: Line(depth=0, leaves=[Leaf(NAME, 'def'), Leaf(NAME, 'foo'), Leaf(LPAR, '('), Leaf(RPAR, ')'), Leaf(COLON, ':')], comments=[], ...inside_brackets=False)
  - current_line.leaves: [Leaf(NAME, 'def'), Leaf(NAME, 'foo'), Leaf(LPAR, '('), Leaf(RPAR, ')'), Leaf(COLON, ':')]
  - self.previous_defs: []
  - current_line.is_def: True

- Variables at Return:
  - max_allowed: 2
  - first_leaf: Leaf(NAME, 'def')
  - before: 0
  - first_leaf.prefix: ''
  - depth: 0
  - self.previous_defs: [0]
  - self: EmptyLineTracker(previous_line=Line(depth=0, leaves=[Leaf(AT, '@'), Leaf(NAME, 'property')], ...inside_brackets=False), previous_after=0, previous_defs=[0])
  - is_decorator: False