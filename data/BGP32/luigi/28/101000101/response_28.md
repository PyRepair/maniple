### Analysis
The buggy function `table_exists` is designed to check if a table exists in a Hive database. It takes in parameters `table`, `database`, and optionally `partition`. If `partition` is provided, it constructs a Hive command to show partitions based on the `partition_spec` function. The bug lies in how the Hive commands are constructed and checked for existence.

### Bug Explanation
1. In the case where `partition` is None, the buggy function constructs a Hive command using `run_hive_cmd` to check if the table exists. However, the command's format is incorrect for the `show tables` operation, which will lead to incorrect results.

2. In the case where `partition` is provided, the buggy function constructs a Hive command to show partitions based on the `partition_spec` function. The statement constructing the Hive command is missing the correct formatting, leading to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to correct the construction of Hive commands in both cases in the function `table_exists`. The Hive commands should be properly formatted to check for the existence of the table and partitions. We should ensure that the commands are correctly constructed using the provided parameters.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2})'.format(database, table, self.partition_spec(partition)))

        return table in stdout
```

By correcting the format of the Hive commands in both cases and ensuring the parameters are correctly substituted, the function should now correctly check for the existence of tables and partitions in the Hive database.