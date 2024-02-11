Case 1:
- Input value and type
obj, type: DataFrame
axis, type: int
key, type: str
obj.index, type: Int64Index
obj.columns, type: Int64Index
obj._data, type: BlockManager
validate, type: bool
obj.shape, type: tuple
sort, type: bool
observed, type: bool
mutated, type: bool
- Output value and type
group_axis, type: Int64Index
is_tuple, type: bool
all_hashable, type: bool
keys, type: list
match_axis_length, type: bool
any_callable, type: bool
any_groupers, type: bool
any_arraylike, type: bool
levels, type: list
groupings, type: list
exclusions, type: list
gpr, type: str
i, type: int

Case 2:
- Input value and type
obj, type: DataFrame
axis, type: int
key, type: list
obj.index, type: Int64Index
obj.columns, type: Int64Index
obj._data, type: BlockManager
validate, type: bool
obj.shape, type: tuple
sort, type: bool
observed, type: bool
mutated, type: bool
- Output value and type
group_axis, type: Int64Index
is_tuple, type: bool
all_hashable, type: bool
keys, type: list
match_axis_length, type: bool
any_callable, type: bool
any_groupers, type: bool
any_arraylike, type: bool
levels, type: list
groupings, type: list
exclusions, type: list
gpr, type: str
i, type: int