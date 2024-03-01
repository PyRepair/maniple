### Bug Explanation:
The bug in the `table_exists` function is related to how the check for table existence is performed. The bug causes the function to incorrectly determine if a table exists or not based on the stdout returned from the `run_hive_cmd` function.

In the buggy implementation:
1. When checking for the existence of a table without partitions, the function checks if the table name is in the stdout, which is incorrect.
2. When checking for the existence of a table with partitions, the function uses the `partition_spec` function to format the partition information before executing the command. This can lead to incorrect formatting and comparison issues.

### Bug Fix Strategy:
To fix the bug in the `table_exists` function, we need to:
1. Ensure that when checking for a table's existence without partitions, we directly compare the stdout to see if the table exists.
2. When checking for a table with partitions, properly format the partition information before executing the command and then check if the stdout contains the specified partition.

### Corrected Version of the `table_exists` function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1}'.format(database, table))

        return stdout and table in stdout
    else:
        partition_query = ", ".join(["{0}='{1}'".format(k, v) for k, v in partition.items()])
        cmd = "use {0}; show partitions {1} partition ({2});".format(database, table, partition_query)
        stdout = run_hive_cmd(cmd)

        if stdout:
            return True
        else:
            return False
```

By making the above changes, the corrected version of the `table_exists` function should now handle table existence checks with and without partitions correctly and pass the failing tests.