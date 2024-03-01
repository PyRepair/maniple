### Bug Explanation
The bug in the `_cython_agg_blocks` function arises from the variable `agg_blocks` being returned as an empty list when it should contain computed blocks. This is due to a logic issue in the function related to the handling of blocks and their aggregation.

The incorrect behavior leads to no numeric types being aggregated as the function tries to aggregate data based on the `how` parameter but ends up with an empty `agg_blocks` list, ultimately causing a `DataError` to be raised.

### Bug Fix Strategy
To fix the bug in the `_cython_agg_blocks` function, we need to ensure that the computed aggregation blocks are added to the `agg_blocks` list correctly. This can be achieved by revisiting the aggregation logic for blocks in the provided code snippet.

### Corrected Function
Here is a corrected version of the `_cython_agg_blocks` function:

```python
def _cython_agg_blocks(
    self, how: str, alt=None, numeric_only: bool = True, min_count: int = -1
) -> "Tuple[List[Block], Index]":
    data: BlockManager = self._get_data_to_aggregate()

    if numeric_only:
        data = data.get_numeric_data(copy=False)

    agg_blocks: List[Block] = []
    new_items: List[np.ndarray] = []
    deleted_items: List[np.ndarray] = []
    split_items: List[np.ndarray] = []
    split_frames: List[DataFrame] = []

    no_result = object()

    for locs, block in data.iterate(return_indexer=True):
        result = no_result
        try:
            result, _ = self.grouper.aggregate(
                block.values, how, axis=1, min_count=min_count
            )
        except NotImplementedError:
            deleted_items.append(locs)
            continue

        if result is not no_result:
            result = maybe_downcast_numeric(result, block.dtype)
            agg_block: Block = block.make_block(result)
            agg_blocks.append(agg_block)
            new_items.append(locs)

    if not agg_blocks:
        raise DataError("No numeric types to aggregate")

    indexer = np.concatenate(new_items)
    agg_items = data.items.take(indexer)

    return agg_blocks, agg_items
```

This corrected version ensures that the aggregation is performed correctly and the resulting blocks are added to the `agg_blocks` list for successful return.