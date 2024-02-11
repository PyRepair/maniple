## Reduced case
### Runtime value and type of the input parameters of the buggy function
ax, value: `DatetimeIndex([...])`, shape: `(49,)`, type: `DatetimeIndex`

self.freq, value: `<Day>`, type: `Day`

self, value: `TimeGrouper(freq=<Day>, axis=0, sort=True, closed='left', label='left', how='mean', convention='e', base=0)`, type: `TimeGrouper`

self.closed, value: `'left'`, type: `str`

ax.tz, value: `<DstTzInfo 'America/Havana' LMT-1 day, 18:31:00 STD>`, type: `America/Havana`

### Runtime value and type of variables right before the buggy function's return
binner, value: `DatetimeIndex([...], dtype='datetime64[ns, America/Havana]', freq='D')`, type: `DatetimeIndex`

labels, value: `DatetimeIndex([...], dtype='datetime64[ns, America/Havana]', freq='D')`, type: `DatetimeIndex`

first, value: `Timestamp('2018-11-03 00:00:00-0400', tz='America/Havana')`, type: `Timestamp`

last, value: `Timestamp('2018-11-06 00:00:00-0500', tz='America/Havana')`, type: `Timestamp`

ax_values, value: `array([...])`, shape: `(49,)`, type: `ndarray`

bin_edges, value: `array([...])`, type: `ndarray`

bins, value: `array([16, 41, 49])`, type: `ndarray`