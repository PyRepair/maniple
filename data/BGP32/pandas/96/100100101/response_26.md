### Bug Explanation
The bug in the `apply` function results from the incorrect calculation of business days and business hours adjustments. There are several issues in the logic:
1. In the case where `n >= 0`, the function should check if the current time is in the `self.end` time range and if `other` is on the offset. However, due to improper condition checking, the adjustment logic does not handle all scenarios correctly.
2. In the case where `n < 0`, the adjustment logic for moving to the previous business day and next opening time is not implemented accurately, leading to incorrect adjustments.

### Bug Fix Strategy
To fix the bug in the `apply` function:
1. Ensure that the adjustments for business days and business hours are correctly calculated based on the specified offset `n`.
2. Implement the adjustment logic for both positive and negative `n` values to handle the cases of moving to the next or previous business day, and adjusting the business hours accordingly.

### Corrected Function
Here is the corrected version of the `apply` function:

```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        n = self.n

        businesshours = sum(self._get_business_hours_by_sec(st, en) for st, en in zip(self.start, self.end))

        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        other = other.replace(minute=0, second=0, microsecond=0)  # reset minutes, seconds, and microseconds

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

        if bd != 0:
            skip_bd = BusinessDay(n=bd)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
            other = other + skip_bd

        bhour_remain = timedelta(minutes=r)

        while bhour_remain != timedelta(0):
            bhour = self._get_closing_time(self._prev_opening_time(other)) - other if n >= 0 else self._next_opening_time(other) - other
            if bhour_remain < bhour:
                other += bhour_remain
                bhour_remain = timedelta(0)
            else:
                bhour_remain -= bhour
                if n >= 0:
                    other = self._next_opening_time(other + bhour)
                else:
                    other = self._get_closing_time(self._next_opening_time(other + bhour - timedelta(seconds=1)))

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")

```

With this corrected version, the `apply` function should now handle the adjustments for business days and business hours correctly, passing the failing test case provided.