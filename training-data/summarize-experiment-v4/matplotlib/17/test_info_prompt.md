Your task is to assist a developer in analyzing a stack trace of a failing test to identify a bug in a program. You will receive the source code of the function suspected to contain the bug, along with the code of the failing tests and the full error messages. Your role is not to fix the bug but to summarize what what stack frames or messages are closely related to the fault location in the buggy function, and simplify the original error message. You summary should be in a single paragraph.

## The source code of the buggy function

```python
def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    """
    Modify the endpoints of a range as needed to avoid singularities.

    Parameters
    ----------
    vmin, vmax : float
        The initial endpoints.
    expander : float, default: 0.001
        Fractional amount by which *vmin* and *vmax* are expanded if
        the original interval is too small, based on *tiny*.
    tiny : float, default: 1e-15
        Threshold for the ratio of the interval to the maximum absolute
        value of its endpoints.  If the interval is smaller than
        this, it will be expanded.  This value should be around
        1e-15 or larger; otherwise the interval will be approaching
        the double precision resolution limit.
    increasing : bool, default: True
        If True, swap *vmin*, *vmax* if *vmin* > *vmax*.

    Returns
    -------
    vmin, vmax : float
        Endpoints, expanded and/or swapped if necessary.
        If either input is inf or NaN, or if both inputs are 0 or very
        close to zero, it returns -*expander*, *expander*.
    """

    if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
        return -expander, expander

    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True

    maxabsvalue = max(abs(vmin), abs(vmax))
    if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
        vmin = -expander
        vmax = expander

    elif vmax - vmin <= maxabsvalue * tiny:
        if vmax == 0 and vmin == 0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander*abs(vmin)
            vmax += expander*abs(vmax)

    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax

```

## Test case 1 for the buggy function
```python
# The relative path of the failing test file: lib/matplotlib/tests/test_colorbar.py

@pytest.mark.parametrize("clim", [(-20000, 20000), (-32768, 0)])
def test_colorbar_int(clim):
    # Check that we cast to float early enough to not
    # overflow ``int16(20000) - int16(-20000)`` or
    # run into ``abs(int16(-32768)) == -32768``.
    fig, ax = plt.subplots()
    im = ax.imshow([[*map(np.int16, clim)]])
    fig.colorbar(im)
    assert (im.norm.vmin, im.norm.vmax) == clim
```

### The error message from the failing test
```text
clim = (-20000, 20000)

    @pytest.mark.parametrize("clim", [(-20000, 20000), (-32768, 0)])
    def test_colorbar_int(clim):
        # Check that we cast to float early enough to not
        # overflow ``int16(20000) - int16(-20000)`` or
        # run into ``abs(int16(-32768)) == -32768``.
        fig, ax = plt.subplots()
        im = ax.imshow([[*map(np.int16, clim)]])
>       fig.colorbar(im)

lib/matplotlib/tests/test_colorbar.py:582: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
lib/matplotlib/figure.py:2200: in colorbar
    cb = cbar.colorbar_factory(cax, mappable, **cb_kw)
lib/matplotlib/colorbar.py:1707: in colorbar_factory
    cb = Colorbar(cax, mappable, **kwargs)
lib/matplotlib/colorbar.py:1231: in __init__
    ColorbarBase.__init__(self, ax, **kwargs)
lib/matplotlib/colorbar.py:472: in __init__
    self.draw_all()
lib/matplotlib/colorbar.py:495: in draw_all
    self._process_values()
lib/matplotlib/colorbar.py:961: in _process_values
    self.norm.vmin, self.norm.vmax = mtransforms.nonsingular(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

vmin = -20000, vmax = 20000, expander = 0.1, tiny = 1e-15, increasing = True

    def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
        """
        Modify the endpoints of a range as needed to avoid singularities.
    
        Parameters
        ----------
        vmin, vmax : float
            The initial endpoints.
        expander : float, default: 0.001
            Fractional amount by which *vmin* and *vmax* are expanded if
            the original interval is too small, based on *tiny*.
        tiny : float, default: 1e-15
            Threshold for the ratio of the interval to the maximum absolute
            value of its endpoints.  If the interval is smaller than
            this, it will be expanded.  This value should be around
            1e-15 or larger; otherwise the interval will be approaching
            the double precision resolution limit.
        increasing : bool, default: True
            If True, swap *vmin*, *vmax* if *vmin* > *vmax*.
    
        Returns
        -------
        vmin, vmax : float
            Endpoints, expanded and/or swapped if necessary.
            If either input is inf or NaN, or if both inputs are 0 or very
            close to zero, it returns -*expander*, *expander*.
        """
    
        if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
            return -expander, expander
    
        swapped = False
        if vmax < vmin:
            vmin, vmax = vmax, vmin
            swapped = True
    
        maxabsvalue = max(abs(vmin), abs(vmax))
        if maxabsvalue < (1e6 / tiny) * np.finfo(float).tiny:
            vmin = -expander
            vmax = expander
    
>       elif vmax - vmin <= maxabsvalue * tiny:
E       RuntimeWarning: overflow encountered in scalar subtract

lib/matplotlib/transforms.py:2799: RuntimeWarning

```


## Test case 2 for the buggy function
```python
# The relative path of the failing test file: lib/matplotlib/tests/test_colorbar.py

@pytest.mark.parametrize("clim", [(-20000, 20000), (-32768, 0)])
def test_colorbar_int(clim):
    # Check that we cast to float early enough to not
    # overflow ``int16(20000) - int16(-20000)`` or
    # run into ``abs(int16(-32768)) == -32768``.
    fig, ax = plt.subplots()
    im = ax.imshow([[*map(np.int16, clim)]])
    fig.colorbar(im)
    assert (im.norm.vmin, im.norm.vmax) == clim
```

### The error message from the failing test
```text
clim = (-32768, 0)

    @pytest.mark.parametrize("clim", [(-20000, 20000), (-32768, 0)])
    def test_colorbar_int(clim):
        # Check that we cast to float early enough to not
        # overflow ``int16(20000) - int16(-20000)`` or
        # run into ``abs(int16(-32768)) == -32768``.
        fig, ax = plt.subplots()
        im = ax.imshow([[*map(np.int16, clim)]])
>       fig.colorbar(im)

lib/matplotlib/tests/test_colorbar.py:582: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
lib/matplotlib/figure.py:2200: in colorbar
    cb = cbar.colorbar_factory(cax, mappable, **cb_kw)
lib/matplotlib/colorbar.py:1707: in colorbar_factory
    cb = Colorbar(cax, mappable, **kwargs)
lib/matplotlib/colorbar.py:1231: in __init__
    ColorbarBase.__init__(self, ax, **kwargs)
lib/matplotlib/colorbar.py:472: in __init__
    self.draw_all()
lib/matplotlib/colorbar.py:495: in draw_all
    self._process_values()
lib/matplotlib/colorbar.py:961: in _process_values
    self.norm.vmin, self.norm.vmax = mtransforms.nonsingular(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

vmin = -32768, vmax = 0, expander = 0.1, tiny = 1e-15, increasing = True

    def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
        """
        Modify the endpoints of a range as needed to avoid singularities.
    
        Parameters
        ----------
        vmin, vmax : float
            The initial endpoints.
        expander : float, default: 0.001
            Fractional amount by which *vmin* and *vmax* are expanded if
            the original interval is too small, based on *tiny*.
        tiny : float, default: 1e-15
            Threshold for the ratio of the interval to the maximum absolute
            value of its endpoints.  If the interval is smaller than
            this, it will be expanded.  This value should be around
            1e-15 or larger; otherwise the interval will be approaching
            the double precision resolution limit.
        increasing : bool, default: True
            If True, swap *vmin*, *vmax* if *vmin* > *vmax*.
    
        Returns
        -------
        vmin, vmax : float
            Endpoints, expanded and/or swapped if necessary.
            If either input is inf or NaN, or if both inputs are 0 or very
            close to zero, it returns -*expander*, *expander*.
        """
    
        if (not np.isfinite(vmin)) or (not np.isfinite(vmax)):
            return -expander, expander
    
        swapped = False
        if vmax < vmin:
            vmin, vmax = vmax, vmin
            swapped = True
    
>       maxabsvalue = max(abs(vmin), abs(vmax))
E       RuntimeWarning: overflow encountered in scalar absolute

lib/matplotlib/transforms.py:2794: RuntimeWarning

```