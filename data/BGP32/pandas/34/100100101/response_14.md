### Bug Explanation
The bug in the `_get_time_bins` function arises from the incorrect handling of Daylight Saving Time (DST) shifts when constructing the `binner` and `labels` variables. The function is not correctly adjusting for the shift that occurs when there is a transition from standard time to DST. This leads to misaligned bins and labels, causing the test case `test_downsample_dst_at_midnight` to fail.

### Bug Fix Strategy
To fix the bug, we need to adjust the construction of `binner` and `labels` to account for DST shifts explicitly. We can achieve this by applying the `normalize` method to the start and end timestamps before creating the `binner` and `labels` DatetimeIndex objects.

### Corrected Code
Here is the corrected version of the `_get_time_bins` function:

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

    first = ax.min().normalize()
    last = ax.max().normalize() + pd.Timedelta(days=1)

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
        labels = labels[1:]

    if ax.hasnans:
        binner = binner.insert(0, NaT)
        labels = labels.insert(0, NaT)

    if len(bins) < len(labels):
        labels = labels[: len(bins)]

    return binner, bins, labels
```

By correcting the DST shifting issue and adjusting the start and end timestamps properly, this version of the function should now correctly handle cases involving DST transitions, as required by the failing test case.