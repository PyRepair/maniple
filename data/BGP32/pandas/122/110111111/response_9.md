The issue with the `equals` function in the `BlockManager` class is that it wrongly returns `True` when comparing two DataFrames with identical blocks but in different locations. This behavior leads to failing tests where the expected output should be `False`.

#### Cause of the Bug:
1. The function compares the axes of two `BlockManager` instances and then iterates over the blocks within each instance.
2. If the number of blocks differs in the two instances, the function incorrectly returns `False`.
3. The function then sorts the blocks based on their type name and `mgr_locs`, resulting in the main issue: even if the blocks are identical, but their locations are different, the function erroneously returns `True`.

#### Fixing the Bug:
To correct the issue, we need to modify the block comparison logic. Instead of comparing based on sorted blocks, we should directly iterate over the blocks and ensure that corresponding blocks match in `equals`.

Here is the corrected version of the `equals` function:

```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    
    # Compare axes
    if not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False
    
    self._consolidate_inplace()
    other._consolidate_inplace()
    
    if len(self.blocks) != len(other.blocks):
        return False
    
    # Compare blocks directly, ensuring that corresponding blocks are equal
    for block, oblock in zip(self.blocks, other.blocks):
        if not block.equals(oblock):
            return False
        
    return True
```

This corrected version will compare the blocks directly, ensuring that even if the block locations are different, as long as the content matches, the function will correctly return `False` when comparing the provided failing test cases.

By implementing this change, the issue mentioned in the GitHub thread should be resolved, and the failing test `test_dataframe_not_equal` should pass as expected.