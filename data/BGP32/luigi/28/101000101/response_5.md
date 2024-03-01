### Analysis
The buggy function `table_exists` has two branches based on whether a `partition` is provided or not. In the case where a `partition` is present, it calls `run_hive_cmd` with a specific command string. However, in the provided buggy code, there is a formatting issue in the command string when querying for partitions, which is likely causing an error.

### Bug Explanation
The bug in the function arises from the incorrect formatting of the command string used when querying for partitions. The `%s` placeholders are not being correctly replaced with the values of `database`, `table`, and `self.partition_spec(partition)` due to the triple quotes and incorrect usage. This leads to an incorrect command being passed to `run_hive_cmd`, resulting in unexpected output.

### Bug Fix Strategy
To fix the bug, we need to properly format the command string when querying for partitions by using an f-string or `.format()` method to correctly replace the placeholders `%s` with the values of `database`, `table`, and `self.partition_spec(partition)`.

### Corrected Code
```python
# The corrected version of the buggy function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))

        return bool(stdout)
```

The corrected version uses proper string formatting to construct the command string for querying partitions, ensuring that the placeholders are replaced correctly with the respective values. This should resolve the bug and make the function behave as expected in all test cases.