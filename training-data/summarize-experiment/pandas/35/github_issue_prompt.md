You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
BUG: Copying PeriodIndex levels on MultiIndex loses weakrefs
```

## The associated detailed issue description
```text
As per comment by @jacobaustin123:
import pandas as pd
idx = pd.MultiIndex.from_arrays([pd.PeriodIndex([pd.Period("2019Q1"), pd.Period("2019Q2")], name='b')])
idx2 = pd.MultiIndex.from_arrays([idx._get_level_values(level) for level in range(idx.nlevels)])
all(x.is_monotonic for x in idx2.levels) # raises an error

Problem description
The weakly referenced PeriodIndex er dropped before intended, so the PeriodEngine gets a None instead of the PeriodIndex.

Expected Output
The above should return True.
```

