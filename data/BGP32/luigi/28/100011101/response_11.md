### Bug Explanation
The bug appears to be related to the comparison between the table name and the output from the `run_hive_cmd` function. In both cases, the function checks if the table name is present in the output. However, in the failing test cases, the function fails to correctly interpret whether the table exists based on the output.

In the failing tests, when the table does exist, the function should return `True`, but the incorrect comparison logic leads to a `False` return.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to correctly check if the table name is present in the output from the `run_hive_cmd` function. We also need to account for potential variations in the output format, such as whitespaces or newline characters.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.strip() in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

This corrected version of the function correctly handles the comparison by stripping whitespace and newline characters and splitting the output to check if the table name is present in the list.