You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
GroupBy(axis=1) Does Not Offer Implicit Selection By Columns Name(s)
```

## The associated detailed issue description
```text
Code Sample, a copy-pastable example if possible
import pandas as pd
import numpy as np

df = pd.DataFrame(np.arange(12).reshape(3, 4), index=[0, 1, 0], columns=[10, 20, 10, 20])
df.index.name = "y"
df.columns.name = "x"

print df

print
print "Grouped along index:"
print df.groupby(by="y").sum()

print
print "Grouped along columns:"
# The following raises a KeyError even though  "x" is a column name
# (like "y" above, which is an index name):
df.groupby(by="x", axis=1).sum()
Problem description
The exception at the end is surprising: the intent is clearly to group by columns, on the "x" column label.

Furthermore, the documentation for groupby() seems to confirm this, as it states for the "by" argument that "A str or list of strs may be passed to group by the columns in self".

Expected Output
A dataframe with index [0, 1, 0] but grouped (and summed) columns [10, 20].

I wasn't able to test with the latest Pandas version, sorry!
```

