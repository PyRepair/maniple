### Bug Explanation
The bug in the `table_exists` function stems from the condition for checking if the table exists in the Hive database. The function checks if the table name is present in the output of the Hive command, but the comparison is flawed, leading to incorrect results. In some cases, the table name might be part of another output string causing the check to fail.

### Bug Fix Strategy
To fix the bug, we need to enhance the comparison mechanism to ensure that only the exact table name match is considered. We can achieve this by splitting the stdout output into lines and then checking if the table name matches exactly with one of the lines.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

This correction splits the output into lines and checks for an exact match of the table name, ensuring the proper identification of table existence in the Hive database.