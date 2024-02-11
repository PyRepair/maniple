input_param = {
    "numeric_only": "True",
    "how": "'mean'",
    "min_count": "-1",
    "self.obj": "DataFrame",
    "self.axis": "0"
}

output = {
    "data": "BlockManager",
    "agg_blocks": "[FloatBlock: slice(0, 1, 1), 1 x 3, dtype: float64]",
    "new_items": "[array([0])]",
    "deleted_items": "[]",
    "split_items": "[]",
    "split_frames": "[]",
    "block": "ExtensionBlock: slice(0, 1, 1), 1 x 9, dtype: Int64",
    "data.blocks": "(ExtensionBlock: slice(0, 1, 1), 1 x 9, dtype: Int64,)",
    "result": "array([[1.5, 1.5, 1.5]])",
    "locs": "array([0])",
    "block.mgr_locs": "BlockPlacement(slice(0, 1, 1))",
    "block.values": "<IntegerArray>[1, <NA>, 2, 1, <NA>, 2, 1, <NA>, 2]",
    "data.items": "Index(['b'], dtype='object')",
    "result.ndim": "2",
    "block.dtype": "Int64Dtype()",
    "block.is_extension": "True",
    "result.shape": "(1, 3)",
    "agg_block": "FloatBlock: slice(0, 1, 1), 1 x 3, dtype: float64",
    "loc": "1",
    "locs.dtype": "dtype('int64')",
    "indexer": "array([0])",
    "agg_items": "Index(['b'], dtype='object')",
    "offset": "1",
    "blk": "FloatBlock: slice(0, 1, 1), 1 x 3, dtype: float64",
    "blk.mgr_locs": "BlockPlacement(slice(0, 1, 1))"
}
print(input_param)
print(output)