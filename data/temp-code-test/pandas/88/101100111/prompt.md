Please fix the buggy function provided below and output a corrected version.
Following these steps:
1. Analyze the buggy function and its relationship with related functions, test code, the expected input/output values, the GitHub issue.
2. Identify potential error locations within the buggy function.
3. Explain the cause of the bug using the buggy function, the related functions, the failing test, the expected input/output variable values, the GitHub Issue information.
4. Suggest a strategy for fixing the bug.
5. Given the buggy function below, provide a corrected version. The corrected version should pass the failing test, satisfy the expected input/output values, resolve the issue posted in GitHub.


Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
from typing import TYPE_CHECKING, Callable, Dict, List, Tuple, Union
from pandas.util._decorators import Appender, Substitution
from pandas.core.dtypes.cast import maybe_downcast_to_dtype
from pandas.core.dtypes.common import is_integer_dtype, is_list_like, is_scalar
from pandas.core.dtypes.generic import ABCDataFrame, ABCSeries
from pandas.core.frame import _shared_docs
from pandas.core.groupby import Grouper
from pandas.core.indexes.api import Index, MultiIndex, get_objs_combined_axis
from pandas.core.reshape.concat import concat
from pandas.core.reshape.util import cartesian_product
from pandas import DataFrame
from pandas import DataFrame
from pandas import DataFrame
```

## The source code of the buggy function
```python
# The relative path of the buggy file: pandas/core/reshape/pivot.py

# This function from the same file, but not the same class, is called by the buggy function
def pivot_table(data, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False) -> 'DataFrame':
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def _add_margins(table: Union['Series', 'DataFrame'], data, values, rows, cols, aggfunc, observed=None, margins_name: str='All', fill_value=None):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def _convert_by(by):
    # Please ignore the body of this function

# this is the buggy function you need to fix
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot_table"], indents=1)
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
                margins=margins,
                dropna=dropna,
                margins_name=margins_name,
                observed=observed,
            )
            pieces.append(table)
            keys.append(getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    keys = index + columns

    values_passed = values is not None
    if values_passed:
        if is_list_like(values):
            values_multi = True
            values = list(values)
        else:
            values_multi = False
            values = [values]

        # GH14938 Make sure value labels are in data
        for i in values:
            if i not in data:
                raise KeyError(i)

        to_filter = []
        for x in keys + values:
            if isinstance(x, Grouper):
                x = x.key
            try:
                if x in data:
                    to_filter.append(x)
            except TypeError:
                pass
        if len(to_filter) < len(data.columns):
            data = data[to_filter]

    else:
        values = data.columns
        for key in keys:
            try:
                values = values.drop(key)
            except (TypeError, ValueError, KeyError):
                pass
        values = list(values)

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

        # gh-21133
        # we want to down cast if
        # the original values are ints
        # as we grouped with a NaN value
        # and then dropped, coercing to floats
        for v in values:
            if (
                v in data
                and is_integer_dtype(data[v])
                and v in agged
                and not is_integer_dtype(agged[v])
            ):
                agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

    table = agged
    if table.index.nlevels > 1:
        # Related GH #17123
        # If index_names are integers, determine whether the integers refer
        # to the level position or name.
        index_names = agged.index.names[: len(index)]
        to_unstack = []
        for i in range(len(index), len(keys)):
            name = agged.index.names[i]
            if name is None or name in index_names:
                to_unstack.append(i)
            else:
                to_unstack.append(name)
        table = agged.unstack(to_unstack)

    if not dropna:
        if table.index.nlevels > 1:
            m = MultiIndex.from_arrays(
                cartesian_product(table.index.levels), names=table.index.names
            )
            table = table.reindex(m, axis=0)

        if table.columns.nlevels > 1:
            m = MultiIndex.from_arrays(
                cartesian_product(table.columns.levels), names=table.columns.names
            )
            table = table.reindex(m, axis=1)

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table._ensure_type(table.fillna(fill_value, downcast="infer"))

    if margins:
        if dropna:
            data = data[data.notna().all(axis=1)]
        table = _add_margins(
            table,
            data,
            values,
            rows=index,
            cols=columns,
            aggfunc=aggfunc,
            observed=dropna,
            margins_name=margins_name,
            fill_value=fill_value,
        )

    # discard the top level
    if (
        values_passed
        and not values_multi
        and not table.empty
        and (table.columns.nlevels > 1)
    ):
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    # GH 15193 Make sure empty columns are removed if dropna=True
    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table

```

## A test function that the buggy function fails
```python
# The relative path of the failing test file: pandas/tests/reshape/test_pivot.py

    @pytest.mark.parametrize("cols", [(1, 2), ("a", "b"), (1, "b"), ("a", 1)])
    def test_pivot_table_multiindex_only(self, cols):
        # GH 17038
        df2 = DataFrame({cols[0]: [1, 2, 3], cols[1]: [1, 2, 3], "v": [4, 5, 6]})

        result = df2.pivot_table(values="v", columns=cols)
        expected = DataFrame(
            [[4, 5, 6]],
            columns=MultiIndex.from_tuples([(1, 1), (2, 2), (3, 3)], names=cols),
            index=Index(["v"]),
        )

        tm.assert_frame_equal(result, expected)
```


## A test function that the buggy function fails
```python
# The relative path of the failing test file: pandas/tests/reshape/test_pivot.py

    @pytest.mark.parametrize("cols", [(1, 2), ("a", "b"), (1, "b"), ("a", 1)])
    def test_pivot_table_multiindex_only(self, cols):
        # GH 17038
        df2 = DataFrame({cols[0]: [1, 2, 3], cols[1]: [1, 2, 3], "v": [4, 5, 6]})

        result = df2.pivot_table(values="v", columns=cols)
        expected = DataFrame(
            [[4, 5, 6]],
            columns=MultiIndex.from_tuples([(1, 1), (2, 2), (3, 3)], names=cols),
            index=Index(["v"]),
        )

        tm.assert_frame_equal(result, expected)
```


## A test function that the buggy function fails
```python
# The relative path of the failing test file: pandas/tests/reshape/test_pivot.py

    @pytest.mark.parametrize("cols", [(1, 2), ("a", "b"), (1, "b"), ("a", 1)])
    def test_pivot_table_multiindex_only(self, cols):
        # GH 17038
        df2 = DataFrame({cols[0]: [1, 2, 3], cols[1]: [1, 2, 3], "v": [4, 5, 6]})

        result = df2.pivot_table(values="v", columns=cols)
        expected = DataFrame(
            [[4, 5, 6]],
            columns=MultiIndex.from_tuples([(1, 1), (2, 2), (3, 3)], names=cols),
            index=Index(["v"]),
        )

        tm.assert_frame_equal(result, expected)
```


## A test function that the buggy function fails
```python
# The relative path of the failing test file: pandas/tests/reshape/test_pivot.py

    @pytest.mark.parametrize("cols", [(1, 2), ("a", "b"), (1, "b"), ("a", 1)])
    def test_pivot_table_multiindex_only(self, cols):
        # GH 17038
        df2 = DataFrame({cols[0]: [1, 2, 3], cols[1]: [1, 2, 3], "v": [4, 5, 6]})

        result = df2.pivot_table(values="v", columns=cols)
        expected = DataFrame(
            [[4, 5, 6]],
            columns=MultiIndex.from_tuples([(1, 1), (2, 2), (3, 3)], names=cols),
            index=Index(["v"]),
        )

        tm.assert_frame_equal(result, expected)
```




## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
columns, expected value: `(1, 2)`, type: `tuple`

aggfunc, expected value: `'mean'`, type: `str`

data, expected value: `   1  2  v
0  1  1  4
1  2  2  5
2  3  3  6`, type: `DataFrame`

values, expected value: `'v'`, type: `str`

margins, expected value: `False`, type: `bool`

dropna, expected value: `True`, type: `bool`

margins_name, expected value: `'All'`, type: `str`

observed, expected value: `False`, type: `bool`

data.columns, expected value: `Index([1, 2, 'v'], dtype='object')`, type: `Index`

#### Expected values and types of variables right before the buggy function's return
index, expected value: `[]`, type: `list`

columns, expected value: `[1, 2]`, type: `list`

keys, expected value: `[1, 2]`, type: `list`

table, expected value: `1  1  2  3
2  1  2  3
v  4  5  6`, type: `DataFrame`

values, expected value: `['v']`, type: `list`

values_passed, expected value: `True`, type: `bool`

values_multi, expected value: `False`, type: `bool`

i, expected value: `'v'`, type: `str`

to_filter, expected value: `[1, 2, 'v']`, type: `list`

x, expected value: `'v'`, type: `str`

agged, expected value: `     v
1 2   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

agged.columns, expected value: `Index(['v'], dtype='object')`, type: `Index`

v, expected value: `'v'`, type: `str`

table.index, expected value: `Index(['v'], dtype='object')`, type: `Index`

agged.index, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=[1, 2])`, type: `MultiIndex`

table.columns, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=[1, 2])`, type: `MultiIndex`

table.empty, expected value: `False`, type: `bool`

table.T, expected value: `     v
1 2   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

### Expected case 2
#### The values and types of buggy function's parameters
columns, expected value: `('a', 'b')`, type: `tuple`

aggfunc, expected value: `'mean'`, type: `str`

data, expected value: `   a  b  v
0  1  1  4
1  2  2  5
2  3  3  6`, type: `DataFrame`

values, expected value: `'v'`, type: `str`

margins, expected value: `False`, type: `bool`

dropna, expected value: `True`, type: `bool`

margins_name, expected value: `'All'`, type: `str`

observed, expected value: `False`, type: `bool`

data.columns, expected value: `Index(['a', 'b', 'v'], dtype='object')`, type: `Index`

#### Expected values and types of variables right before the buggy function's return
index, expected value: `[]`, type: `list`

columns, expected value: `['a', 'b']`, type: `list`

keys, expected value: `['a', 'b']`, type: `list`

table, expected value: `a  1  2  3
b  1  2  3
v  4  5  6`, type: `DataFrame`

values, expected value: `['v']`, type: `list`

values_passed, expected value: `True`, type: `bool`

values_multi, expected value: `False`, type: `bool`

i, expected value: `'v'`, type: `str`

to_filter, expected value: `['a', 'b', 'v']`, type: `list`

x, expected value: `'v'`, type: `str`

agged, expected value: `     v
a b   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

agged.columns, expected value: `Index(['v'], dtype='object')`, type: `Index`

v, expected value: `'v'`, type: `str`

table.index, expected value: `Index(['v'], dtype='object')`, type: `Index`

agged.index, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=['a', 'b'])`, type: `MultiIndex`

table.columns, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=['a', 'b'])`, type: `MultiIndex`

table.empty, expected value: `False`, type: `bool`

table.T, expected value: `     v
a b   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

### Expected case 3
#### The values and types of buggy function's parameters
columns, expected value: `(1, 'b')`, type: `tuple`

aggfunc, expected value: `'mean'`, type: `str`

data, expected value: `   1  b  v
0  1  1  4
1  2  2  5
2  3  3  6`, type: `DataFrame`

values, expected value: `'v'`, type: `str`

margins, expected value: `False`, type: `bool`

dropna, expected value: `True`, type: `bool`

margins_name, expected value: `'All'`, type: `str`

observed, expected value: `False`, type: `bool`

data.columns, expected value: `Index([1, 'b', 'v'], dtype='object')`, type: `Index`

#### Expected values and types of variables right before the buggy function's return
index, expected value: `[]`, type: `list`

columns, expected value: `[1, 'b']`, type: `list`

keys, expected value: `[1, 'b']`, type: `list`

table, expected value: `1  1  2  3
b  1  2  3
v  4  5  6`, type: `DataFrame`

values, expected value: `['v']`, type: `list`

values_passed, expected value: `True`, type: `bool`

values_multi, expected value: `False`, type: `bool`

i, expected value: `'v'`, type: `str`

to_filter, expected value: `[1, 'b', 'v']`, type: `list`

x, expected value: `'v'`, type: `str`

agged, expected value: `     v
1 b   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

agged.columns, expected value: `Index(['v'], dtype='object')`, type: `Index`

v, expected value: `'v'`, type: `str`

table.index, expected value: `Index(['v'], dtype='object')`, type: `Index`

agged.index, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=[1, 'b'])`, type: `MultiIndex`

table.columns, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=[1, 'b'])`, type: `MultiIndex`

table.empty, expected value: `False`, type: `bool`

table.T, expected value: `     v
1 b   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

### Expected case 4
#### The values and types of buggy function's parameters
columns, expected value: `('a', 1)`, type: `tuple`

aggfunc, expected value: `'mean'`, type: `str`

data, expected value: `   a  1  v
0  1  1  4
1  2  2  5
2  3  3  6`, type: `DataFrame`

values, expected value: `'v'`, type: `str`

margins, expected value: `False`, type: `bool`

dropna, expected value: `True`, type: `bool`

margins_name, expected value: `'All'`, type: `str`

observed, expected value: `False`, type: `bool`

data.columns, expected value: `Index(['a', 1, 'v'], dtype='object')`, type: `Index`

#### Expected values and types of variables right before the buggy function's return
index, expected value: `[]`, type: `list`

columns, expected value: `['a', 1]`, type: `list`

keys, expected value: `['a', 1]`, type: `list`

table, expected value: `a  1  2  3
1  1  2  3
v  4  5  6`, type: `DataFrame`

values, expected value: `['v']`, type: `list`

values_passed, expected value: `True`, type: `bool`

values_multi, expected value: `False`, type: `bool`

i, expected value: `'v'`, type: `str`

to_filter, expected value: `['a', 1, 'v']`, type: `list`

x, expected value: `'v'`, type: `str`

agged, expected value: `     v
a 1   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`

agged.columns, expected value: `Index(['v'], dtype='object')`, type: `Index`

v, expected value: `'v'`, type: `str`

table.index, expected value: `Index(['v'], dtype='object')`, type: `Index`

agged.index, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=['a', 1])`, type: `MultiIndex`

table.columns, expected value: `MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=['a', 1])`, type: `MultiIndex`

table.empty, expected value: `False`, type: `bool`

table.T, expected value: `     v
a 1   
1 1  4
2 2  5
3 3  6`, type: `DataFrame`



## A GitHub issue for this bug

The issue's title:
```text
BUG/API: pivot_table with multi-index columns only
```

The issue's detailed description:
```text
Code Sample, a copy-pastable example if possible

In [21]: df = pd.DataFrame({'k': [1, 2, 3], 'v': [4, 5, 6]})

In [22]: df.pivot_table(values='v', columns='k')
Out[22]: 
k  1  2  3
v  4  5  6

In [23]: df.pivot_table(values='v', index='k')
Out[23]: 
   v
k   
1  4
2  5
3  6

In [24]: df2 = pd.DataFrame({'k1': [1, 2, 3], 'k2': [1, 2, 3], 'v': [4, 5, 6]})

In [25]: df2.pivot_table(values='v', index=('k1','k2'))
Out[25]: 
       v
k1 k2   
1  1   4
2  2   5
3  3   6

In [26]: df2.pivot_table(values='v', columns=('k1','k2'))
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-26-80d7fdeb9743> in <module>()
----> 1 df2.pivot_table(values='v', columns=('k1','k2'))

~\Anaconda\envs\py36\lib\site-packages\pandas\core\reshape\pivot.py in pivot_table(data, values, index, columns, aggfunc, fill_value, margins, dropna, margins_name)
    172     # discard the top level
    173     if values_passed and not values_multi and not table.empty and \
--> 174        (table.columns.nlevels > 1):
    175         table = table[values[0]]
    176 

~\Anaconda\envs\py36\lib\site-packages\pandas\core\generic.py in __getattr__(self, name)
   3075         if (name in self._internal_names_set or name in self._metadata or
   3076                 name in self._accessors):
-> 3077             return object.__getattribute__(self, name)
   3078         else:
   3079             if name in self._info_axis:

AttributeError: 'Series' object has no attribute 'columns'

Expected Output
No error, symmetrical between rows/columns and single/multi case

Output of pd.show_versions()
pandas 0.20.2
```



