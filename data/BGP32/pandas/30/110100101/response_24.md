## Bug Explanation
The bug in the `_try_convert_to_date` function lies in the logic for handling boolean values in the input data. The current implementation assumes that boolean values can be converted to integer (`int64`) values and then checked for range validity. However, since boolean values are not compatible with integer conversion, this logic fails, leading to incorrect processing of boolean data.

## Bug Fix Strategy
To fix this bug, we need to handle boolean values separately and ensure that they are converted properly before being processed for date conversion. We can check the data type of the input and handle boolean values differently from numeric values.

## Corrected Function
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
        elif new_data.dtype == "bool":
            new_data = new_data.astype("int64")  # Convert boolean values to integers
        
        # check for boolean type
        if new_data.dtype == "int64":
            # ignore numbers that are out of range
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

By handling boolean values separately and converting them to integers before further processing, the corrected function should now properly handle boolean data and pass the failing test.