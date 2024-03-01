The bug in the `equals` function stems from the comparison of blocks based on their order rather than content. The function needs to compare the blocks based on their actual data, not just their locations or dtype. 

To fix the bug, we should compare blocks based on their data, and not on their positions or dtype. We can achieve this by extracting the data from each block and comparing it directly.

Here is the corrected version of the `equals` function:

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

    self_blocks_data = [block.values for block in self.blocks]
    other_blocks_data = [block.values for block in other.blocks]
    
    return all(
        np.array_equal(block_data, other_block_data) 
        for block_data, other_block_data in zip(self_blocks_data, other_blocks_data)
    )
```

This corrected version compares the actual data within each block of the `self` and `other` `BlockManager` objects, ensuring a proper comparison based on content rather than order or type.

By implementing this change, the function will correctly identify if `self` and `other` have equal contents regardless of the order or dtype of the blocks.