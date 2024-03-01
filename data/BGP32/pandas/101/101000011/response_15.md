### Analysis:
1. The buggy function `astype_nansafe` is responsible for casting elements of an array to a specific data type in a nan-safe manner.
2. The GitHub issue highlights a specific problem with converting categorical values containing NaNs to integer dtype, where NaN is incorrectly converted to a negative integer value.
3. The bug is likely related to how NaN values are handled when converting categorical data to integer type, leading to unexpected results.
4. The bug seems to stem from the handling of NaN values in categorical data when converting to int dtype.

### Bug Explanation:
The bug occurs in the `astype_nansafe` function due to improper handling of NaN values in categorical data when casting to integer type. The bug leads to NaN values being incorrectly converted to negative integers when converting categorical data to int dtype.

### Bug Fix Strategy:
To fix the bug, we need to address the specific case where NaN values in categorical data are being incorrectly converted to negative integers. This can be achieved by updating the logic for handling NaN values during the conversion process to ensure that NaN remains as NaN in the resulting integer dtype.

### Corrected Version:
```python
def astype_nansafe(arr, dtype, copy: bool = True, skipna: bool = False):
    """
    Cast the elements of an array to a given dtype in a nan-safe manner.

    Parameters
    ----------
    arr : ndarray
    dtype : np.dtype
    copy : bool, default True
        If False, a view will be attempted but may fail, if
        e.g. the item sizes don't align.
    skipna: bool, default False
        Whether or not we should skip NaN when casting as a string-type.

    Raises
    ------
    ValueError
        The dtype was a datetime64/timedelta64 dtype, but it had no unit.
    """

    if is_extension_array_dtype(dtype):
        return dtype.construct_array_type()._from_sequence(arr, dtype=dtype, copy=copy)

    if not isinstance(dtype, np.dtype):
        dtype = pandas_dtype(dtype)

    if issubclass(dtype.type, str):
        return lib.astype_str(arr.ravel(), skipna=skipna).reshape(arr.shape)

    if is_datetime_or_timedelta_dtype(arr) and is_integer_dtype(dtype):
        if not is_datetime64ns_dtype(dtype) and not is_timedelta64ns_dtype(dtype):
            raise TypeError(f"cannot astype a datetime/timedelta to integer dtype")

        result = arr.astype(dtype)
        if isna(arr).any():
            result[isna(arr)] = np.nan
        return result

    if is_datetime64_dtype(arr) and is_object_dtype(dtype):
        return tslib.ints_to_pydatetime(arr.view(np.int64))
    elif is_timedelta64_dtype(arr) and is_object_dtype(dtype):
        return tslibs.ints_to_pytimedelta(arr.view(np.int64))

    if np.issubdtype(arr.dtype, np.floating) and np.issubdtype(dtype, np.integer) \
            and not np.isnan(arr).any():
        return arr.astype(dtype)

    result = arr.astype(dtype, copy=copy)
    if isna(arr).any():
        result[isna(arr)] = np.nan

    return result
```

### Summary:
The corrected version of the `astype_nansafe` function addresses the bug related to converting categorical data containing NaN values to integer dtype. The updated logic ensures that NaN values are properly handled during the conversion process, preventing them from being erroneously converted to negative integers.