After examining the buggy function and the expected input/output values, the bug appears to be related to the aggregation process of the data blocks. It seems that the issue might stem from the way the operation is handled when handling non-numeric data blocks. The implementation does not properly exclude the non-numeric blocks or handle them when trying to perform aggregation operations like mean, median, or variance.

To fix the bug, we need to adjust the logic to properly handle non-numeric data blocks when performing aggregation operations. Specifically, we need to address cases where alt is not defined (when how is not 'ohlc') and deal with non-numeric data blocks appropriately.

Here is the corrected version of the function:

```python
    def _cython_agg_blocks(
        self, how: str, alt=None, numeric_only: bool = True, min_count: int = -1
    ) -> "Tuple[List[Block], Index]":
        data: BlockManager = self._get_data_to_aggregate()

        if numeric_only:
            data = data.get_numeric_data(copy=False)

        agg_blocks: List[Block] = []
        new_items: List[np.ndarray] = []
    
        for block in data.blocks:
            if not block.is_numeric:
                continue
            
            locs = block.mgr_locs.as_array
            result = no_result
            
            try:
                result, _ = self.grouper.aggregate(
                    block.values, how, axis=1, min_count=min_count
                )
            except NotImplementedError:
                if alt is None:
                    deleted_items.append(locs)
                    continue

                obj = self.obj[data.items[locs]]
                if obj.shape[1] == 1:
                    obj = obj.iloc[:, 0]

                s = get_groupby(obj, self.grouper)
                result = s.aggregate(lambda x: alt(x, axis=self.axis))

            if result is not no_result:
                result = maybe_downcast_numeric(result, block.dtype)
                agg_block = block.make_block(result)
                new_items.append(locs)
                agg_blocks.append(agg_block)

        if not agg_blocks:
            raise DataError("No numeric types to aggregate")
        
        agg_items = data.items.take(np.concatenate(new_items))

        offset = 0
        for blk in agg_blocks:
            loc = len(blk.mgr_locs)
            blk.mgr_locs = np.arange(offset, offset + loc)
            offset += loc

        return agg_blocks, agg_items
```

This revised version adjusts the logic to only perform aggregation on numeric data blocks, skipping non-numeric blocks. The function now correctly handles cases where the alt function is not defined and excludes non-numeric blocks from the aggregation process.