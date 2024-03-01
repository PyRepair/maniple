### Analysis:
- The buggy function `_try_convert_to_date` is responsible for converting data into date format.
- The issue occurs when trying to convert boolean values to dates, resulting in a TypeError.
- The failing test `test_readjson_bool_series` expects a Pandas Series of boolean values but receives a Series of timestamps after a change in behavior in Pandas version 1.0.0.
- The `_try_convert_to_date` function fails to handle boolean input data appropriately, causing the error.

### Bug Explanation:
- The buggy function `_try_convert_to_date` tries to convert boolean values to dates, leading to a TypeError.
- The function is not equipped to handle boolean data types, resulting in incorrect conversions and raising exceptions instead of returning the expected boolean Series.

### Bug Fix Strategy:
- Modify the `_try_convert_to_date` function to handle boolean data types separately.
- Ensure that boolean values are correctly processed and returned as a boolean Series without attempts to convert them into dates.

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
            return new_data, True
        
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

### The corrected function now handles boolean data types separately and returns the expected boolean Series.