### Analysis:
- The buggy function `_try_convert_to_date` is attempting to convert data to datetime format in the given units.
- The failing test `test_readjson_bool_series` is trying to parse a JSON array containing boolean values into a Series.
- The error message indicates that a boolean value is not convertible to datetime when the function tries to convert the data.

### Bug:
- The bug is caused by the `_try_convert_to_date` function trying to convert non-datetime compatible data (boolean in this case) to datetime.

### Fix:
- We need to add an explicit check to handle boolean values separately and return without attempting to convert them to datetime.
- We should also ensure that the conversion to `int64` happens for object types only when needed.

### Corrected Function:
```python
def _try_convert_to_date(self, data):
    """
    Try to parse a ndarray-like into a date column.

    Try to coerce object in epoch/iso formats and integer/float in epoch formats. Return a boolean if parsing was successful.
    """
    # no conversion on empty
    if not len(data):
        return data, False
    
    new_data = data
    if new_data.dtype == "object":
        try:
            new_data = data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass

    # ignore boolean values
    if np.issubdtype(new_data.dtype, np.bool_):
        return data, False

    # ignore numbers that are out of range
    if issubclass(new_data.dtype.type, np.number):
        in_range = (
            isna(new_data._values)
            | (new_data > self.min_stamp)
            | (new_data._values == iNaT)
        )
        if not in_range.all():
            return data, False

    date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
    for date_unit in date_units:
        try:
            new_data = to_datetime(new_data, errors="raise", unit=date_unit)
        except (ValueError, OverflowError):
            continue
        return new_data, True
    return data, False
```

Now, with the above fix, the function should handle boolean values correctly and return without trying to convert them to datetime.