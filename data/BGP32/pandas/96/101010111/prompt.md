Please fix the buggy function provided below and output a corrected version.
Following these steps:
1. Analyze the buggy function and its relationship with related functions, corresponding error message, the expected input/output values, the GitHub issue.
2. Identify potential error locations within the buggy function.
3. Explain the cause of the bug using the buggy function, the related functions, the corresponding error message, the expected input/output variable values, the GitHub Issue information.
4. Suggest a strategy for fixing the bug.
5. Given the buggy function below, provide a corrected version. The corrected version should pass the failing test, satisfy the expected input/output values, resolve the issue posted in GitHub.


Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
from datetime import date, datetime, timedelta
from pandas._libs.tslibs.offsets import ApplyTypeError, BaseOffset, _get_calendar, _is_normalized, _to_dt64, apply_index_wraps, as_datetime, roll_yearday, shift_month
```

## The source code of the buggy function
```python
# The relative path of the buggy file: pandas/tseries/offsets.py

# This function from the same file, but not the same class, is called by the buggy function
def apply_wraps(func):
    # Please ignore the body of this function

# The declaration of the class containing the buggy function
class BusinessHourMixin(BusinessMixin):
    # This function from the same class is called by the buggy function
    def next_bday(self):
        # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def _next_opening_time(self, other, sign=1):
        # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def _prev_opening_time(self, other):
        # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def _get_business_hours_by_sec(self, start, end):
        # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def _get_closing_time(self, dt):
        # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def is_on_offset(self, dt):
        # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def _is_on_offset(self, dt):
        # Please ignore the body of this function



    # this is the buggy function you need to fix
    @apply_wraps
    def apply(self, other):
        if isinstance(other, datetime):
            # used for detecting edge condition
            nanosecond = getattr(other, "nanosecond", 0)
            # reset timezone and nanosecond
            # other may be a Timestamp, thus not use replace
            other = datetime(
                other.year,
                other.month,
                other.day,
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
            )
            n = self.n
    
            # adjust other to reduce number of cases to handle
            if n >= 0:
                if other.time() in self.end or not self._is_on_offset(other):
                    other = self._next_opening_time(other)
            else:
                if other.time() in self.start:
                    # adjustment to move to previous business day
                    other = other - timedelta(seconds=1)
                if not self._is_on_offset(other):
                    other = self._next_opening_time(other)
                    other = self._get_closing_time(other)
    
            # get total business hours by sec in one business day
            businesshours = sum(
                self._get_business_hours_by_sec(st, en)
                for st, en in zip(self.start, self.end)
            )
    
            bd, r = divmod(abs(n * 60), businesshours // 60)
            if n < 0:
                bd, r = -bd, -r
    
            # adjust by business days first
            if bd != 0:
                skip_bd = BusinessDay(n=bd)
                # midnight business hour may not on BusinessDay
                if not self.next_bday.is_on_offset(other):
                    prev_open = self._prev_opening_time(other)
                    remain = other - prev_open
                    other = prev_open + skip_bd + remain
                else:
                    other = other + skip_bd
    
            # remaining business hours to adjust
            bhour_remain = timedelta(minutes=r)
    
            if n >= 0:
                while bhour_remain != timedelta(0):
                    # business hour left in this business time interval
                    bhour = (
                        self._get_closing_time(self._prev_opening_time(other)) - other
                    )
                    if bhour_remain < bhour:
                        # finish adjusting if possible
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        # go to next business time interval
                        bhour_remain -= bhour
                        other = self._next_opening_time(other + bhour)
            else:
                while bhour_remain != timedelta(0):
                    # business hour left in this business time interval
                    bhour = self._next_opening_time(other) - other
                    if (
                        bhour_remain > bhour
                        or bhour_remain == bhour
                        and nanosecond != 0
                    ):
                        # finish adjusting if possible
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        # go to next business time interval
                        bhour_remain -= bhour
                        other = self._get_closing_time(
                            self._next_opening_time(
                                other + bhour - timedelta(seconds=1)
                            )
                        )
    
            return other
        else:
            raise ApplyTypeError("Only know how to combine business hour with datetime")
    
```

### The error message from the failing test
```text
cls = <class 'pandas.core.arrays.datetimes.DatetimeArray'>
index = <DatetimeArray>
['2020-11-25 15:00:00', '2020-11-25 16:00:00', '2020-11-27 15:00:00',
 '2020-11-27 16:00:00']
Length: 4, dtype: datetime64[ns]
freq = <CustomBusinessHour: CBH=15:00-17:00>, kwargs = {'ambiguous': 'raise'}
inferred = None
on_freq = <DatetimeArray>
['2020-11-25 15:00:00', '2020-11-25 16:00:00', '2020-11-27 15:00:00',
 '2020-11-27 16:00:00', '2020-11...2-11 15:00:00', '2020-12-11 16:00:00',
 '2020-12-14 15:00:00', '2020-12-14 16:00:00']
Length: 26, dtype: datetime64[ns]

    @classmethod
    def _validate_frequency(cls, index, freq, **kwargs):
        """
        Validate that a frequency is compatible with the values of a given
        Datetime Array/Index or Timedelta Array/Index
    
        Parameters
        ----------
        index : DatetimeIndex or TimedeltaIndex
            The index on which to determine if the given frequency is valid
        freq : DateOffset
            The frequency to validate
        """
        if is_period_dtype(cls):
            # Frequency validation is not meaningful for Period Array/Index
            return None
    
        inferred = index.inferred_freq
        if index.size == 0 or inferred == freq.freqstr:
            return None
    
        try:
            on_freq = cls._generate_range(
                start=index[0], end=None, periods=len(index), freq=freq, **kwargs
            )
            if not np.array_equal(index.asi8, on_freq.asi8):
>               raise ValueError
E               ValueError

pandas/core/arrays/datetimelike.py:891: ValueError

During handling of the above exception, another exception occurred:

    def test_date_range_with_custom_holidays():
        # GH 30593
        freq = pd.offsets.CustomBusinessHour(start="15:00", holidays=["2020-11-26"])
        result = pd.date_range(start="2020-11-25 15:00", periods=4, freq=freq)
>       expected = pd.DatetimeIndex(
            [
                "2020-11-25 15:00:00",
                "2020-11-25 16:00:00",
                "2020-11-27 15:00:00",
                "2020-11-27 16:00:00",
            ],
            freq=freq,
        )

pandas/tests/indexes/datetimes/test_date_range.py:954: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pandas/core/indexes/datetimes.py:246: in __new__
    dtarr = DatetimeArray._from_sequence(
pandas/core/arrays/datetimes.py:419: in _from_sequence
    cls._validate_frequency(result, freq, ambiguous=ambiguous)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'pandas.core.arrays.datetimes.DatetimeArray'>
index = <DatetimeArray>
['2020-11-25 15:00:00', '2020-11-25 16:00:00', '2020-11-27 15:00:00',
 '2020-11-27 16:00:00']
Length: 4, dtype: datetime64[ns]
freq = <CustomBusinessHour: CBH=15:00-17:00>, kwargs = {'ambiguous': 'raise'}
inferred = None
on_freq = <DatetimeArray>
['2020-11-25 15:00:00', '2020-11-25 16:00:00', '2020-11-27 15:00:00',
 '2020-11-27 16:00:00', '2020-11...2-11 15:00:00', '2020-12-11 16:00:00',
 '2020-12-14 15:00:00', '2020-12-14 16:00:00']
Length: 26, dtype: datetime64[ns]

    @classmethod
    def _validate_frequency(cls, index, freq, **kwargs):
        """
        Validate that a frequency is compatible with the values of a given
        Datetime Array/Index or Timedelta Array/Index
    
        Parameters
        ----------
        index : DatetimeIndex or TimedeltaIndex
            The index on which to determine if the given frequency is valid
        freq : DateOffset
            The frequency to validate
        """
        if is_period_dtype(cls):
            # Frequency validation is not meaningful for Period Array/Index
            return None
    
        inferred = index.inferred_freq
        if index.size == 0 or inferred == freq.freqstr:
            return None
    
        try:
            on_freq = cls._generate_range(
                start=index[0], end=None, periods=len(index), freq=freq, **kwargs
            )
            if not np.array_equal(index.asi8, on_freq.asi8):
                raise ValueError
        except ValueError as e:
            if "non-fixed" in str(e):
                # non-fixed frequencies are not meaningful for timedelta64;
                #  we retain that error message
                raise e
            # GH#11587 the main way this is reached is if the `np.array_equal`
            #  check above is False.  This can also be reached if index[0]
            #  is `NaT`, in which case the call to `cls._generate_range` will
            #  raise a ValueError, which we re-raise with a more targeted
            #  message.
>           raise ValueError(
                f"Inferred frequency {inferred} from passed values "
                f"does not conform to passed frequency {freq.freqstr}"
            )
E           ValueError: Inferred frequency None from passed values does not conform to passed frequency CBH

pandas/core/arrays/datetimelike.py:902: ValueError

```



## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-25 15:00:00')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `25`, type: `int`

other.hour, expected value: `15`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `3`, type: `int`

self, expected value: `<3 * CustomBusinessHours: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `Timestamp('2020-11-27 16:00:00')`, type: `Timestamp`

nanosecond, expected value: `0`, type: `int`

other.day, expected value: `27`, type: `int`

other.hour, expected value: `16`, type: `int`

n, expected value: `3`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `1`, type: `int`

r, expected value: `60`, type: `int`

skip_bd, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `Timedelta('0 days 02:00:00')`, type: `Timedelta`

### Expected case 2
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-25 15:00:00')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `25`, type: `int`

other.hour, expected value: `15`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `1`, type: `int`

self, expected value: `<CustomBusinessHour: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `datetime.datetime(2020, 11, 25, 16, 0)`, type: `datetime`

nanosecond, expected value: `0`, type: `int`

other.hour, expected value: `16`, type: `int`

n, expected value: `1`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `0`, type: `int`

r, expected value: `60`, type: `int`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `datetime.timedelta(seconds=7200)`, type: `timedelta`

### Expected case 3
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-25 16:00:00')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `25`, type: `int`

other.hour, expected value: `16`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `1`, type: `int`

self, expected value: `<CustomBusinessHour: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `datetime.datetime(2020, 11, 27, 15, 0)`, type: `datetime`

nanosecond, expected value: `0`, type: `int`

other.day, expected value: `27`, type: `int`

other.hour, expected value: `15`, type: `int`

n, expected value: `1`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `0`, type: `int`

r, expected value: `60`, type: `int`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `datetime.timedelta(seconds=3600)`, type: `timedelta`

### Expected case 4
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-27 15:00:00')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `27`, type: `int`

other.hour, expected value: `15`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `1`, type: `int`

self, expected value: `<CustomBusinessHour: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `datetime.datetime(2020, 11, 27, 16, 0)`, type: `datetime`

nanosecond, expected value: `0`, type: `int`

other.hour, expected value: `16`, type: `int`

n, expected value: `1`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `0`, type: `int`

r, expected value: `60`, type: `int`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `datetime.timedelta(seconds=7200)`, type: `timedelta`

### Expected case 5
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-25 15:00:00', freq='CBH')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `25`, type: `int`

other.hour, expected value: `15`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `3`, type: `int`

self, expected value: `<3 * CustomBusinessHours: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `Timestamp('2020-11-27 16:00:00')`, type: `Timestamp`

nanosecond, expected value: `0`, type: `int`

other.day, expected value: `27`, type: `int`

other.hour, expected value: `16`, type: `int`

n, expected value: `3`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `1`, type: `int`

r, expected value: `60`, type: `int`

skip_bd, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `Timedelta('0 days 02:00:00')`, type: `Timedelta`

### Expected case 6
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-25 15:00:00', freq='CBH')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `25`, type: `int`

other.hour, expected value: `15`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `1`, type: `int`

self, expected value: `<CustomBusinessHour: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `datetime.datetime(2020, 11, 25, 16, 0)`, type: `datetime`

nanosecond, expected value: `0`, type: `int`

other.hour, expected value: `16`, type: `int`

n, expected value: `1`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `0`, type: `int`

r, expected value: `60`, type: `int`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `datetime.timedelta(seconds=7200)`, type: `timedelta`

### Expected case 7
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-25 16:00:00')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `25`, type: `int`

other.hour, expected value: `16`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `1`, type: `int`

self, expected value: `<CustomBusinessHour: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `datetime.datetime(2020, 11, 27, 15, 0)`, type: `datetime`

nanosecond, expected value: `0`, type: `int`

other.day, expected value: `27`, type: `int`

other.hour, expected value: `15`, type: `int`

n, expected value: `1`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `0`, type: `int`

r, expected value: `60`, type: `int`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `datetime.timedelta(seconds=3600)`, type: `timedelta`

### Expected case 8
#### The values and types of buggy function's parameters
other, expected value: `Timestamp('2020-11-27 15:00:00')`, type: `Timestamp`

other.year, expected value: `2020`, type: `int`

other.month, expected value: `11`, type: `int`

other.day, expected value: `27`, type: `int`

other.hour, expected value: `15`, type: `int`

other.minute, expected value: `0`, type: `int`

other.second, expected value: `0`, type: `int`

other.microsecond, expected value: `0`, type: `int`

self.n, expected value: `1`, type: `int`

self, expected value: `<CustomBusinessHour: CBH=15:00-17:00>`, type: `CustomBusinessHour`

self.end, expected value: `(datetime.time(17, 0),)`, type: `tuple`

self.start, expected value: `(datetime.time(15, 0),)`, type: `tuple`

self.weekmask, expected value: `'Mon Tue Wed Thu Fri'`, type: `str`

self.holidays, expected value: `(numpy.datetime64('2020-11-26'),)`, type: `tuple`

self.next_bday, expected value: `<CustomBusinessDay>`, type: `CustomBusinessDay`

#### Expected values and types of variables right before the buggy function's return
other, expected value: `datetime.datetime(2020, 11, 27, 16, 0)`, type: `datetime`

nanosecond, expected value: `0`, type: `int`

other.hour, expected value: `16`, type: `int`

n, expected value: `1`, type: `int`

businesshours, expected value: `7200`, type: `int`

bd, expected value: `0`, type: `int`

r, expected value: `60`, type: `int`

bhour_remain, expected value: `datetime.timedelta(0)`, type: `timedelta`

bhour, expected value: `datetime.timedelta(seconds=7200)`, type: `timedelta`



## A GitHub issue for this bug

The issue's title:
```text
Pandas date_range does not work when using periods and adding holiday
```

The issue's detailed description:
```text
This code works fine

pd.date_range(start='2020-11-25 10:00',periods=14,
              freq=pd.offsets.CustomBusinessHour(start='10:00'))
but if I add holidays then it produces more than 14 periods

pd.date_range(start='2020-11-25 10:00',periods=14,
              freq=pd.offsets.CustomBusinessHour(start='10:00',holidays=['2020-11-26']))
Output:

DatetimeIndex(['2020-11-25 10:00:00', '2020-11-25 11:00:00',
               '2020-11-25 12:00:00', '2020-11-25 13:00:00',
               '2020-11-25 14:00:00', '2020-11-25 15:00:00',
               '2020-11-25 16:00:00', '2020-11-27 10:00:00',
               '2020-11-27 11:00:00', '2020-11-27 12:00:00',
               '2020-11-27 13:00:00', '2020-11-27 14:00:00',
               '2020-11-27 15:00:00', '2020-11-27 16:00:00',
               '2020-11-30 10:00:00', '2020-11-30 11:00:00',
               '2020-11-30 12:00:00', '2020-11-30 13:00:00',
               '2020-11-30 14:00:00', '2020-11-30 15:00:00',
               '2020-11-30 16:00:00', '2020-12-01 10:00:00',
               '2020-12-01 11:00:00', '2020-12-01 12:00:00',
               '2020-12-01 13:00:00', '2020-12-01 14:00:00',
               '2020-12-01 15:00:00', '2020-12-01 16:00:00',
               '2020-12-02 10:00:00', '2020-12-02 11:00:00',
               '2020-12-02 12:00:00'],
              dtype='datetime64[ns]', freq='CBH')
If I replace periods with the corresponding end then everything works fine.

pd.date_range(start='2020-11-25 10:00',end='2020-11-27 16:00:00',
              freq=pd.offsets.CustomBusinessHour(start='10:00',holidays=['2020-11-26']))
I am not sure why date_range has this weird behavior. Appreciate any help.
```



