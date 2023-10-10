You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

@Appender(IndexingMixin.at.__doc__)
class _AtIndexer(_ScalarAccessIndexer):
    _takeable = False

    def _convert_key(self, key, is_setter: bool = False):
        """
        Require they keys to be the same type as the index. (so we don't
        fallback)
        """
        # allow arbitrary setting
        if is_setter:
            return list(key)

        for ax, i in zip(self.obj.axes, key):
            if ax.is_integer():
                if not is_integer(i):
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if is_integer(i) and not ax.holds_integer():
                    raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key



The test error on command line is following:

===================================================================== test session starts =====================================================================
platform linux -- Python 3.8.10, pytest-5.4.3, py-1.8.1, pluggy-0.13.1
rootdir: /home/huijieyan/Desktop/PyRepair/benchmarks/BugsInPy_Cloned_Repos/pandas:69, inifile: setup.cfg
plugins: hypothesis-5.16.0, cov-4.1.0, mock-3.11.1, timeout-2.1.0
timeout: 60.0s
timeout method: signal
timeout func_only: False
collected 2 items                                                                                                                                             

pandas/tests/indexes/test_numeric.py FF                                                                                                                 [100%]

========================================================================== FAILURES ===========================================================================
__________________________________________________ TestFloat64Index.test_lookups_datetimelike_values[vals0] ___________________________________________________

self = <pandas.tests.indexes.test_numeric.TestFloat64Index object at 0x7f30f190e9a0>
vals = DatetimeIndex(['2016-01-01', '2016-01-02', '2016-01-03'], dtype='datetime64[ns]', freq='D')

    @pytest.mark.parametrize(
        "vals",
        [
            pd.date_range("2016-01-01", periods=3),
            pd.timedelta_range("1 Day", periods=3),
        ],
    )
    def test_lookups_datetimelike_values(self, vals):
        # If we have datetime64 or timedelta64 values, make sure they are
        #  wrappped correctly  GH#31163
        ser = pd.Series(vals, index=range(3, 6))
        ser.index = ser.index.astype("float64")
    
        expected = vals[1]
    
        result = ser.index.get_value(ser, 4.0)
        assert isinstance(result, type(expected)) and result == expected
        result = ser.index.get_value(ser, 4)
        assert isinstance(result, type(expected)) and result == expected
    
        result = ser[4.0]
        assert isinstance(result, type(expected)) and result == expected
        result = ser[4]
        assert isinstance(result, type(expected)) and result == expected
    
        result = ser.loc[4.0]
        assert isinstance(result, type(expected)) and result == expected
        result = ser.loc[4]
        assert isinstance(result, type(expected)) and result == expected
    
        result = ser.at[4.0]
        assert isinstance(result, type(expected)) and result == expected
        # GH#31329 .at[4] should cast to 4.0, matching .loc behavior
>       result = ser.at[4]

pandas/tests/indexes/test_numeric.py:429: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
pandas/core/indexing.py:2088: in __getitem__
    key = self._convert_key(key)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <pandas.core.indexing._AtIndexer object at 0x7f30f199ff90>, key = (4,), is_setter = False

    def _convert_key(self, key, is_setter: bool = False):
        """
        Require they keys to be the same type as the index. (so we don't
        fallback)
        """
        # allow arbitrary setting
        if is_setter:
            return list(key)
    
        for ax, i in zip(self.obj.axes, key):
            if ax.is_integer():
                if not is_integer(i):
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if is_integer(i) and not ax.holds_integer():
>                   raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
E                   ValueError: At based indexing on an non-integer index can only have non-integer indexers

pandas/core/indexing.py:2128: ValueError
__________________________________________________ TestFloat64Index.test_lookups_datetimelike_values[vals1] ___________________________________________________

self = <pandas.tests.indexes.test_numeric.TestFloat64Index object at 0x7f30f19a6550>
vals = TimedeltaIndex(['1 days', '2 days', '3 days'], dtype='timedelta64[ns]', freq='D')

    @pytest.mark.parametrize(
        "vals",
        [
            pd.date_range("2016-01-01", periods=3),
            pd.timedelta_range("1 Day", periods=3),
        ],
    )
    def test_lookups_datetimelike_values(self, vals):
        # If we have datetime64 or timedelta64 values, make sure they are
        #  wrappped correctly  GH#31163
        ser = pd.Series(vals, index=range(3, 6))
        ser.index = ser.index.astype("float64")
    
        expected = vals[1]
    
        result = ser.index.get_value(ser, 4.0)
        assert isinstance(result, type(expected)) and result == expected
        result = ser.index.get_value(ser, 4)
        assert isinstance(result, type(expected)) and result == expected
    
        result = ser[4.0]
        assert isinstance(result, type(expected)) and result == expected
        result = ser[4]
        assert isinstance(result, type(expected)) and result == expected
    
        result = ser.loc[4.0]
        assert isinstance(result, type(expected)) and result == expected
        result = ser.loc[4]
        assert isinstance(result, type(expected)) and result == expected
    
        result = ser.at[4.0]
        assert isinstance(result, type(expected)) and result == expected
        # GH#31329 .at[4] should cast to 4.0, matching .loc behavior
>       result = ser.at[4]

pandas/tests/indexes/test_numeric.py:429: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
pandas/core/indexing.py:2088: in __getitem__
    key = self._convert_key(key)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <pandas.core.indexing._AtIndexer object at 0x7f30f1bf4cc0>, key = (4,), is_setter = False

    def _convert_key(self, key, is_setter: bool = False):
        """
        Require they keys to be the same type as the index. (so we don't
        fallback)
        """
        # allow arbitrary setting
        if is_setter:
            return list(key)
    
        for ax, i in zip(self.obj.axes, key):
            if ax.is_integer():
                if not is_integer(i):
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if is_integer(i) and not ax.holds_integer():
>                   raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
E                   ValueError: At based indexing on an non-integer index can only have non-integer indexers

pandas/core/indexing.py:2128: ValueError
=================================================================== short test summary info ===================================================================
FAILED pandas/tests/indexes/test_numeric.py::TestFloat64Index::test_lookups_datetimelike_values[vals0] - ValueError: At based indexing on an non-integer ind...
FAILED pandas/tests/indexes/test_numeric.py::TestFloat64Index::test_lookups_datetimelike_values[vals1] - ValueError: At based indexing on an non-integer ind...
====================================================================== 2 failed in 0.40s ======================================================================



The raised issue description for this bug is:
BUG: corner cases in DTI.get_value, Float64Index.get_value

Series lookups are affected for the Float64Index case.