### Bug Explanation
The bug in the `_try_convert_to_date` function is occurring because it tries to convert boolean values (`True` and `False`) to datetime, which is not possible. This causes a `TypeError` to be raised during the conversion process.

### Bug Fix Strategy
To fix the bug, we need to modify the function to handle boolean values separately before attempting any datetime conversion. We should exclude boolean values from the datetime conversion process.

### Corrected Version
```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False
        
        if data.dtype == "object":
            try:
                data = data.astype("int64")
            except (TypeError, ValueError, OverflowError):
                pass
        
        if issubclass(data.dtype.type, np.number):
            in_range = (
                isna(data._values)
                | (data > self.min_stamp)
                | (data._values == iNaT)
            )
            if not in_range.all():
                return data, False
        
        if data.dtype == 'bool':
            return data, False  # Don't attempt datetime conversion for boolean values
        
        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        for date_unit in date_units:
            try:
                data = to_datetime(data, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return data, True
        return data, False
``` 

By excluding boolean values from the datetime conversion process, the corrected function should now pass the failing test `test_readjson_bool_series`.