## GitHub Issue: AmbiguousTimeError on clock change day in Cuba

### Description:
The groupby function with daily frequency fails with an AmbiguousTimeError on a clock change day in Cuba, causing unexpected behavior.

### Code Sample:
```
import pandas as pd
from datetime import datetime

start = datetime(2018, 11, 3, 12)
end = datetime(2018, 11, 5, 12)
index = pd.date_range(start, end, freq="1H")
index = index.tz_localize('UTC').tz_convert('America/Havana')
data = list(range(len(index)))
dataframe = pd.DataFrame(data, index=index)
groups = dataframe.groupby(pd.Grouper(freq='1D'))
```

### Problem:
On a long clock-change day in Cuba, e.g 2018-11-04, midnight local time is an ambiguous timestamp. The `pd.Grouper` function does not handle this as expected and raises an `AmbiguousTimeError`.

This issue is similar to #23742 but seems to be unresolved.

### Expected Output:
The call to groupby should return three groups (one for each day, 3rd, 4th, and 5th of November). The group for the 4th of November should be labeled as '2018-11-04 00:00:00-04:00' (the first midnight, before the clock change) and should contain the 25 hourly data points for this day.

### Environment:
- Python: 3.6.8
- pandas: 0.24.2
- Operating System: Linux (x86_64)