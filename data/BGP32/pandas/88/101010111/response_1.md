### Bug Location and Cause:
The bug occurs in the `pivot_table` function of the `pivot.py` file due to incorrect handling when calling the `pivot_table` function recursively for each function in the `aggfunc` list. This results in an incorrect DataFrame structure that causes attribute errors thereafter.

When the `aggfunc` parameter is a list, the faulty section in the `pivot_table` function recursively calls itself for each function in the list without correctly handling the output structure. This causes the series object, which doesn't have a `columns` attribute, to be passed onward, leading to an AttributeError when trying to access the `columns` attribute later on.

### Bug Fix Strategy:
To fix the bug, the recursive call handling for each function in the `aggfunc` list should ensure that the final output maintains its DataFrame structure, thereby avoiding the AttributeError issue. This can be achieved by properly constructing and accumulating the DataFrame pieces during the recursive calls. 

Here is a corrected version of the `pivot_table` function that addresses the bug and aligns with the expected input/output values in the described test cases:

```python
def pivot_table(
    data,
    values=None,
    index=None,
    columns=None,
    aggfunc="mean",
    fill_value=None,
    margins=False,
    dropna=True,
    margins_name="All",
    observed=False,
) -> "DataFrame":
    index = _convert_by(index)
    columns = _convert_by(columns)

    if isinstance(aggfunc, list):
        pieces: List[DataFrame] = []
        keys = []
        for func in aggfunc:
            table = pivot_table(
                data,
                values=values,
                index=index,
                columns=columns,
                fill_value=fill_value,
                aggfunc=func,
                margins=False,  # Disable margins in recursive calls
                dropna=dropna,
                margins_name=margins_name,
                observed=observed,
            )
            pieces.append(table)
            keys.append(getattr(func, "__name__", func))

        if all(isinstance(piece, ABCDataFrame) for piece in pieces):
            # Concatenate DataFrame pieces only
            return concat(pieces, keys=keys, axis=1)

    keys = index + columns
    ...
```

This revised version enhances the handling of the recursive call during the aggregation phase, ensuring that only DataFrames are concatenated at the end. Additionally, the recursive calls during aggregation disable margins to prevent any discrepancies in the resulting DataFrame structure.

By using this corrected `pivot_table` function, all the described test cases should pass successfully without triggering any attribute errors, providing the expected DataFrame structures.