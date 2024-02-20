The relevant input/output values are:
- self._values: `<PeriodArray> ['2019Q1', '2019Q2']`
- self: `PeriodIndex(['2019Q1', '2019Q2'], dtype='period[Q-DEC]', freq='Q-DEC')`

Rational: The input values of self._values and self are likely relevant to the bug as they are used to create _engine, and could potentially be causing the issue.