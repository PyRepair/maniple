To fix the bug, we need to handle the case when the data type is "bool" separately and convert it to the desired output format.

Here's the fixed code:

```python
def _try_convert_to_date(self, data):
    """
    Try to parse a ndarray like into a date column.

    Try to coerce object in epoch/iso formats and integer/float in epoch
    formats. Return a boolean if parsing was successful.
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

    # If the data type is "bool", convert it to the desired output format
    if new_data.dtype == "bool":
        return pd.Series(new_data), True

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

The fix handles the case when the data type is "bool" separately and converts it to a Pandas Series using `pd.Series(new_data)`. This ensures that the output is a Series of bools instead of timestamps.

The fix can be easily applied to the original project by replacing the `_try_convert_to_date` method with the fixed code.