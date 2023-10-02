The problem is occurring because despite the user setting `raw=True`, the raw numpy array isn't being passed to the UDF, instead a pandas Series object is passed. The root cause of the issue is in line:

    apply_func = self._generate_cython_apply_func(args, kwargs, raw, offset, func)

This function should be replaced with the call that can handle raw data if raw is true. We should make sure to pass the raw data when raw is true, therefore the corrected code is:

```python
from typing import Dict, Optional, Tuple


def apply(
    self,
    func,
    raw: bool = False,
    engine: str = "cython",
    engine_kwargs: Optional[Dict] = None,
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict] = None,
):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    kwargs.pop("_level", None)
    kwargs.pop("floor", None)
    window = self._get_window()
    offset = calculate_center_offset(window) if self.center else 0
    if not is_bool(raw):
        raise ValueError("raw parameter must be `True` or `False`")

    if engine == "cython":
        if engine_kwargs is not None:
            raise ValueError("cython engine does not accept engine_kwargs")
        if raw:
            apply_func = generate_cython_apply_func_raw(args, kwargs, raw, offset, func)
        else:
            apply_func = self._generate_cython_apply_func(args, kwargs, raw, offset, func)
    elif engine == "numba":
        if raw is False:
            raise ValueError("raw must be `True` when using the numba engine")
        if func in self._numba_func_cache:
            apply_func = self._numba_func_cache[func]
        else:
            apply_func = generate_numba_apply_func(args, kwargs, func, engine_kwargs)
    else:
        raise ValueError("engine must be either 'numba' or 'cython'")

    return self._apply(
        apply_func,
        center=False,
        floor=0,
        name=func,
        use_numba_cache=engine == "numba",
    )
```

In the above fix, `generate_cython_apply_func_raw` is the function that handles the raw data. Please implement it accordingly.