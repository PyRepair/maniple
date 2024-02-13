You have been provided with a description for GitHub issue. However, it may be ambiguous, please simplify it and make it readable by developer while keeping the key information.

Here is an example summary of a GitHub issue:

GitHub Bug Title:
TypeError when calling mean on a DataFrameGroupBy with Int64 dtype

Description:
Using the new nullable integer data type, calling mean after grouping results in a TypeError. It works with int64 dtype and also with Int64 dtype when taking a single column to give a SeriesGroupBy. The error occurs with median and std as well. However, it does not occur with min, max, or first.

Expected Output:
When performing aggregation operations on a DataFrameGroupBy object with columns of nullable integer data type (Int64), the following behaviours are expected for the specified methods:
mean(): The method should compute the mean of grouped data without raising a TypeError.
median():The method should compute the median of grouped data without raising a TypeError.
std(): The method should compute the standard deviation of grouped data without raising a TypeError.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0


# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/contrib/hive.py



    # this is the buggy function you need to fix
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
    
```


# A GitHub issue title for this bug
```text
hive table_exists should be case insensitive?
```

## The GitHub issue's detailed description
```text
Any thoughts on this one?\n\nIn https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L141\n(possibly here too, but we're not on CDH: https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L192)\n\nSometimes we have tables that are defined as capitalized, rather than lower case underscored names. These are easier to read in code if left capitalized, though hive is case insensitive, and will return them as lower case.\n\nE.g. when checking for an existing table table = 'FooBar', stdout will return with foobar and the test will fail\n\nThis wasn't an issue in older versions, which just checked for string \"does not exist\" or \"Table not found\" in stdout.\n\nWould be easy to fix using return stdout and table.lower() in stdout or return stdout and table.lower() in stdout.lower()\n\nLet me know your thoughts on this. I can supply a pull request if necessary.\n\nThanks,\nLin.
```

# A GitHub issue title for this bug
```text
Fix #896: make table_exists case insensitive
```

## The GitHub issue's detailed description
```text
Check stdout against table.lower() to avoid case issues
```