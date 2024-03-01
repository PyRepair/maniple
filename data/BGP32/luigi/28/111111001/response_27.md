### Bug Explanation:
The bug in the `table_exists` function lies in the comparison of the table name in the `stdout` variable. The function checks if the `table` variable is in the `stdout` string, which can lead to false positives if the table name is a substring of another table name in the output.

### Bug Fix:
To fix this bug, we need to ensure an exact match between the table name and the lines in the `stdout`. We can split the `stdout` string by newline characters and check each line individually for an exact match with the table name.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return any(line.strip() == table for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By making the above changes, the corrected function will now compare each line in the `stdout` individually with the table name instead of checking if the table name is present in the whole `stdout` string.