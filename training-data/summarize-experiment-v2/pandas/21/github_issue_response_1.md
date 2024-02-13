GitHub Bug Title:
Inconsistent behavior of list indexers in series index

Description:
When using list indexers in a series index, it behaves differently from array-like indexers. It raises a KeyError for list indexers, while it works as expected for array-like indexers. This behavior is inconsistent and does not match the expected behavior for ser.loc[key].

Expected Output:
List indexers in a series index should work consistently with array-like indexers and ser.loc[key].

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0