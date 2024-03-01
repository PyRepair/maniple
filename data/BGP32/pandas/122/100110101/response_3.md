### Analysis:
The `equals` function compares two `BlockManager` instances for equality. The failing test `test_dataframe_not_equal` creates two DataFrames with columns in different order and expects the `equals` function to return `False`. The error message shows that the function is incorrectly returning `True` instead of `False`.

#### Issue:
The issue lies in how the function sorts and compares the `blocks` attribute of the `BlockManager` instances. The function `canonicalize` sorts the blocks based on the block's datatype and mgr_locs. When comparing the sorted blocks, it should compare the content of each block instead of the block objects themselves.

#### Strategy for fixing the bug:
1. Update the `canonicalize` function to extract essential information from the blocks.
2. Modify the comparison of sorted blocks to compare the contents instead of the block objects.

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

    def extract_block_info(block):
        return block.values

    self_blocks = sorted(self.blocks, key=extract_block_info)
    other_blocks = sorted(other.blocks, key=extract_block_info)
    return all(
        np.array_equal(block, oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

Now, with the updated `extract_block_info` function that extracts the block values, and comparison using `np.array_equal`, the function should correctly compare the blocks' contents and return `False` for the test case provided.