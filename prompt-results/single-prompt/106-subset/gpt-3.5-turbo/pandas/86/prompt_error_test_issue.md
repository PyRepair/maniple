You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if values is None:
        cols = [columns] if index is None else [index, columns]
        append = index is None
        indexed = data.set_index(cols, append=append)
    else:
        if index is None:
            index = data.index
        else:
            index = data[index]
        index = MultiIndex.from_arrays([index, data[columns]])

        if is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data._constructor(
                data[values].values, index=index, columns=values
            )
        else:
            indexed = data._constructor_sliced(data[values].values, index=index)
    return indexed.unstack(columns)



The test error on command line is following:

===================================================================== test session starts =====================================================================
platform linux -- Python 3.8.10, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
rootdir: /home/huijieyan/Desktop/PyRepair/benchmarks/BugsInPy_Cloned_Repos/pandas:86, inifile: setup.cfg
plugins: hypothesis-5.16.0, cov-4.1.0, mock-3.11.1, timeout-2.1.0
timeout: 60.0s
timeout method: signal
timeout func_only: False
collected 1 item                                                                                                                                              

pandas/tests/reshape/test_pivot.py F                                                                                                                    [100%]

========================================================================== FAILURES ===========================================================================
_____________________________________________________ TestPivotTable.test_pivot_columns_none_raise_error ______________________________________________________

self = Index(['col1', 'col2', 'col3'], dtype='object'), key = None, method = None, tolerance = None

    @Appender(_index_shared_docs["get_loc"])
    def get_loc(self, key, method=None, tolerance=None):
        if method is None:
            if tolerance is not None:
                raise ValueError(
                    "tolerance argument only valid if using pad, "
                    "backfill or nearest lookups"
                )
            try:
>               return self._engine.get_loc(key)

pandas/core/indexes/base.py:2901: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

>   cpdef get_loc(self, object val):

pandas/_libs/index.pyx:109: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

>   return self.mapping.get_item(val)

pandas/_libs/index.pyx:136: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

>   cpdef get_item(self, object val):

pandas/_libs/hashtable_class_helper.pxi:1614: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

>   raise KeyError(val)
E   KeyError: None

pandas/_libs/hashtable_class_helper.pxi:1622: KeyError

During handling of the above exception, another exception occurred:

self = <pandas.tests.reshape.test_pivot.TestPivotTable object at 0x7f908cfc98b0>

    def test_pivot_columns_none_raise_error(self):
        # GH 30924
        df = pd.DataFrame(
            {"col1": ["a", "b", "c"], "col2": [1, 2, 3], "col3": [1, 2, 3]}
        )
        msg = r"pivot\(\) missing 1 required argument: 'columns'"
        with pytest.raises(TypeError, match=msg):
>           df.pivot(index="col1", values="col3")

pandas/tests/reshape/test_pivot.py:791: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
pandas/core/frame.py:5947: in pivot
    return pivot(self, index=index, columns=columns, values=values)
pandas/core/reshape/pivot.py:441: in pivot
    index = MultiIndex.from_arrays([index, data[columns]])
pandas/core/frame.py:2793: in __getitem__
    indexer = self.columns.get_loc(key)
pandas/core/indexes/base.py:2903: in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
pandas/_libs/index.pyx:109: in pandas._libs.index.IndexEngine.get_loc
    cpdef get_loc(self, object val):
pandas/_libs/index.pyx:136: in pandas._libs.index.IndexEngine.get_loc
    return self.mapping.get_item(val)
pandas/_libs/hashtable_class_helper.pxi:1614: in pandas._libs.hashtable.PyObjectHashTable.get_item
    cpdef get_item(self, object val):
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

>   raise KeyError(val)
E   KeyError: None

pandas/_libs/hashtable_class_helper.pxi:1622: KeyError
=================================================================== short test summary info ===================================================================
FAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_columns_none_raise_error - KeyError: None
====================================================================== 1 failed in 0.51s ======================================================================



The test source code is following:

    def test_pivot_columns_none_raise_error(self):
        # GH 30924
        df = pd.DataFrame(
            {"col1": ["a", "b", "c"], "col2": [1, 2, 3], "col3": [1, 2, 3]}
        )
        msg = r"pivot\(\) missing 1 required argument: 'columns'"
        with pytest.raises(TypeError, match=msg):
            df.pivot(index="col1", values="col3")



The raised issue description for this bug is:
BUG: Wrong error message is raised when columns=None in df.pivot

From docstring, index and values can be optional in df.pivot, but columns is not

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html
index : string or object, optional
Column to use to make new frame¡¯s index. If None, uses existing index.

columns : string or object
Column to use to make new frame¡¯s columns.

However, the error message is confusing now, should raise columns is not optional.

Code example:
>>> df = pd.DataFrame({"foo": ['one', 'one', 'two', 'two'],"bar": ['A', 'A', 'B', 'C'],"baz": [1, 2, 3, 4]})
>>> df.pivot(columns=None)

KeyError: 'None of [None] are in the columns'