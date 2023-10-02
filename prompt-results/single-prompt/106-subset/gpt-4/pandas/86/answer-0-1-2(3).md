You should add an exception at the beginning of the pivot method to check if the columns parameter is None, because according to the method docstring, this parameter should not be optional:

Here is the fixed source code:

@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if columns is None:
        raise TypeError('pivot() missing 1 required argument: \'columns\'')
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

Now, running the previously failing test:

    def test_pivot_columns_none_raise_error(self):
        # GH 30924
        df = pd.DataFrame(
            {"col1": ["a", "b", "c"], "col2": [1, 2, 3], "col3": [1, 2, 3]}
        )
        msg = r"pivot\(\) missing 1 required argument: 'columns'"
        with pytest.raises(TypeError, match=msg):
            df.pivot(index="col1", values="col3")

will yield the expected result and pass.