# Bug Title
DataFrame.equals() returns True for identical blocks with different locations

## Description
When using the DataFrame.equals() method on two DataFrames with identical blocks but different locations, it incorrectly returns True instead of False. This behavior is unexpected and needs to be fixed.

## Code Sample
```python
import pandas as pd

df3 = pd.DataFrame({'a': [1, 2], 'b': ['s', 'd']})
df4 = pd.DataFrame({'a': ['s', 'd'], 'b': [1, 2]})
df3.equals(df4)
```

## Expected Output
I expected the DataFrame.equals() method to return False, but it is returning True.

## Environment
- Python version: 3.6.8
- Pandas version: 0.25.0
- Numpy version: 1.16.4
- Operating System: Windows 10