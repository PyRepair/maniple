### Analysis:
1. The `table_exists` function within the `HiveCommandClient` class is checking for the existence of a table in a database, either with or without a partition.
2. The function uses the `run_hive_cmd` function to execute Hive commands and check the output to determine if the table exists.
3. The bug seems to be related to how the function checks the returned output from `run_hive_cmd` and determines the table existence.
4. The bug may be due to the inconsistent handling of the output from `run_hive_cmd`.

### Bug Cause:
The bug in the `table_exists` function arises from how the function checks the output of the `run_hive_cmd` function. When checking for the existence of a table without a partition, the function checks if the table name is in the output. However, for tables with partitions, the function only checks if the output is not empty, leading to inconsistencies.

### Bug Fix:
To fix the bug, we need to ensure that the function consistently checks the output from `run_hive_cmd` for both cases (with and without partitions) and properly determines the existence of the table.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show tables like "{1}{2}";""".format(database, table, self.partition_spec(partition)))
        return stdout and table in stdout
```

The corrected version consistently checks if the table name exists in the output from `run_hive_cmd` for both cases, with and without partitions. This should fix the inconsistent behavior and address the bug.