### Bug Explanation
The bug in the `table_exists` function lies in the comparison between the `table` and `stdout` values. The condition `table in stdout` is checking if the entire table name is present in the `stdout` string, which can lead to false negatives in cases where the table name is part of another string in `stdout`.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison condition to properly check if the table name is present as a separate entity in the `stdout` string. One way to achieve this is by splitting the `stdout` string based on newlines and then checking if the `table` name is present in any of the resulting strings.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

With this correction, we split the `stdout` string by newline characters and check if the `table` name is present in any of the substrings. This will ensure that we correctly identify the presence of the table in the `stdout` output.