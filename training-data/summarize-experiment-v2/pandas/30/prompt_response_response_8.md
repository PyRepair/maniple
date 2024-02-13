Here is the corrected version of the _try_convert_to_date function:

```python
class Parser():

    def _try_convert_to_date(self, data):
        """
        Try to parse a ndarray like into a date column.

        Try to coerce object in epoch/iso formats and integer/float in epoch
        formats. Return a boolean if parsing was successful.
        """
        # no conversion on empty
        if not len(data):
            return data, False

        new_data = data
        if new_data.dtype == "object":
            try:
                new_data = pd.to_numeric(data, errors='coerce')
            except (TypeError, ValueError, OverflowError):
                pass

        # ignore numbers that are out of range
        if isna(new_data).any() or pd.isnull(new_data).any() or pd.isna(new_data).any():
            return data, False

        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        for date_unit in date_units:
            try:
                new_data = pd.to_datetime(new_data, infer_datetime_format=True, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True
        return data, False
```

I have made the following changes to the function:
1. Replaced the `data.astype("int64")` with `pd.to_numeric(data, errors='coerce')` to handle non-numeric data properly.
2. Updated the condition for checking out-of-range numbers to use `isna(new_data).any()` and `pd.isnull(new_data).any()` to handle NA values as well.
3. Used `pd.to_datetime` with `infer_datetime_format=True` to convert the data into datetime.
4. Made minor updates to the error handling and return statements.

This corrected function should now handle the parsing of ndarray-like input into a date column correctly and pass the failing test while addressing the issues reported in the GitHub bug.