### Analysis
The bug in the `_get_time_bins` function is causing an `AmbiguousTimeError` when trying to group by daily frequency on a clock change day in Cuba due to the handling of ambiguous timestamps. The issue is related to the way `date_range` is being used and the handling of datetimes near the end of the period.

### Bug Cause
The bug is caused by the `date_range` function used to generate the binner and labels. When the end timestamp contains nanosecond parts, applying `date_range` can lead to a slightly earlier last bin, causing the error due to ambiguity.

### Fix Strategy
1. Modify the calculation of `last` to ensure it includes the maximum timestamp from the initial date range without parsing ambiguity.
2. Adjust the `date_range` call by setting `normalize=True` to avoid issues related to nanosecond parts in timestamps.

### Corrected Function
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
    # GH #12037
    # use first/last directly instead of call replace() on them
    # because replace() will swallow the nanosecond part
    # thus last bin maybe slightly before the end if the end contains
    # nanosecond part and lead to `Values falls after last bin` error
    binner = labels = date_range(
        freq=self.freq,
        start=first,
        end=last,
        tz=ax.tz,
        name=ax.name,
        ambiguous="infer",
        normalize=True  # Fix: Normalize to avoid ambiguity
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

Applying this correction should resolve the issue with the `AmbiguousTimeError` and make the test case `test_downsample_dst_at_midnight` pass successfully without errors.