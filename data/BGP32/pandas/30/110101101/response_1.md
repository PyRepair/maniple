The bug in the `_try_convert_to_date` function is due to the improper handling of boolean data type, which is not accounted for in the current implementation.

### Bug Explanation:
When the function encounters boolean data in the input, it tries to convert it to `int64` which is unnecessary since booleans can represent `True` as 1 and `False` as 0 by default. This unnecessary conversion leads to incorrect results for boolean data types.

### Fix Strategy:
1. Recognize boolean data type and handle it separately without unnecessary conversions.
2. Update the logic to correctly identify boolean values and avoid unnecessary conversions.

### Corrected Version of the Function:
```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False
        
        if data.dtype == bool:
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
        
        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        for date_unit in date_units:
            try:
                new_data = to_datetime(new_data, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True
        return data, False
```

By updating the function to handle boolean data types correctly, it should now pass the failing test case.