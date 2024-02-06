You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
round method fails when columns are CategoricalIndex of IntervalIndex
```

## The associated detailed issue description
```text
Code Sample, a copy-pastable example if possible
cols = pd.interval_range(0, 2)
data = np.random.rand(5, 2)

df = pd.DataFrame(data, columns=cols)
df.round() # works

cols2 = pd.CategoricalIndex(cols)
df2 = pd.DataFrame(data, columns=cols2)
df2.round() # fails

TypeError: No matching signature found
Problem description
The round method fails whenever the columns are CategoricalIndex made from an IntervalIndex. The pd.cut function creates these types of value and they can appear in columns when using pivot_table.

Expected Output
Should round as normal.
```

