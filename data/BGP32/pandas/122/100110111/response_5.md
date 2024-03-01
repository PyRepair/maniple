### Analysis:
- The function `equals` is used to compare two `BlockManager` objects which contain multiple blocks of data.
- The failing test `test_dataframe_not_equal` creates two dataframes where the data types of columns `a` and `b` are interchanged. The test expects the `equals` function to return `False`.
- The error message indicates that the comparison is returning `True` instead of `False`.

### Errors:
1. The function is not correctly comparing the blocks within `BlockManager`.
2. It is not handling the case where the locations of blocks are different due to unconsolidated blocks like `Categorical`.

### Bug Cause:
The bug is caused by the comparison mechanism within the function. It is not handling the case where block locations are different.

### Strategy for Fixing:
1. Modify the comparison function to consider the block locations when comparing blocks.
2. Implement a mechanism to compare the block locations accurately.

### Corrected Version of the Function:
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

    self_blocks = sorted(self.blocks, key=lambda block: block_ids(block))
    other_blocks = sorted(other.blocks, key=lambda block: block_ids)

    return all(
        block_id_equals(block, oblock)
        for block, oblock in zip(self_blocks, other_blocks)
    )

def block_ids(block):
    # This function returns a tuple containing identifiers of the block
    return (block.dtype.name, block.values.nbytes, block._simple_block_type)

def block_id_equals(block, oblock):
    # Compare block locations as well
    if block_ids(block) != block_ids(oblock):
        return False
    if block.shape != oblock.shape:
        return False
    if not isna(block._inv_mgr_locs).equals(oblock._inv_mgr_locs):
        return False
    return block.values.equals(oblock.values)
```  

### Modification Explanation:
1. I have defined `block_ids` function to generate an identifier tuple for a block based on data type, size, and block type.
2. `block_id_equals` function compares the identifiers along with the block shape, location, and values for accurate comparison.
3. The sorting of blocks is done based on the identifiers using `block_ids` function.
4. The comparison mechanism ensures that block locations are considered during comparison.

By implementing these changes, the function should correctly handle the comparison of `BlockManager` objects with different block locations.