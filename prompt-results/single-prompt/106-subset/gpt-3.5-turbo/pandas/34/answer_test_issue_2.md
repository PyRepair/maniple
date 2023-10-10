```python
import pandas as pd
from pandas.core.groupby.grouper import raise_ambiguous_time_error
from pandas._libs.tslibs import NaT
from pandas.tseries.frequencies import to_offset

def _get_time_bins(self, ax):
    if not isinstance(ax, pd.DatetimeIndex):
        raise TypeError(
            "axis must be a DatetimeIndex, but got "
            f"an instance of {type(ax).__name__}"
        )

    if len(ax) == 0:
        binner = labels = pd.DatetimeIndex(data=[], freq=self.freq, name=ax.name)
        return binner, [], labels

    first, last = pd._libs.tslibs.timestamps._get_timestamp_range_edges(
        ax.min(), ax.max(), self.freq, closed=self.closed, base=self.base
    )
    # GH #12037
    # use first/last directly instead of call replace() on them
    # because replace() will swallow the nanosecond part
    # thus last bin maybe slightly before the end if the end contains
    # nanosecond part and lead to `Values falls after last bin` error
    binner = labels = pd.date_range(
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
    bins = pd._libs.ops.interval.generate_bins_mm(
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

def test_downsample_dst_at_midnight():
    # GH 25758
    start = pd.Timestamp(2018, 11, 3, 12)
    end = pd.Timestamp(2018, 11, 5, 12)
    index = pd.date_range(start, end, freq="1H")
    index = index.tz_localize("UTC").tz_convert("America/Havana")
    data = list(range(len(index)))
    dataframe = pd.DataFrame(data, index=index)
    result = dataframe.groupby(pd.Grouper(freq="1D", ambiguous='infer', base=to_offset('H'))).mean()
    expected = pd.DataFrame(
        [7.5, 28.0, 44.5],
        index=pd.date_range("2018-11-03", periods=3).tz_localize(
            "America/Havana", ambiguous='infer'
        ),
    )
    pd.testing.assert_frame_equal(result, expected)
```