You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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



The test source code is following:

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
        result = ser.at[4]
        assert isinstance(result, type(expected)) and result == expected

        result = ser.iloc[1]
        assert isinstance(result, type(expected)) and result == expected

        result = ser.iat[1]
        assert isinstance(result, type(expected)) and result == expected



The raised issue description for this bug is:
BUG: corner cases in DTI.get_value, Float64Index.get_value

Series lookups are affected for the Float64Index case.