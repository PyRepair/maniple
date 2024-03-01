The bug in the `apply` function is causing the `test_date_range_with_custom_holidays` test to fail. The issue stems from how the function handles the adjustment of `other` datetime values based on the given CustomBusinessHour offset.

The bug seems to be related to the calculation of business days and business hours. Due to incorrect handling of business day adjustments and remaining business hours, the resulting output is not aligned with the expected behavior.

To fix the bug, we need to carefully adjust the business day and business hour calculations in the `apply` function to ensure that the `other` datetime values align correctly with the CustomBusinessHour offset.

Here's a corrected version of the `apply` function:

```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        # used for detecting edge condition
        nanosecond = getattr(other, 'nanosecond', 0)

        # reset timezone and nanosecond
        # other may be a Timestamp, thus not use replace
        other = datetime(
            other.year,
            other.month,
            other.day,
            other.hour,
            other.minute,
            other.second,
            other.microsecond
        )
        n = self.n

        if self._is_on_offset(other):
            return other

        # adjust the other datetime based on the Custom Business Hour offset
        adjusted_time = other.time()
        if n >= 0:
            if adjusted_time < self.start:
                other = self._next_opening_time(other)
            elif adjusted_time >= self.end:
                other = self._next_opening_time(other.replace(hour=self.start.hour)) + self

        else:
            if adjusted_time <= self.start:
                other = self._prev_opening_time(other) - self
            elif adjusted_time > self.end:
                other = self._prev_opening_time(other).replace(hour=self.end.hour)

        return other

    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This corrected version focuses on adjusting the `other` datetime value correctly based on the CustomBusinessHour offset, ensuring it aligns with the start and end times specified.

With this fix, the `test_date_range_with_custom_holidays` test should now pass successfully.