### Bug Explanation
The bug is likely related to the function not correctly handling the case sensitivity of table names in the output of the `run_hive_cmd` function. The buggy function compares the output from the `run_hive_cmd` function to the table name, potentially leading to false negatives when the table names do not match exactly (e.g., different cases).

### Bug Fix Strategy
To fix the bug, we should modify the buggy function to handle the case sensitivity issue by converting both the table name and the output from `run_hive_cmd` to a common case (e.g., lowercase or uppercase) before comparison.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table.lower() in stdout.lower()
    else:
        partition_str = ", ".join(["{}='{}'".format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, partition_str))
        
        return bool(stdout)
``` 

In the corrected function, we convert both the table name and the output to lowercase using the `lower()` method before comparison to ensure case-insensitive matching. Additionally, we format the partition specification correctly before running the command to show partitions.