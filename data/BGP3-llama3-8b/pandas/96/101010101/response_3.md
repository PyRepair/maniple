Here is the corrected version of the function:
```
    @apply_wraps
    def apply(self, other):
        if isinstance(other, datetime):
            nanosecond = getattr(other, "nanosecond", 0)
            other = datetime(other.year, other.month, other.day, other.hour, other.minute, other.second, other.microsecond)
            n = self.n
            if n >= 0:
                if other.time() in self.end or not self._is_on_offset(other):
                    other = self._next_opening_time(other)
            else:
                if other.time() in self.start:
                    other = other - timedelta(seconds=1)
                if not self._is_on_offset(other):
                    other = self._next_opening_time(other)
                    other = self._get_closing_time(other)
            businesshours = sum(self._get_business_hours_by_sec(st, en) for st, en in zip(self.start, self.end))
            bd, r = divmod(abs(n * 60), businesshours // 60)
            if n < 0:
                bd, r = -bd, -r
            if bd!= 0:
                skip_bd = BusinessDay(n=bd)
                if not self.next_bday.is_on_offset(other):
                    prev_open = self._prev_opening_time(other)
                    remain = other - prev_open
                    other = prev_open + skip_bd + remain
                else:
                    other = other + skip_bd
            bhour_remain = timedelta(minutes=r)
            while bhour_remain!= timedelta(0):
                bhour = (self._prev_opening_time(other + timedelta(minutes=1)) - other).total_seconds() / 60
                if bhour_remain < bhour:
                    other += bhour_remain
                    bhour_remain = timedelta(0)
                else:
                    bhour_remain -= bhour
                    other = self._next_opening_time(other + timedelta(minutes=1))
            return other
        else:
            raise ApplyTypeError("Only know how to combine business hour with datetime")
```
This function has been fixed to correctly adjust the `other` datetime object based on the business hours and the offset rules specified by the `CustomBusinessHour` and `CustomBusinessDay` classes. The correct approach is to adjust the `other` datetimes by skipping the business days and remaining business hours at the end, if necessary.