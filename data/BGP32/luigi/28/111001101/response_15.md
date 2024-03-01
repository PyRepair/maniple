### Bug Explanation
The bug in the `table_exists` function lies in the condition checking for the existence of the table. When the `partition` parameter is provided, the function constructs a Hive query incorrectly by passing the partition spec as a single string without proper formatting. This results in the Hive query not being able to find the table, leading to incorrect output.

### Bug Fix Strategy
To fix the bug, we need to ensure that the Hive query is constructed correctly when the `partition` parameter is provided. We need to correctly format the partition specification in the Hive query to match the structure expected by the Hive CLI.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_spec_string = ','.join([f"{k}='{v}'" for k, v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_spec_string))
        return bool(stdout)
``` 

In the corrected version, we properly format the partition specification in the Hive query by converting the partition dictionary into a string with key-value pairs separated by commas and surrounded by quotes. This ensures the Hive query is constructed correctly to check for the existence of the table with the specific partition.