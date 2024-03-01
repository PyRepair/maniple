### Bug Explanation:
The bug in the `equals` function lies in the sorting mechanism for `self_blocks` and `other_blocks` using the `canonicalize` function. The `canonicalize` function attempts to create a key for sorting by combining the data type name and manager locations of a block. However, the bug arises from how it handles extracting `mgr_locs.as_array.tolist()`, which should be `mgr_locs.as_array.tolist()` instead. The incorrect method call causes a AttributeError during execution, leading to incorrect sorting and ultimately, incorrect equality checking.

### Bug Fix Strategy:
To fix the bug, we need to correct the method call by removing the unnecessary `as_array` segment. By using `mgr_locs.tolist()` as intended, we can properly create a sortable key for each block. This change should prevent the AttributeError and ensure correct sorting, leading to accurate equality comparisons.

### Corrected Version:

```python
def canonicalize(block):
    return (block.dtype.name, block.mgr_locs.tolist())

self_blocks = sorted(self.blocks, key=canonicalize)
other_blocks = sorted(other.blocks, key=canonicalize)
return all(
    block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
)
```