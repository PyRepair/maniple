### Bug explanation
The bug in the provided function is related to the creation of `binner` and `labels` when adjusting time bins. The `binner` and `labels` are created using the `date_range` function, but the `labels` generation logic inside the conditional blocks is incorrect due to swapping `if` conditions, which leads to incorrect results for the labels.

### Bug location
The bug is located in the conditional logic where `labels` are assigned different values based on the `self.closed` and `self.label` conditions. The conditions for `self.closed` and `self.label` are not correctly applied.

### Bug fix strategy
To fix the bug, the conditions for assigning values to `labels` based on `self.closed` and `self.label` need to be corrected. Additionally, the handling of `ax.hasnans` where `NaT` values are inserted into `binner` and `labels` also needs to be fixed.

### Corrected version of the function
```python
def _get_time_bins(self, ax):
    if not isinstance(ax, DatetimeIndex):
        raise TypeError(
            "axis must be a DatetimeIndex, but got "
            f"an instance of {type(ax).__name__}"
        )

    if len(ax) == 0:
        binner = labels = DatetimeIndex(data=[], freq=self.freq, name=ax.name)
        return binner, [], labels

    first, last = _get_timestamp_range_edges(
        ax.min(), ax.max(), self.freq, closed=self.closed, base=self.base
    )
    
    binner = labels = date_range(
        freq=self.freq,
        start=first,
        end=last,
        tz=ax.tz,
        name=ax.name,
        ambiguous="infer",
        nonexistent="shift_forward",
    )

    ax_values = ax.asi8
    binner, bin_edges = self._adjust_bin_edges(binner, ax_values)

    bins = lib.generate_bins_dt64(
        ax_values, bin_edges, self.closed, hasnans=ax.hasnans
    )

    if self.closed == "right":
        labels = binner
        if self.label == "right":
            labels = labels[1:]
    elif self.label == "right":
        labels = labels[:-1]  # Fix to generate labels properly
    
    if ax.hasnans:
        binner = binner.insert(0, NaT)
        labels = labels.insert(0, NaT)

    if len(bins) < len(labels):
        labels = labels[:len(bins)]

    return binner, bins, labels
```

This corrected version of the function addresses the issues mentioned, ensuring correct generation of `binner` and `labels` based on `self.closed` and `self.label` conditions, as well as handling `ax.hasnans` appropriately. This fix should satisfy the expected input/output values provided for the failing test case.