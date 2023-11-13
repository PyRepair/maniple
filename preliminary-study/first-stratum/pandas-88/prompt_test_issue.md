You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

# Note: We need to make sure `frame` is imported before `pivot`, otherwise
# _shared_docs['pivot_table'] will not yet exist.  TODO: Fix this dependency
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



The test source code is following:

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



The raised issue description for this bug is:
BUG/API: pivot_table with multi-index columns only

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