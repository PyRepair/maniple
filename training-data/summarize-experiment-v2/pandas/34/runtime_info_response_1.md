Input:
ax = DatetimeIndex(['2018-11-03 08:00:00-04:00'...], freq='H')
self.freq = <Day>
self.closed = 'left'
self.base = 0
self
ax.tz = <DstTzInfo 'America/Havana' LMT-1 day, 18:31:00 STD>
ax.asi8 = array([...]), shape (49,)
ax.hasnans = False
self.label = 'left'

Output:
binner = DatetimeIndex(['2018-11-03 00:00:00-04:00', '2018-11-04 00:00:00-04:00', '2018-11-05 00:00:00-05:00', '2018-11-06 00:00:00-05:00'], dtype='datetime64[ns, America/Havana]', freq='D')
labels = DatetimeIndex(['2018-11-03 00:00:00-04:00', '2018-11-04 00:00:00-04:00', '2018-11-05 00:00:00-05:00'], dtype='datetime64[ns, America/Havana]', freq='D')
first = Timestamp('2018-11-03 00:00:00-0400', tz='America/Havana')
last = Timestamp('2018-11-06 00:00:00-0500', tz='America/Havana')
ax_values = array([...]), shape (49,)
bin_edges = array([...])
bins = array([16, 41, 49])