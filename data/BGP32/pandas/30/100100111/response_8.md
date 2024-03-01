### Identify the Bug
The bug lies in the `_try_convert_to_date` function where it incorrectly converts the input data to timestamps even for boolean values. This causes the function to return incorrect results when Boolean values are passed as input.

### Error Cause
The bug occurs because the function attempts to convert the input data to timestamps regardless of the data type. When Boolean values are encountered, this results in incorrect conversions and ultimately produces wrongly formatted output.

### Fix Strategy
To fix the bug, we need to update the function to only attempt date conversions for data that requires it, such as numeric values or objects that can be converted to integers. For Boolean data, the function should skip the date conversion step altogether and return the original input data as output.

### Corrected Function
Here is the corrected version of the `_try_convert_to_date` function:

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
    elif new_data.dtype == "bool":
        return new_data, False

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

By adding the `elif new_data.dtype == "bool":` condition, the function will now correctly handle Boolean data without attempting date conversions. This fix should resolve the issue reported on GitHub and ensure that the function behaves as expected for different data types.