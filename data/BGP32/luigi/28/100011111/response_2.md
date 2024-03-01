### Fixing the Bug:

#### Problem Identification:
The bug in the `table_exists` function lies in the comparison between the `table` name and the `stdout` result. The `table` name is not being converted to lowercase for case-insensitive comparison, leading to test failures when the case of the `table` name and the `stdout` result do not match.

#### Solution Strategy:
1. Convert the `table` name to lowercase for comparison with the `stdout` result.
2. Update the comparison condition to check if the lowercase `table` name is present in the lowercase `stdout` result.
3. Implement this logic for both cases (when partition is None and when partition is specified).

#### Corrected Version of the Function:
```python
# The corrected version of the function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the `table` name and the `stdout` result to lowercase before comparison, this corrected version of the function ensures case-insensitive matching for table existence checks. This change aligns with the suggested fix mentioned in the GitHub issue for making `table_exists` case-insensitive.