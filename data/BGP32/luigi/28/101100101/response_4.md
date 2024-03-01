### Bug Explanation
The bug in the `table_exists` function arises from the condition checks in the function. In the first if statement, the function checks if `stdout` is not empty and if `table` is within `stdout`. However, in the failing test cases, the `stdout` value is not being parsed correctly in this condition. 

Additionally, the `run_hive_cmd` function is being called correctly but the comparison logic after getting the output is causing the bug.

### Bug Fix Strategy
To fix the bug, we need to modify the condition check for the first if statement to accurately check if the `table` string is present in the `stdout` string.

### Corrected Version

```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table)).strip()
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition))).strip()
    
            return bool(stdout)
```

By stripping the `stdout` string before returning it, we ensure that any newline characters or extra spaces do not interfere with the conditional checks. This corrected version should pass the failing test cases provided.