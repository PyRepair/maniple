The bug in the `_try_convert_to_date` function is related to incorrectly converting boolean values to date values leading to an error in the test case `test_readjson_bool_series`.

### Bug Analysis:
1. The function attempts to convert boolean values to int64 and then to datetime, causing the issue.
2. The function fails to properly handle boolean values during conversion to date.

### Bug Explanation:
1. The input data is a Series of boolean values `[True, True, False]`.
2. The function incorrectly converts the boolean values to int64 and then tries to convert them to datetime.
3. Due to this incorrect conversion, the function fails to generate the expected output of a Series of boolean values.
4. This mismatch leads to the test case failure as it expects a Series of boolean values but the function converts the boolean values to datetimes.

### Bug Fix Strategy:
1. Detect boolean input in the function and handle it separately to avoid unnecessary conversion attempts.
2. If the Series contains boolean values, simply return it without performing any additional conversions.

### Corrected Function:
```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False
        
        if data.dtype == "bool":
            return data, True
        
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

By handling boolean values separately and avoiding unnecessary conversions, the corrected function should now pass the failing test and return the expected output.