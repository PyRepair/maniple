The bug in the provided function `_try_convert_to_date` is that it does not handle boolean values appropriately for conversion to datetime, leading to a `TypeError` when trying to convert a boolean value to datetime.

### Bug Explanation:
- The function tries to convert the input data to `int64` if it is of type "object". This conversion includes boolean values which should not be converted to `int64`.
- When the function encounters a boolean value, it proceeds to try and convert it to datetime using `to_datetime`, leading to a `TypeError` because boolean values cannot be converted to datetime.
- The bug causes the function to return `new_data` unchanged, leading to incorrect results.

### Fix Strategy:
- Add a check to handle boolean values separately before attempting to convert the data to `int64` or datetime.
- If the data is of type `bool`, return it as is without any conversion.

### Corrected Function:
```python
def _try_convert_to_date(self, data):
    if not len(data):
        return data, False

    new_data = data
    if new_data.dtype == "object":
        try:
            new_data = data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass

    # Handle boolean values separately
    if new_data.dtype == "bool":
        return data, False

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

By adding a check to handle boolean values separately and returning them as is, the corrected function should now pass the failing test cases and produce the expected results.