### Analysis:
1. The function `_get_time_bins` is part of the resampling process in pandas. It is responsible for getting time bins based on the input DatetimeIndex.
2. The test function `test_downsample_dst_at_midnight` fails due to an issue with handling ambiguous time on a clock change day in Cuba.
3. The GitHub issue reports a similar problem where `pd.Grouper` raises an `AmbiguousTimeError` when dealing with an ambiguous timestamp on a clock change day in Cuba.
4. The function `_get_time_bins` does not handle ambiguous timestamps correctly, leading to incorrect grouping and labeling.

### Bug:
The bug arises from the handling of ambiguous timestamps during the resampling process, causing the test to fail when dealing with DST changes.

### Strategy for Fixing the Bug:
1. When creating the `binner` and `labels`, ensure proper handling of ambiguous timestamps on clock change days.
2. Adjust the way bins are generated to account for any potential ambiguity in timestamps.
3. Update the label shifting logic to reflect correct groupings on clock change days.

### Corrected Version of the Function:
```python
def _get_time_bins(self, ax):
    if not isinstance(ax, DatetimeIndex):
        raise TypeError(
            "axis must be a DatetimeIndex, but got "
            f"an instance of {type(ax).__name__}"
        )

    if len(ax) == 0:
        binner = DatetimeIndex(data=[], freq=self.freq, name=ax.name)
        return binner, [], binner

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
        labels = binner[1:] if self.label == "right" else binner
    elif self.label == "right":
        labels = binner[1:]

    if ax.hasnans:
        binner = binner.insert(0, NaT)
        labels = labels.insert(0, NaT)

    if len(bins) < len(labels):
        labels = labels[:len(bins)]

    return binner, bins, labels
```

This corrected version of the function includes adjustments to handle ambiguous timestamps properly during resampling, which should resolve the issue reported on GitHub and make the failing test pass.