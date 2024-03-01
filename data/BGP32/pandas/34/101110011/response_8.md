### Bug Analysis:
The buggy function `_get_time_bins` in the `TimeGrouper` class of `pandas/core/resample.py` is causing an `AmbiguousTimeError` when the test function `test_downsample_dst_at_midnight` is executed. This error is due to a problem with handling ambiguous timestamps during daylight saving time transitions, as described in the GitHub issue #25758.

### Issue Cause:
The bug arises because the `date_range` function is used to create `binner` and `labels` in `_get_time_bins` without considering ambiguous timestamps on clock change days. This leads to an `AmbiguousTimeError` when grouping the data on the affected day.

### Bug Fix Strategy:
To address the bug, it is necessary to handle the ambiguous time issue during the creation of the `binner` and `labels` and ensure that the timestamps are correctly adjusted to avoid conflicts with daylight saving transitions.

### Corrected Version:

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

    # general version, knowing nothing about relative frequencies
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

    # if we end up with more labels than bins
    # adjust the labels
    # GH4076
    if len(bins) < len(labels):
        labels = labels[: len(bins)]

    return binner, bins, labels
```

This corrected version includes `ambiguous="infer"` in the `date_range` call to handle ambiguous timestamps properly during daylight saving time transitions on clock change days.

Applying this fix should address the `AmbiguousTimeError` issue, allowing the test function `test_downsample_dst_at_midnight` to run without errors.