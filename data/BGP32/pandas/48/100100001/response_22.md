### Analysis:
The `_cython_agg_blocks` function is responsible for aggregating data blocks based on the specified operation (`how`) provided. The bug seems to reside in the logic of handling non-numeric data blocks when an exception is caught during aggregation.

### Potential Error Locations:
1. Exception handling block for `NotImplementedError`.
2. Handling of non-numeric data blocks.
3. Splitting of object-dtype blocks into `List[Block[T], Block[U]]`.

### Bug Cause:
The bug arises when the function encounters a `NotImplementedError` during aggregation of non-numeric data blocks and tries to perform an alternative operation (`alt`). The implementation is not handling this scenario correctly, leading to incorrect results and failing tests.

### Strategy for Fixing the Bug:
- Refactor the exception handling logic for `NotImplementedError`.
- Properly handle the alternative operation for non-numeric data blocks.
- Ensure correct handling of split object-dtype blocks.
- Update the aggregation logic to handle all scenarios correctly.

### Corrected Version of the Function:
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
    for block in data.blocks:
        result = no_result
        locs = block.mgr_locs.as_array
        try:
            result, _ = self.grouper.aggregate(
                block.values, how, axis=1, min_count=min_count
            )
        except NotImplementedError:
            if alt is None:
                raise
            else:
                result = alt(block.values)

        if isinstance(result, DataFrame):
            result = result._data.blocks[0].values

        if result is not no_result:
            result = maybe_downcast_numeric(result, block.dtype)
            agg_block: Block = block.make_block(result)
            new_items.append(locs)
            agg_blocks.append(agg_block)

    if not (agg_blocks or split_frames):
        raise DataError("No numeric types to aggregate")

    indexer = np.concatenate(new_items)
    agg_items = data.items.take(np.sort(indexer))

    offset = 0
    for blk in agg_blocks:
        loc = len(blk.mgr_locs)
        blk.mgr_locs = indexer[offset : (offset + loc)]
        offset += loc

    return agg_blocks, agg_items
```

By handling the alternative operation correctly and modifying the aggregation logic where necessary, the corrected version of the function should now pass the failing test cases.