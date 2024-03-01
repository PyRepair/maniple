### Analysis
The `TimeGrouper` class has a `_get_time_bins` method which is supposed to calculate time bins for grouping based on the provided axis (datetime index). The bug seems to be related to how the `labels` are adjusted based on the `closed` and `label` parameters.

The current implementation fails to correctly adjust the labels when the `closed` condition is "right".

### Bug Cause
The bug is caused by the incorrect adjustment of labels based on the `closed` and `label` conditions. When `self.closed` is set to "right", the labels are not correctly modified based on the `label` parameter.

### Fix Strategy
To fix the bug, we need to ensure that the adjustment of labels is correctly handled based on the `closed` and `label` conditions. We can adjust the labels according to the logic mentioned in the comments within the method.

### Corrected Version

```python
class TimeGrouper(Grouper):
    # Other methods and class/imports remain the same

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
            labels = binner.shift(1, freq=self.freq)
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

The corrected version handles adjusting the `labels` based on the `closed` and `label` conditions. This should address the bug and ensure that the test case `test_downsample_dst_at_midnight` passes successfully.