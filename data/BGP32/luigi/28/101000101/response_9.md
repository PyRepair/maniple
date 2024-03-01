### Analyzing the buggy function

The buggy function `table_exists` is supposed to check if a table exists in a given database based on the input parameters such as `table`, `database`, and potential `partition`. If a partition is provided, it also utilizes the `partition_spec` function to construct the correct partition clause. However, the bug seems to be related to the formatting of the command strings passed to `run_hive_cmd`.

### Identifying potential error locations

1. The string formatting in the `stdout = run_hive_cmd` lines might be incorrect, leading to issues with executing the Hive commands.
2. The condition for checking `return stdout and table in stdout` may not accurately determine if the table exists in the database.
3. The usage of `partition_spec` function in the second part of the function might not be correctly formatted, potentially leading to errors.
4. The condition `if stdout:` may not accurately determine if the table exists due to potential variations in the output from Hive commands.

### Cause of the bug

The bug arises from incorrect string formatting in constructing Hive commands using the `run_hive_cmd` function. Additionally, the condition checks and the usage of `partition_spec` function might not align with the expected output from Hive commands, leading to incorrect results.

### Strategy for fixing the bug

1. Ensure correct string formatting for constructing Hive commands based on input parameters.
2. Improve the condition checks to accurately determine if the table exists in the database.
3. Verify the usage of `partition_spec` function to construct the partition clause properly.

### Corrected version of the function

```python
# Corrected version of the function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_clause = ', '.join(['{0}="{1}"'.format(k, v) for k, v in partition.items()])
        query = 'use {0}; show partitions {1} partition ({2});'.format(database, table, partition_clause)
        stdout = run_hive_cmd(query)
        return stdout != ''
```

This corrected version addresses the string formatting issues for constructing Hive commands with proper clause formation when dealing with partitions. Additionally, it improves the condition check for accurately determining if the table exists in the given database.