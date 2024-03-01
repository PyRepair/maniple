### Analysis:
- The `table_exists` function in the `HiveCommandClient` class is responsible for checking if a given table exists in the specified database with an optional partition.
- The function uses the `run_hive_cmd` function to execute Hive commands.
- The error messages indicate that the test case is not passing as expected.
- The issue seems to be related to the condition checking and parsing the output of the `run_hive_cmd`.
- The first test case fails because it expects `True` but receives `False`.
- The second test case fails for the same reason.

### Potential Error Locations:
1. The condition checking logic in the `table_exists` function might not correctly evaluate the output of `run_hive_cmd`.
2. The formatting of the command strings passed to `run_hive_cmd` might be incorrect.

### Cause of the Bug:
1. The condition `return stdout and table in stdout` is using a logical AND operation, which might not work as intended if the output of `run_hive_cmd` is not properly handled.
2. The formatting of the Hive command passed to `run_hive_cmd` in the else part might be causing issues in retrieving the correct output.

### Strategy for Fixing the Bug:
1. Ensure that the output of `run_hive_cmd` is properly handled and parsed to check for the existence of the table.
2. Verify the formatting of the Hive commands constructed in both parts of the conditional statement.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout.strip() == "OK"
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
    
        return stdout.strip() == "OK"
```

In the corrected version, we have:
- Used the string method `strip()` to remove any leading or trailing whitespaces from the output before comparison.
- Fixed the formatting of the Hive commands to ensure the correct execution.

By making these adjustments, the corrected version of the `table_exists` function should now pass the failing tests.