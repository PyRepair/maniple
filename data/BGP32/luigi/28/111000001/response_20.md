## Explanation of the Bug:

The bug in the `table_exists` function arises from the way the `run_hive_cmd` function is being called within the `HiveCommandClient` class. The `run_hive_cmd` function is not being called with the proper arguments, leading to potential errors in the command execution.

In the case of calling `run_hive_cmd` with the SQL query `"use %s; show partitions %s partition (%s)"`, the substitution fields `%s` are not being properly replaced with the values of `database`, `table`, and `self.partition_spec(partition)` respectively. This can result in incorrect queries being sent to Hive.

## Strategy for Fixing the Bug:

To fix the bug in the `table_exists` function, we need to ensure that the `run_hive_cmd` function is called with the correct arguments and that the SQL queries being constructed are formed properly. This involves correctly substituting the values into the SQL queries before executing them.

## Corrected Version of the Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        partition_sql = self.partition_spec(partition)
        sql_query = 'use {0}; show partitions {1} partition ({2})'.format(database, table, partition_sql)
        stdout = run_hive_cmd(sql_query)

        return bool(stdout)
```

In the corrected version of the `table_exists` function, we properly construct the SQL query by substituting the values of `database`, `table`, and `self.partition_spec(partition)` into the query string before calling the `run_hive_cmd` function. This ensures that the correct SQL query is executed in Hive and reduces the chances of errors occurring.