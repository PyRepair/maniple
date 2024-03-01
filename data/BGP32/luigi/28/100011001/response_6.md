### Bug Explanation:
The bug in the `table_exists` function stems from the comparison operation when checking if a table exists in the Hive database. The function checks if the table name is present in the output received from the Hive command. However, in the current implementation, the check is not accurate. It only checks if the table name is a substring of the output, leading to incorrect evaluation.

### Bug Location:
The bug is in the comparison operation where it checks if the table name is in the stdout returned from the Hive command. The condition `table in stdout` is not a precise way to check the presence of the table in the output.

### Bug Fix:
To fix the bug, we need to modify the condition where we check if the table name is exactly in the output. We should split the output by lines and then check if the table name is present in any of the lines. This way, we can accurately determine if the table exists in the database.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return any(table == line.strip() for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```