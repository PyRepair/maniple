GitHub Bug Title:
TypeError when using the groupby method with axis=1 and column names

Description:
When using the groupby method along with axis=1 and column names, a KeyError is raised even though the intent is to group by columns with the specified column label. The documentation for groupby() also indicates that "A str or list of strs may be passed to group by the columns." 

Expected Output:
A dataframe with index [0, 1, 0] but grouped (and summed) columns [10, 20].

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- pandas: (version not provided)

```python
# code sample not provided
```