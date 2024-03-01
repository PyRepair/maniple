### Bug Explanation
The bug in the provided function `table_exists` lies in the condition checking for the presence of the table in the retrieved output. The current implementation checks for an exact match of the table name in the output, leading to incorrect results when the table names are in different cases (e.g., 'mytable' and 'MyTable').

### Bug Fix Strategy
To fix the bug, we need to perform a case-insensitive check for the table name in the output. This will ensure that the function behaves correctly regardless of the case sensitivity of table names.

### Corrected Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in map(str.lower, stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

With this correction, the function will compare the lowercase version of the table names, which makes it case-insensitive and solves the bug that caused incorrect results.