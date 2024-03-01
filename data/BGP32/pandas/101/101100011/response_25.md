### Analysis:
1. The buggy function `astype_nansafe` is responsible for casting elements of an array to a given data type in a nan-safe manner.
2. The buggy function calls other functions within the same file, like `pandas_dtype`, `is_datetime64_dtype`, `is_timedelta64_dtype`, `is_extension_array_dtype`, etc., to handle different cases based on the input data type.
3. The failing test `test_astype_nansafe` tries to cast a NaN value to an integer and expects a ValueError to be raised, but the current implementation does not handle this scenario correctly.
4. The GitHub issue suggests that when converting a categorical series containing NaNs to an integer dtype, the NaNs are incorrectly converted to negative integer values, leading to unexpected results.

### Bug Fix Strategy:
1. Update the section of the buggy function that handles the case for converting NaN values to integer to correctly raise a ValueError.
2. Add a condition to handle the scenario of casting to an integer where NaN values are present.

### Corrected Version of the Buggy Function:
```python
def astype_nansafe(arr, dtype, copy: bool = True, skipna: bool = False):
    """
    Cast the elements of an array to a given dtype a nan-safe manner.

    Parameters
    ----------
    arr : ndarray
    dtype : np.dtype
    copy : bool, default True
        If False, a view will be attempted but may fail, if e.g. the item sizes don't align.
    skipna: bool, default False
        Whether or not we should skip NaN when casting as a string-type.

    Raises
    ------
    ValueError
        The dtype was a datetime64/timedelta64 dtype, but it had no unit.
    ValueError
        Cannot convert non-finite values (NA or inf) to integer.
    """
    
    if is_extension_array_dtype(dtype):
        return dtype.construct_array_type()._from_sequence(arr, dtype=dtype, copy=copy)

    if not isinstance(dtype, np.dtype):
        dtype = pandas_dtype(dtype)

    if issubclass(dtype.type, str):
        return lib.astype_str(arr.ravel(), skipna=skipna).reshape(arr.shape)

    elif is_datetime64_dtype(arr):
        if is_object_dtype(dtype):
            return tslib.ints_to_pydatetime(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)

        if dtype.kind == "M":
            return arr.astype(dtype)

        raise TypeError(f"cannot astype a datetimelike from [{arr.dtype}] to [{dtype}]")

    elif is_timedelta64_dtype(arr):
        if is_object_dtype(dtype):
            return tslibs.ints_to_pytimedelta(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)

        if dtype not in [_INT64_DTYPE, _TD_DTYPE]:
            if dtype.kind == "m":
                mask = isna(arr)
                result = arr.astype(dtype).astype(np.float64)
                result[mask] = np.nan
                return result
        elif dtype == _TD_DTYPE:
            return arr.astype(_TD_DTYPE, copy=copy)

        raise TypeError(f"cannot astype a timedelta from [{arr.dtype}] to [{dtype}]")

    elif np.issubdtype(arr.dtype, np.floating) and np.issubdtype(dtype, np.integer):
        if not np.isfinite(arr).all():
            raise ValueError("Cannot convert non-finite values (NA or inf) to integer")
    
    elif is_object_dtype(arr):
        if np.issubdtype(dtype.type, np.integer):
            return lib.astype_intsafe(arr.ravel(), dtype).reshape(arr.shape)

        elif is_datetime_or_timedelta_dtype(dtype):
            if isna(arr).any():
                raise ValueError("Cannot convert non-finite values (NA or inf) to integer")
            return astype_nansafe(arr.astype('float64'), dtype, copy=copy)        

    if dtype.name in ("datetime64", "timedelta64"):
        msg = (
            f"The '{dtype.name}' dtype has no unit. Please pass in "
            f"'{dtype.name}[ns]' instead."
        )
        raise ValueError(msg)

    if copy or is_object_dtype(arr) or is_object_dtype(dtype):
        return arr.astype(dtype, copy=True)

    return arr.view(dtype)
```

### Changes Made:
1. Added a condition to handle the scenario when casting to an integer and NaN values are present in the array.
2. Raised a ValueError if NaN values are encountered during the conversion to an integer.

Now, the corrected version of the `astype_nansafe` function should appropriately handle the conversion of NaN values to integer, passing the failing test and resolving the issue reported in GitHub.