The bug in the `_try_convert_to_date` function is causing a `TypeError` when trying to convert boolean values to datetime. The function incorrectly assumes that all data needs to be converted to integers for datetime conversion.

To fix this bug, we need to handle boolean data separately before attempting to convert to datetime. Here is the corrected version of the function:

```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False
        
        if data.dtype == "bool":
            date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
            for date_unit in date_units:
                try:
                    new_data = to_datetime(data, errors="raise", unit=date_unit)
                    return new_data, True
                except (TypeError, ValueError, OverflowError):
                    pass
        
        new_data = data
        if new_data.dtype == "object":
            try:
                new_data = pd.to_numeric(data, errors="raise")
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
                return new_data, True
            except (ValueError, OverflowError):
                continue
        
        return data, False
```

This corrected version of the function handles boolean data separately before attempting to convert to datetime, avoiding the `TypeError` that was occurring. This fix should allow the function to correctly convert various types of data to datetime without errors.