### Bug Analysis:
1. The `equals` function in the `BlockManager` class is intended to compare two instances of `BlockManager` and return `True` if they are equal.
2. The bug arises because the function compares blocks based on their memory locations rather than their content.
3. The failing test `test_dataframe_not_equal` creates two dataframes with swapped columns and expects the `equals` function to return `False`.
4. The error message shows that the function returned `True` instead of `False`, indicating a comparison issue.
5. The comparison logic in the buggy function sorts the blocks by memory location, leading to incorrect equality determination.

### Bug Fix Strategy:
To fix the bug, we need to modify the comparison logic in the `equals` function to compare the content of the blocks instead of their memory locations. We can sort the blocks based on their content before comparing them.

### Corrected Version:
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    if not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False
    self._consolidate_inplace()
    other._consolidate_inplace()
    if len(self.blocks) != len(other.blocks):
        return False

    # canonicalize block content, not based on memory locations
    def canonicalize(block):
        return block.values.tostring()

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By making the change above, the `equals` function should now correctly compare the content of the blocks within the `BlockManager` instances, resolving the issue and passing the failing test case.