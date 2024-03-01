Potential error locations in the buggy function:
1. Comparing the lengths of `self_axes` and `other_axes` without considering potential differences.
2. Sorting `self.blocks` and `other.blocks` using a key function that might not be handling all possible cases correctly.

Cause of the bug:
The bug in the given function arises from comparing `self_axes` and `other_axes` without considering that the order of axes might be different. Additionally, sorting the blocks based on a key function that may not handle all cases correctly can lead to incorrect comparisons.

Strategy for fixing the bug:
To fix the bug, we need to ensure that the comparison between `self_axes` and `other_axes` considers all possible cases, such as different order of axes. Additionally, the key function used for sorting blocks should be able to handle all block types correctly.

Corrected version of the function:

```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if set(self_axes) != set(other_axes):
        return False

    self._consolidate_inplace()
    other._consolidate_inplace()
    
    if len(self.blocks) != len(other.blocks):
        return False

    def canonicalize(block):
        return (type(block).__name__, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

In the corrected version:
- Changed the comparison of `self_axes` and `other_axes` to use sets to compare the axes irrespective of the order.
- Modified the `canonicalize` function to use the type name of the block for sorting.
- Added `type(block).__name__` when creating the tuple in the canonicalize function for better handling of block types.