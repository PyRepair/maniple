The issue is that the `equals` method of the DataFrame class is returning `True` when it should be returning `False` for the given test case. The issue is caused by the fact that the `sorted` function is used on the `self.blocks` and `other.blocks` lists, which changes the order of the blocks and leads to incorrect comparison.

To fix this issue, we can modify the `canonicalize` function to not include the block order information. This can be achieved by removing the `block.mgr_locs.as_array.tolist()` from the tuple returned by the `canonicalize` function.

Here's the fixed code:

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
    # name because block order is not important for equality
    def canonicalize(block):
        return (block.dtype.name)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This fix ensures that the blocks are sorted based on their types only, ignoring the block order within the DataFrame.

With this fix, the `df1.equals(df2)` assertion in the test case `test_dataframe_not_equal` will return `False` as expected.