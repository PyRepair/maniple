The bug in the `_try_convert_to_date` function is that it is not correctly converting the data to datetime when the dtype is "object." The code is mistakenly converting object types to int64 without properly handling date formats.

### Cause of the Bug:
In the failing test case with input data as `"[true, true, false]"`, the function is not able to convert the boolean values to datetime due to incorrect handling of object types. This results in the function returning the original data without converting it into a datetime format, causing the test to fail.

### Fix Strategy:
To fix the bug, the function should properly handle object types representing date formats by parsing them using `to_datetime`. Additionally, the function should check for boolean values and convert them to datetime format accordingly.

### Corrected Version of the Function:
```python
def _try_convert_to_date(self, data):
    if not len(data):
        return data, False

    new_data = data
    if new_data.dtype == "object":
        try:
            new_data = to_datetime(new_data, errors="raise")
        except ValueError:
            pass

    # ignore numbers that are out of range
    if issubclass(new_data.dtype.type, np.number):
        in_range = (
            isna(new_data._values)
            | (new_data > self.min_stamp)
            | (new_data._values == iNaT)
        )
        if not in_range.all():
            return data, False

    for date_unit in (self.date_unit,) if self.date_unit else self._STAMP_UNITS:
        try:
            new_data = to_datetime(new_data, errors="raise", unit=date_unit)
        except (ValueError, OverflowError):
            continue
        return new_data, True
    return data, False
```

After applying this correction, the function should now correctly convert object types representing date formats to datetime, ensuring that the failing test `test_readjson_bool_series` passes successfully.