# GitHub Issue: Categorical NaN Not Converted to Int Correctly

## Description:
When converting categorical series back into an Int column, NaN is unexpectedly converted to a negative integer value. This behavior is not as expected and can cause issues.

### Expected Output:
NaN in the category should convert to NaN in IntX (nullable integer) or float.

### Versions: 
- Python: 3.7.4.final.0
- Pandas: 0.25.1
- Numpy: 1.17.2