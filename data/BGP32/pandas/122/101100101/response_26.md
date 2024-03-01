## Bug Explanation
The bug in the provided function arises from the `canonicalize` function that is being used to sort the blocks before comparing them. The issue lies in accessing the block information incorrectly within the `canonicalize` function.

When calling `block` in the `canonicalize` function, it needs to access the `dtype` attribute directly, instead of using `block.dtype`. The correct usage should be `block._type`.

## Bug Fix Strategy
To fix this bug, we need to modify the `canonicalize` function to access the block type correctly by changing `block.dtype.name` to `block._type.name`.

## Corrected Version of the Function

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
        
        # canonicalize block order, using a tuple combining the type
        # name and then mgr_locs because there might be unconsolidated
        # blocks (say, Categorical) which can only be distinguished by
        # the iteration order
        def canonicalize(block):
            return (block._type.name, block.mgr_locs.as_array.tolist())
        
        self_blocks = sorted(self.blocks, key=canonicalize)
        other_blocks = sorted(other.blocks, key=canonicalize)
        return all(
            block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
        )
``` 

After applying the correction provided above, the `equals` function should now correctly compare the two `BlockManager` objects as expected.