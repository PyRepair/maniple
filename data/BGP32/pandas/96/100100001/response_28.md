### Analysis:
The buggy function `apply(self, other)` is designed to adjust a given datetime object according to a custom business hour offset. However, it fails to handle the case when the adjustment involves skipping non-business days using the `BusinessDay` object. This leads to incorrect adjustments and causes the failing test `test_date_range_with_custom_holidays` to fail.

### Identified Bug:
The bug lies in the section where the function attempts to adjust by business days first using a `BusinessDay` object. The logic for handling non-business days is flawed and does not correctly skip non-business days, leading to incorrect results.

### Bug Fix Strategy:
To fix the bug, the logic for skipping non-business days using the `BusinessDay` object needs to be revised. The function should correctly identify non-business days and adjust the datetime object accordingly before proceeding with the remaining business hour adjustments.

### Corrected Version:
```python
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
            if isinstance(self, CustomBusinessHour):
                start_of_day = datetime(other.year, other.month, other.day, 0, 0, 0)
                business_days = pd.offsets.CustomBusinessDay(holidays=self.holidays)
                other = (start_of_day + bd * business_days).to_pydatetime()

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

By modifying the logic to correctly skip non-business days when adjusting by business days using a `CustomBusinessDay` object, we ensure that the correct adjustment is applied based on the provided holidays. This corrected version of the function should now pass the failing test scenario.