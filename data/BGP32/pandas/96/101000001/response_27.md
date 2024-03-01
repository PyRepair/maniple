The bug in the provided function `apply` arises from the incorrect assignment of the `n` variable and the logic for adjusting the business hours. The main issue is with the computation of the `bd` and `r` variables which are used to adjust the `other` datetime based on the business hours.

Here is a corrected version of the `apply` function with the necessary fixes:
```python
    @classmethod
    def apply(cls, self, other):
        if isinstance(other, datetime):
            # reset timezone and nanosecond
            other = other.replace(tzinfo=None, microsecond=0)
            n = self.n

            if n >= 0:
                if other.time() not in self.start or not self._is_on_offset(other):
                    other = self._next_opening_time(other)
            else:
                if other.time() in self.start:
                    other = other - timedelta(seconds=1)
                if not self._is_on_offset(other):
                    other = self._next_opening_time(other)
                    other = self._get_closing_time(other)

            businesshours = sum(
                self._get_business_hours_by_sec(st, en)
                for st, en in zip(self.start, self.end)
            )

            bd, r = divmod(abs(n), businesshours // 60)
            if n < 0:
                bd, r = -bd, -r

            if bd != 0:
                skip_bd = BusinessDay(n=bd)
                if not self.next_bday().is_on_offset(other):
                    prev_open = self._prev_opening_time(other)
                    remain = other - prev_open
                    other = prev_open + skip_bd + remain
                else:
                    other = other + skip_bd

            bhour_remain = timedelta(minutes=r)

            if n >= 0:
                while bhour_remain != timedelta(0):
                    bhour = self._get_closing_time(self._next_opening_time(other)) - other
                    if bhour_remain < bhour:
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        bhour_remain -= bhour
                        other = self._next_opening_time(other + bhour)
            else:
                while bhour_remain != timedelta(0):
                    bhour = self._next_opening_time(other) - other
                    if bhour_remain >= bhour:
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        bhour_remain -= bhour
                        other = self._next_opening_time(other)

            return other
        else:
            raise ApplyTypeError("Only know how to combine business hour with datetime")
```

In this corrected version of the `apply` function, the computation of the `bd` and `r` values has been modified to handle negative values correctly. Additionally, adjustments have been made in the while loops to correctly adjust the `other` datetime based on the business hours.

By fixing these issues, the function should now work as intended and return the adjusted datetime based on the provided business hours.