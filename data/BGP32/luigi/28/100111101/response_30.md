### Issues and Explanation
1. The buggy function fails to correctly handle the `partition` parameter, leading to incorrect logic and erroneous returns.
2. The function does not properly check for the presence of the table name in the output from the Hive commands, leading to incorrect responses.
3. The buggy function fails to properly handle case sensitivity, causing assertions to fail when comparing table names.
4. The function does not account for potential empty string outputs from the Hive commands.

### Fix Strategy
1. Modify the function to appropriately handle the `partition` parameter and correctly format the Hive command.
2. Ensure that the function correctly parses the output of the Hive commands to determine table existence.
3. Implement case-insensitive table name comparison to meet the test requirements.
4. Check for empty string outputs from the Hive commands and handle them accordingly.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

In the corrected version, the function now properly handles both cases with or without partitions. It effectively checks for table existence in the Hive output in a case-insensitive manner. Additionally, it correctly accounts for empty string outputs. This updated version should pass the failing tests and satisfy the expected input/output values.