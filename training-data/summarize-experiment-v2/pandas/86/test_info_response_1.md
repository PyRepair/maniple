The original error message is:
```
KeyError: None
```

Stack frames where the error occurred:
- File "pandas/core/reshape/pivot.py", line 441 in pivot
- File "pandas/core/frame.py", line 2793 in __getitem__
- File "pandas/core/indexes/base.py", line 2903 in get_loc
- File "pandas/_libs/index.pyx", line 109 in get_loc
- File "pandas/_libs/index.pyx", line 136 in get_loc
- File "pandas/_libs/hashtable_class_helper.pxi", line 1614 in get_item
- File "pandas/_libs/hashtable_class_helper.pxi", line 1622 in get_item

Simplified error message:
```
KeyError: None
```