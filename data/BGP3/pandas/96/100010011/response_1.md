Here's a corrected version of the buggy function:

```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        #... (rest of the function remains the same)

        on_freq = DatetimeArray._from_sequence(result,errorMessage)
        if not np.array_equal(index.asi8, on_freq.asi8):
            raise ValueError(
                f"Inferred frequency {inferred} from passed values "
                f"does not conform to passed frequency {freq.freqstr}"
            )
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")

    #... (rest of the function remains the same)
```

Explanation:
The bug was in the line `on_freq = cls._generate_range(start=index[0], end=None, periods=len(index), freq=freq, **kwargs)`.
When the date range is generated with a custom business hour, the engine regards these dates as a reference for business hours' summation. Therefore, when adding a custom holiday, the resulted dates are changed due to adjusting for business days.