### Bug Analysis
- The bug occurs because the function `_try_convert_to_date` is trying to convert boolean values to datetime, which is not possible.
- The function is mistakenly converting the data to `int64` if it's of type "object", which is not the correct approach for boolean values.
- The function fails to handle boolean values correctly before trying to convert them to datetime, resulting in a TypeError.

### Bug Fix Strategy
To fix the bug, we need to adjust the conversion logic to handle boolean values correctly before attempting to convert them to datetime. We should skip the datetime conversion for boolean values and handle them appropriately.

### Corrected Version
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

        # ignore numbers that are out of range
        if issubclass(new_data.dtype.type, np.number):
            in_range = (
                isna(new_data._values)
                | (new_data > self.min_stamp)
                | (new_data._values == iNaT)
            )
            if not in_range.all():
                return data, False
        
        if new_data.dtype == "bool":
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

By checking for boolean values and returning False as conversion status for boolean data, we prevent the TypeError from occurring when trying to convert boolean values to datetime. This correction should resolve the issue and allow the function to handle boolean values correctly.