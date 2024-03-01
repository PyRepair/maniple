### Analysis:
1. The `equals` function in the `BlockManager` class is meant to compare two `BlockManager` instances for equality.
2. The function compares the axes of the two instances, consolidates them, and then compares the blocks within them.
3. The bug occurs in comparing the blocks due to not handling the block locations correctly.
4. The failing test is checking if two DataFrames with swapped columns are equal.

### Bug Cause:
The bug occurs because the function expects blocks in a specific order, but when the block locations are different, the comparison fails.

### Fix Strategy:
1. Sort the blocks based on block type and location to handle unconsolidated blocks.
2. Update the comparison logic to compare the sorted blocks.

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

    # Sort blocks based on type and location
    def canonicalize(block):
        return (type(block).__name__, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    # Compare sorted blocks
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

### Updated Test:
```python
def test_dataframe_not_equal():
    # see GH28839
    df1 = pd.DataFrame({"a": [1, 2], "b": ["s", "d"]})
    df2 = pd.DataFrame({"a": ["s", "d"], "b": [1, 2]})
    assert df1.equals(df2) is False
```

Now, the corrected `equals` function should pass the failing test and address the issue mentioned on GitHub.