### Bug Explanation
The bug in the `equals` function arises due to the comparison of the `self.blocks` and `other.blocks`. The comparison relies on the ordering of the blocks which might not be consistent if the blocks are unconsolidated. In the failing test case, the DataFrames `df1` and `df2` have the columns `a` and `b` swapped, leading to a comparison failure.

### Bug Fix Strategy
To fix the bug, we need to ensure that the comparison of the blocks is performed correctly, regardless of the order of columns in the DataFrames. One way to achieve this is by iterating over the blocks in a more structured manner that does not solely rely on the order of the blocks.

### Corrected Code
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
    
    self_blocks_dict = {block.block_id: block for block in self.blocks}
    other_blocks_dict = {block.block_id: block for block in other.blocks}
    
    if len(self_blocks_dict) != len(other_blocks_dict):
        return False
    
    for block_id in self_blocks_dict:
        if block_id not in other_blocks_dict:
            return False
        if not self_blocks_dict[block_id].equals(other_blocks_dict[block_id]):
            return False

    return True
```

With this corrected code, we iterate over the blocks using dictionaries to ensure a consistent comparison even if the order is different. This modification should address the bug and make the function pass the failing test cases.