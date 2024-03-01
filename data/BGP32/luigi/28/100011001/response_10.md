### Bug Explanation
The bug in the `table_exists` function lies in the condition used to determine if the table exists. The function is checking if the table name is present in the output from the `run_hive_cmd` function. However, the condition `stdout and table in stdout` is flawed. This condition returns `False` in cases where the `stdout` contains the table name as a substring, resulting in incorrect evaluations.

### Bug Fix Strategy
To fix the bug, we need to modify the condition for checking table existence. Instead of checking for a substring match, we should split the lines in the output and compare the table name directly.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        tables = stdout.split("\n")
        
        return any(t.strip().lower() == table.lower() for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        
        return bool(stdout)
```

With this corrected version, the function will split the output by newline character, check each line for an exact match with the table name (ignoring case), and return `True` if the table is found in the list of tables or if the partition data is returned.