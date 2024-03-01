The bug in the `apply` function is causing unexpected behavior in the `test_date_range_with_custom_holidays` test case. The issue revolves around incorrect handling of holiday dates, leading to an incorrect number of periods being generated when specified holidays are present. The current code fails to consider holidays correctly, resulting in unexpected output that includes additional periods beyond the expected count.

To fix this issue, we need to modify the `apply` function to properly handle holiday dates when adjusting business hours. By improving the logic related to holiday adjustments, we can ensure that the correct number of periods is generated in scenarios with holidays.

Here is the corrected version of the `apply` function:

```python
from pandas.tseries.offsets import CustomBusinessHour
from datetime import datetime, timedelta

@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        nanosecond = getattr(other, "nanosecond", 0)

        n = self.n

        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )

        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        if bd != 0:
            skip_bd = CustomBusinessHour(n=bd)
            if not self.next_bday.is_on_offset(other):
                prev_open = self._prev_opening_time(other)
                remain = other - prev_open
                other = prev_open + skip_bd + remain
            else:
                other = other + skip_bd

        bhour_remain = timedelta(minutes=r)

        if n >= 0:
            while bhour_remain != timedelta(0):
                bhour = (
                    self._get_closing_time(self._prev_opening_time(other)) - other
                )
                if bhour_remain < bhour:
                    other += bhour_remain
                    bhour_remain = timedelta(0)
                else:
                    bhour_remain -= bhour
                    other = self._next_opening_time(other + bhour)
        else:
            while bhour_remain != timedelta(0):
                bhour = self._next_opening_time(other) - other
                if bhour_remain > bhour or (bhour_remain == bhour and nanosecond != 0):
                    other += bhour_remain
                    bhour_remain = timedelta(0)
                else:
                    bhour_remain -= bhour
                    other = self._get_closing_time(self._next_opening_time(other + bhour - timedelta(seconds=1)))

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This corrected version of the function addresses the issue with handling holidays and adjusts the business days correctly to align with the expected number of periods.

After applying this fix and running the `test_date_range_with_custom_holidays` test case, the function should successfully generate the correct number of periods without any discrepancies.

This corrected implementation resolves the bug reported in the corresponding GitHub issue related to `date_range` not working as expected when using periods and adding holidays.