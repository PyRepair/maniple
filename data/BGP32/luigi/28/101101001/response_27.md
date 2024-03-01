### Bug Explanation:
1. The bug lies in the `table_exists` function where the condition to check if a table exists in the given database is incorrect.
2. When there is no partition specified, the function fetches the tables using a Hive command and checks if the desired table is in the output. However, the comparison is faulty.
3. The bug occurs because in the condition `return stdout and table in stdout`, the `stdout` variable is a string containing output from the hive command, but the comparison with `table` directly doesn't account for the formatting of this output. It should check for table names separated by newlines.
4. A strategy to fix this bug would be to split the `stdout` string by newlines and then check if the `table` exists in the resulting list.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.strip().split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```