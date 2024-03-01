### Bug Explanation
The bug in the `equals` function arises from comparing two DataFrames (`self` and `other`) where the column order is different but the data within the columns is the same. The function currently checks for equality based on the column order as well, which leads to a false assertion failure.

### Bug Fix Strategy
To fix the bug, we need to modify the `equals` function to only check for equality in terms of the data contained in the DataFrames, disregarding the column order.

### Corrected Function
```python
def equals(self, other):
    if self.shape != other.shape:
        return False
    
    # Check for equality regardless of column order
    for self_col in self:
        self_data = self[self_col].values
        other_col = other[self_col]
        if not self_data.equals(other_col):
            return False
    
    return True
```

This corrected function will compare the data in each column of `self` with the corresponding column in `other` without considering the column order, which aligns with the expected behavior.