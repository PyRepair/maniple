The error message "No matching signature found" indicates that the `round` method fails when the columns are a `CategoricalIndex` made from an `IntervalIndex`. The `pd.cut` function creates these types of values, which can appear in columns when using `pivot_table`. The expected output is that the rounding operation should work as normal.

The error occurs in the `get_indexer` method of the `IntervalIndex` class. This method encounters difficulty in processing the interval data type, possibly due to the absence of an appropriate method signature. This absence leads to the TypeError being raised, resulting in the failed test case.

To fix the bug:

1. Implement a conditional check at the beginning of the `get_indexer` method to handle cases where the input `target` is a `CategoricalIndex` made from an `IntervalIndex`.
2. Change the logic for indexing and handling `IntervalIndex` objects to ensure that appropriate operations are performed without encountering a TypeError.

Here's the corrected version of the `get_indexer` method:

```python
@Substitution(
    **dict(
        _index_doc_kwargs,
        **{
            "raises_section": textwrap.dedent(
                """
    Raises
    ------
    NotImplementedError
        If any method argument other than the default of
        None is specified as these are not yet implemented.
    """
            )
        },
    )
)
@Appender(_index_shared_docs["get_indexer"])
def get_indexer(
    self,
    target: AnyArrayLike,
    method: Optional[str] = None,
    limit: Optional[int] = None,
    tolerance: Optional[Any] = None,
) -> np.ndarray:

    if isinstance(target, CategoricalIndex) and isinstance(target.values, IntervalIndex):
        # Handle CategoricalIndex made from an IntervalIndex
        target_as_index = target.values
    else:
        target_as_index = ensure_index(target)

    self._check_method(method)

    if self.is_overlapping:
        msg = (
            "cannot handle overlapping indices; use "
            "IntervalIndex.get_indexer_non_unique"
        )
        raise InvalidIndexError(msg)

    if isinstance(target_as_index, IntervalIndex):
        # rest of the code remains unchanged
        # ...
        # ...

    return ensure_platform_int(indexer)
```

In this corrected version, we first check if the `target` input is a `CategoricalIndex` made from an `IntervalIndex`. If it is, we extract the `IntervalIndex` from the `CategoricalIndex` and proceed with the rest of the method. This modification addresses the issue of the `round` method failing when columns are a `CategoricalIndex` of `IntervalIndex`.