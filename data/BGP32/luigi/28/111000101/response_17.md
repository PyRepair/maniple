### Analysis
The buggy function `table_exists` is designed to check if a table exists in a given Hive database. It calls the `run_hive_cmd` function to execute Hive commands and parse the output to determine if the table exists. The bug occurs in constructing the Hive command when checking for table existence with partitions.

### Error Location
The bug is located in the else block of the `table_exists` function where the Hive command is constructed to search for partitions. The issue arises from incorrectly formatting the Hive command string for searching partitions.

### Bug Explanation
The bug in the `table_exists` function occurs when constructing the Hive command to check for table partitions. In the buggy code, the `%s` placeholders are not correctly formatted within the Hive command string. This leads to incorrect Hive command execution and results in unexpected outcomes.

### Bug Fix Strategy
To fix the bug, we need to properly format the Hive command string when checking for table partitions. By correctly interpolating the database, table, and partition spec values into the command string, we can ensure that the Hive command is executed as intended.

### Corrected Code
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        partition_condition = ' and '.join(['{0} = "{1}"'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2});""".format(database, table, partition_condition))

        return bool(stdout)
```

This corrected code properly formats the Hive command string when checking for table partitions. It constructs the partition condition by joining key-value pairs of the partition dictionary and correctly interpolates them into the Hive command.