The bug in the `_try_convert_to_date` function of the `Parser` class is related to incorrectly converting boolean values in the input data to datetime values. This issue occurs when trying to parse boolean values as timestamps, leading to unexpected behavior and raising errors.

### Cause of the Bug:
- The bug arises from treating boolean values as potential timestamp values during the conversion process.
- In the provided test cases, the input data includes boolean values, triggering the undesired conversion flow.

### Fix Strategy:
To fix this bug, we need to add a specific check to handle boolean values differently and prevent trying to convert them to datetime values. We can modify the logic to check for boolean data types and handle them appropriately without attempting datetime conversion.

### Corrected Version of the Function:
Here is the corrected version of the `_try_convert_to_date` function that handles boolean values correctly:

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
        
        # Additional check to handle boolean values separately
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

By specifically handling boolean values in the input data and avoiding datetime conversion for them, this corrected function should address the issue described in the GitHub report and provide the expected output for boolean values.