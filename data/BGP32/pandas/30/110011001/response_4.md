### Analysis:
- The function `_try_convert_to_date` is designed to convert data to a date column. However, it fails when encountering boolean values, as seen in the error message provided.
- The function first attempts to convert the data to `int64`, but in the case of boolean values, it should check for those types and handle them differently.
- The error message specifically points out that `<class 'bool'> is not convertible to datetime`.
- The function is currently converting boolean values directly to `int64`, which is not the correct conversion for booleans.

### Bug Cause:
- The bug is caused by the function not handling boolean values when attempting to convert data to a date column. It directly converts booleans to `int64`, which results in a type error when `to_datetime` is called on boolean data.

### Fix Strategy:
- We need to enhance the function to check for boolean values and handle them appropriately before trying to convert the data to `int64`.
- When encountering boolean values, we should convert them to a format that can be successfully processed by `to_datetime`.

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
                if np.issubdtype(new_data.dtype, np.bool_):
                    new_data = new_data.astype(str)
                new_data = to_datetime(new_data, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True
        return data, False
```

In the corrected version, we check if the data type is a boolean before trying to convert it to datetime. If it is a boolean, we convert it to a string to handle it properly in the `to_datetime` function. This modification should resolve the issue with converting boolean values to datetime.