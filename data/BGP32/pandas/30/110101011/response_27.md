### Analysis:
- The `_try_convert_to_date` function tries to convert the input data into dates using various methods.
- It checks if the data is of "object" type and tries to convert it to "int64".
- It then checks if the data is within a valid range and tries to convert it to datetime using different date units.
- The bug seems to be causing incorrect conversion leading to the failure of the test case `test_readjson_bool_series`.
- The issue on GitHub indicates that the problem arises due to attempting to convert boolean values to datetime instead of preserving them as boolean values.

### Error Location:
- The bug could be in how the function handles converting boolean values to datetime, which should not be the case.

### Cause of the Bug:
- In the failing test case, the input data is a list of boolean values, `[true, true, false]`.
- The function incorrectly tries to convert these boolean values to int64 and then attempts to convert them to datetime.
- This results in incorrect behavior and leads to a failure in the test case.

### Fix Strategy:
- Modify the function to detect boolean values separately and ensure they remain as boolean values without attempting datetime conversion.

### Corrected Version:
```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False
        
        new_data = data
        if new_data.dtype == "object":
            try:
                new_data = data.astype("int64")
            except (TypeError, ValueError, OverflowError):
                pass
        
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

After applying this correction, the function will correctly handle boolean values and avoid unnecessary conversion attempts, hence passing the failing test case and resolving the issue reported on GitHub.