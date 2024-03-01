### Analysis:
1. The `table_exists` function in the `luigi/contrib/hive.py` file is supposed to check if a table exists in a given database in Hive.
2. The function checks for the existence of a table by running a Hive command and checking the output.
3. The bug seems to be related to how the function handles the check for the existence of a table with partitions.
4. The current implementation of the function may not correctly handle the case where partitions are specified.

### Bug Cause:
- The bug is likely caused by how the function constructs the Hive command for checking table existence with partitions.
- In the `else` block of the function, the `run_hive_cmd` call for checking table existence with partitions may not be handling the partition specification correctly.

### Bug Fix Strategy:
- Ensure that the Hive command for checking table existence with partitions is correctly constructed and executed.
- Modify the way the partition specification is included in the Hive command to ensure it is properly formatted.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_str = " ".join(["{0}='{1}'".format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, partition_str))
        return stdout and table in stdout
```

### Updated Test Function:
- The test function provided does not need to be changed since the functionality remains the same.