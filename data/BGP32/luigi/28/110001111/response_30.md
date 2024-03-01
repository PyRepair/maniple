### Bug Explanation
The bug in the `table_exists` function stems from the fact that the comparison between the `table` name and the output `stdout` is case-sensitive. This causes issues when the table names are provided in different cases (capitalized, lower case) as Hive is case-insensitive, leading to test failures. The suggestion in the GitHub issue is to make the comparison case-insensitive by converting both strings to lowercase before the comparison.

### Strategy for Fixing the Bug
To fix the bug and address the GitHub issue, we need to update the function to convert both the `table` name and the `stdout` output to lowercase before comparing them.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):
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

In the corrected version, both the `table` and the `stdout` are converted to lowercase before the comparison, making the function case-insensitive and resolving the bug reported in the GitHub issue.