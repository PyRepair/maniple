### Analysis:
The error message indicates that there is a `KeyError: None` being raised in the function. This error occurs during the execution of the `get_loc` method in the `pivot` function. Specifically, the problem is within the line `index = MultiIndex.from_arrays([index, data[columns]])`. This line tries to create a `MultiIndex` object using the `index` and `data[columns]` values.

### Issues:
1. The error occurs when trying to create a `MultiIndex` object using the `index` parameter without proper handling.
2. The `None` key is not being properly handled in this line, leading to the `KeyError`.

### Bug Fix Strategy:
To fix this bug, we need to determine if the `index` is `None` before attempting to create a `MultiIndex` object. If the `index` is `None`, we should proceed with the existing index of the DataFrame.

### Corrected Function:
```python
from pandas.util._decorators import Appender, Substitution
from pandas.core.dtypes.common import is_integer_dtype, is_list_like, is_scalar
from pandas.core.frame import _shared_docs
from pandas.core.indexes.api import Index, MultiIndex, get_objs_combined_axis
from pandas import DataFrame

@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: DataFrame, index=None, columns=None, values=None) -> DataFrame:
    if values is None:
        cols = [columns] if index is None else [index, columns]
        append = index is None
        indexed = data.set_index(cols, append=append)
    else:
        if index is None:
            index = data.index
        else:
            index = data[index]

        if columns is not None:
            index = MultiIndex.from_arrays([index, data[columns]])
            
        if is_list_like(values) and not isinstance(values, tuple):
            indexed = data._constructor(
                data[values].values, index=index, columns=values
            )
        else:
            indexed = data._constructor_sliced(data[values].values, index=index)

    return indexed.unstack(columns)
```

### Explanation:
1. Added a check for `columns is not None` before attempting to create the `MultiIndex` object.
2. Only create the `MultiIndex` if the `columns` parameter is provided in the function call.
3. This fix will ensure that the `KeyError: None` is resolved by handling the `None` key appropriately when constructing the `MultiIndex`.

### This corrected version of the `pivot` function should now pass the failing test related to the reported issue.