GitHub Bug Title:
TypeError for pivot_table function with multi-index columns only

Description:
When using the pivot_table function with multi-index columns, a TypeError occurs, and it does not work symmetrically between rows/columns and single/multi case.

Expected Output:
No error should occur when using the pivot_table function with multi-index columns, and it should work symmetrically between rows/columns and single/multi case.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0