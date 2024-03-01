### Analysis:
1. The buggy function `_get_time_bins` is part of the `TimeGrouper` class in the file `pandas/core/resample.py`.
2. The failing test `test_downsample_dst_at_midnight` is located in `pandas/tests/resample/test_datetime_index.py`.
3. The error message indicates an `AmbiguousTimeError` when calling `groupby(pd.Grouper(freq="1D")).mean()` due to the handling of ambiguous timestamps.
4. The corresponding GitHub issue (#25758) highlights the problem with daily frequency resampling on clock-change days in regions with ambiguous timezones like Cuba.
5. The current implementation does not handle ambiguous timestamps properly, leading to the error.

### Bug Explanation:
- The bug occurs because the function fails to handle ambiguous timestamps correctly, specifically on clock-change days when a timestamp can be repeated due to the time change.
- This situation is common in regions practicing daylight saving time or timezone changes.
- The error message indicates the inability to infer the DST time from an ambiguous timestamp, causing the failing test.

### Fix Strategy:
- To fix the bug, we need to enhance the logic to handle ambiguous timestamps, especially for regions with timezone changes.
- We should modify the `_get_time_bins` function to address these ambiguous timestamps and ensure correct grouping during resampling.

### Corrected Version of the `_get_time_bins` Function:
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
    # Use first/last directly instead of call replace() on them
    # to preserve nanosecond part and handle ambiguous timestamps
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

    # Generate bins considering ambiguous timestamps
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

    # Adjust labels if more than bins
    if len(bins) < len(labels):
        labels = labels[: len(bins)]

    return binner, bins, labels
```

After applying this corrected version of the `_get_time_bins` function, it should properly handle ambiguous timestamps and resolve the issue with daily resampling on clock-change days in regions like Cuba.