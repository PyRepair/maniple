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
    ValueError
        Cannot convert non-finite values (NA or inf) to integer
    """

    # dispatch on extension dtype if needed
    if is_extension_array_dtype(dtype):
        return dtype.construct_array_type()._from_sequence(arr, dtype=dtype, copy=copy)

    if not isinstance(dtype, np.dtype):
        dtype = pandas_dtype(dtype)

    if issubclass(dtype.type, str):
        return lib.astype_str(arr.ravel(), skipna=skipna).reshape(arr.shape)

    elif is_datetime_or_timedelta_dtype(dtype):
        if is_object_dtype(dtype):
            return tslib.ints_to_pydatetime(arr.view(np.int64))
        elif dtype == _INT64_DTYPE:
            return arr.view(dtype)

        if dtype.kind == "M":
            return arr.astype(dtype)

        if dtype.kind == "m" and skipna:
            mask = isna(arr)
            result = arr.astype(dtype).astype(np.float64)
            result[mask] = np.nan
            return result

        if dtype == _TD_DTYPE:
            return arr.astype(_TD_DTYPE, copy=copy)

        raise TypeError(f"cannot astype a {dtype.name} from [{arr.dtype}] to [{dtype}]")

    elif np.issubdtype(arr.dtype, np.floating) and np.issubdtype(dtype, np.integer):

        if not np.isfinite(arr).all():
            raise ValueError("Cannot convert non-finite values (NA or inf) to integer")

    elif is_object_dtype(arr):

        if np.issubdtype(dtype.type, np.integer):
            return lib.astype_intsafe(arr.ravel(), dtype).reshape(arr.shape)

        if is_datetime_or_timedelta_dtype(dtype):
            from pandas import to_datetime, to_timedelta

            return astype_nansafe(to_datetime(arr).values, dtype, copy=copy)
    elif pandas_dtype(dtype).name in ("datetime64", "timedelta64"):
        msg = (
            f"The '{pandas_dtype(dtype).name}' dtype has no unit. Please pass in "
            f"{pandas_dtype(dtype).name}[ns]' instead."
        )
        raise ValueError(msg)

    return arr.astype(dtype, copy=copy)
```