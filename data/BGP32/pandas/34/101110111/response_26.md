To fix the bug in the `_get_time_bins` function, we need to address the issue related to the AmbiguousTimeError on clock change day in Cuba. The bug originates from the wrong handling of the time bins on the day with the clock change. To resolve this bug, we should adjust the method to handle the ambiguous timestamp correctly.

Here is an updated version of `_get_time_bins` function:

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
    
    closed_param = 'right' if self.closed == 'right' else 'left'
    
    # Performing custom handling for the ambiguous time error
    if ax.tz._transition_info is not None:
        dts = pd.DatetimeIndex(data=[first, last], tz=ax.tz)
        index_date = date_range(start=dts.min(), end=dts.max(), freq=self.freq, tz=dts.tz, closed=closed_param)
        
        binner = date_range(start=index_date.min(), end=index_date.max(), freq=self.freq, tz=index_date.tz, closed=closed_param)
        labels = binner.drop_duplicates()
    
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

    # if we end up with more labels than bins
    # adjust the labels
    if len(bins) < len(labels):
        labels = labels[: len(bins)]

    return binner, bins, labels
```

This updated function includes additional logic to handle the AmbiguousTimeError by identifying the transition period in the timezone information and adjusting the time bins accordingly for the ambiguous timestamp. The `tz._transition_info` check helps to detect if the timezone has a transition information. 

By implementing this adjustment, the function should now correctly group time bins on days with a clock change, resolving the AmbiguousTimeError.