# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if values is None:
        cols = [columns] if index is None else [index, columns]
        append = index is None
        indexed = data.set_index(cols, append=append)
    else:
        if index is None:
            index = data.index
        else:
            index = data[index]
        index = MultiIndex.from_arrays([index, data[columns]])

        if is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data._constructor(
                data[values].values, index=index, columns=values
            )
        else:
            indexed = data._constructor_sliced(data[values].values, index=index)
    return indexed.unstack(columns)

```

The github issue message is:
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



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


