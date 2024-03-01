### Correction:

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

        if issubclass(new_data.dtype.type, np.number):
            in_range = (
                isna(new_data._values)
                | (new_data > self.min_stamp)
                | (new_data._values == iNaT)
            )
            if not in_range.all():
                return data, False

        if new_data.dtype == "bool":  # Add condition for bool dtype
            return new_data, False

        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        for date_unit in date_units:
            try:
                new_data = to_datetime(new_data, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True
        return data, False
```

### Explanation:
The bug occurs because the function does not handle boolean data correctly, trying to convert it to datetime which leads to a TypeError. To fix this issue, a new condition is added to check if the data type is 'bool'. If it is 'bool', we return the data directly with a False flag, preventing the unnecessary datetime conversion attempt.

By including this new condition, the function will now correctly handle boolean data without attempting to convert it to datetime, resolving the TypeError and aligning with the expected behavior for boolean data in the provided test case.