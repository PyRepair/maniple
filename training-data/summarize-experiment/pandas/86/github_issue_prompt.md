You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
BUG: Wrong error message is raised when columns=None in df.pivot
```

## The associated detailed issue description
```text
From docstring, index and values can be optional in df.pivot, but columns is not

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html
index : string or object, optional
Column to use to make new frame’s index. If None, uses existing index.

columns : string or object
Column to use to make new frame’s columns.

However, the error message is confusing now, should raise columns is not optional.

Code example:
>>> df = pd.DataFrame({"foo": ['one', 'one', 'two', 'two'],"bar": ['A', 'A', 'B', 'C'],"baz": [1, 2, 3, 4]})
>>> df.pivot(columns=None)

KeyError: 'None of [None] are in the columns'
```

