GitHub Bug Title:
Error Message Raised Incorrectly for columns=None in df.pivot

Description:
The error message currently indicates that columns is optional in df.pivot, however, the documentation states that it is not. This should be clarified to reflect that columns is not optional.

Expected Output:
When using df.pivot with columns=None, a KeyError should be raised indicating that columns cannot be None.

Environment:
- Python: 3.7.3.final.0
- pandas: 1.0.1
- numpy: 1.18.1