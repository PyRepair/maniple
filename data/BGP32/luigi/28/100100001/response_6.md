## Analysis:
The buggy function `table_exists` in `luigi/contrib/hive.py` is expected to determine if a given table exists in the specified database and optionally with a specified partition. The bug seems to be related to how the function processes the output from the `run_hive_cmd` function.

## Error Identification:
The bug is likely in the condition checking logic using `stdout` and how the function handles the partition argument.

## Bug Explanation:
The bug occurs because the function incorrectly checks for the existence of the table based on the output from `run_hive_cmd`. The function expects the table name to be present in stdout for validating the existence of the table. However, in some cases, the table name might be present in a newline-separated format, which causes the function to incorrectly determine if the table exists.

## Bug Fix Strategy:
1. Modify the condition checking to handle both cases where the table name is directly present in stdout or is in a newline separated format.
2. Ensure that the function correctly processes the partition argument if provided.

## Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and (table in stdout or table in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By updating the condition checking logic to consider both cases where the table name might be directly present or in a newline-separated format, the corrected function should pass the failing test cases.