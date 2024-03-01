```python
def _cython_agg_blocks(
        self, how: str, alt=None, numeric_only: bool = True, min_count: int = -1
    ) -> "Tuple[List[Block], Index]":
        data: BlockManager = self._get_data_to_aggregate()

        if numeric_only:
            data = data.get_numeric_data(copy=False)

        agg_blocks: List[Block] = []
        new_items: List[np.ndarray] = []
        split_items: List[np.ndarray] = []
        split_frames: List[DataFrame] = []

        no_result = object()
        for block in data.blocks:
            locs = block.mgr_locs.as_array
            try:
                result, index = self.grouper.aggregate(
                    block, how, axis=self._axis, min_count=min_count
                )
            except NotImplementedError:
                if alt is None:
                    deleted_items.append(locs)
                    continue
                # call our grouper again with only this block
                obj = self.obj[data.items[locs]]
                s = get_groupby(obj, self.grouper)
                result = s.aggregate(lambda x: alt(x, axis=self.axis))

            if result is not no_result:
                result = maybe_downcast_numeric(result, block.dtype)
                agg_block: Block = make_block(result, placement=slice(None))

            new_items.append(locs)
            agg_blocks.append(agg_block)

        if not agg_blocks:
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