### Analysis:
1. The function `_get_time_bins` within the `TimeGrouper` class is responsible for generating time bins for resampling in pandas.
2. The issue reported on GitHub relates to handling ambiguous timestamps when performing grouping by daily frequency.
3. The bug causes an `AmbiguousTimeError` on clock change days in specific time zones like Cuba due to incorrect handling of ambiguous timestamps.
4. The bug occurs because the function `date_range()` is giving slightly incorrect results when dealing with ambiguous timestamps.
5. The strategy to fix the bug involves handling ambiguous timestamps correctly, ensuring that the labels and bins align properly.

### Bug Fix:
To fix the bug, we need to adjust the way `date_range()` generates time bins to handle ambiguous timestamps correctly.

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
        binner = lib.generate_bins_dt64(
            start=first,
            end=last + self.freq,  # Fix to ensure correct binning with ambiguous timestamps
            freq=self.freq,
            tz=ax.tz,
            closed=self.closed,
            ambiguous='infer',
            nonexistent='shift_forward'
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

By adjusting how the time bins are generated and making sure the ambiguous timestamps are handled correctly, this bug should be fixed and the test `test_downsample_dst_at_midnight` should pass without raising an `AmbiguousTimeError`.