To fix the bug in the `_get_time_bins` function, we need to address the issue related to AmbiguousTimeError on clock change days in Cuba. The problem arises due to the handling of timestamps before and after the clock change on such days.

The bug can be fixed by modifying the logic to handle the transition between different time zones on the clock change day, especially when working with daily frequency data. The function should handle the ambiguity in timestamps correctly.

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

    # Adjust labels based on the number of bins
    if len(bins) < len(labels):
        labels = labels[: len(bins)]

    return binner, bins, labels
```

This corrected version addresses the issue of ambiguous timestamps on the clock change day in Cuba by using the parameter `ambiguous="infer"` in the `date_range` function call.

By incorporating this change, the function should now handle the timestamps correctly, providing the expected results for cases like the one described in the GitHub issue.

Make sure to run the failing test function `test_downsample_dst_at_midnight` after applying this fix to verify that the bug has been resolved.