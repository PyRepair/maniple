### Bug Explanation
The bug in the provided function `table_exists` lies in how the function checks for the existence of the table in the database. In both cases where the function checks for the existence of the table with or without partitions, the logic to parse the output of the `run_hive_cmd` function is incorrect.

In the first case, where no partition is specified, the function checks if the table name is present in the stdout output returned by the `run_hive_cmd` function. The bug here is that the function checks for an exact match of the table name in the entire stdout output, which is incorrect.

In the second case, when a partition is specified, the function constructs a command to show partitions for the given table and partition. Again, the bug lies in the parsing of the stdout output returned by `run_hive_cmd`. The function expects a simple boolean value to indicate the existence of the table, which leads to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to modify the parsing logic for the stdout output of the `run_hive_cmd` function. The function should correctly handle the output to determine if the table exists in the database.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower().split()
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd("use {0}; show partitions {1} ({2});".format(database, table, partition_spec))
        return bool(stdout)
```

In the corrected version:
1. When checking for the existence of a table without a partition, we split the stdout by line and check if the lowercase table name is present in any of the lines.
2. When checking for the existence of a table with a partition, we construct the command correctly and return a boolean value based on the presence of any output.

This corrected version should now handle the table existence checks accurately based on the given input parameters and produced stdout output.