### Analysis:
1. The function `_get_time_bins` is part of the `TimeGrouper` class which extends the `Grouper` class.
2. The function calls another function `_get_timestamp_range_edges` from the same file.
3. The issue described on GitHub relates to handling ambiguous timestamps during the grouping operation, specifically on clock change days in Cuba.
4. The failing test involves downsampling a datetime index with hourly frequency to daily frequency in a timezone with a clock change day.
5. The bug causes an `AmbiguousTimeError` due to the incorrect handling of ambiguous timestamps on clock change days.

### Bug Explanation:
The bug is likely caused by the incorrect label assignment for ambiguous timestamps on clock change days in the `_get_time_bins` function. The function fails to properly handle the last bin being slightly before the end if the end contains a nanosecond part, leading to the `AmbiguousTimeError` during the grouping operation in the failing test.

### Bug Fix Strategy:
1. Directly use `first` and `last` timestamps obtained from `_get_timestamp_range_edges` instead of calling `replace()` on them to avoid losing nanosecond precision.
2. Adjust the label assignment for ambiguous timestamps during bin creation to ensure correct behavior on clock change days.

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
    # Avoid losing nanosecond precision when using the timestamps
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

    # General version, knowing nothing about relative frequencies
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

    # If we end up with more labels than bins, adjust the labels
    if len(bins) < len(labels):
        labels = labels[: len(bins)]

    return binner, bins, labels
```

Applying this correction should address the issue described on GitHub and ensure that the failing test `test_downsample_dst_at_midnight` passes correctly.