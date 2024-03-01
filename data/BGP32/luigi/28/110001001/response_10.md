### Bug Explanation
The bug in the `table_exists` function arises from the comparison of the `table` name in the stdout response. The comparison is case-sensitive, causing issues when the `table` name provided as input differs in case from the tables listed in the `stdout`. This discrepancy leads to incorrect results and potential failures in determining whether the table exists or not.

### Fix Strategy
To fix this bug, we need to make the comparison case-insensitive. This can be achieved by converting both the `table` input and the tables listed in the `stdout` to lowercase before performing the comparison.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

In the corrected version, both the `table` input and the tables listed in the `stdout` are converted to lowercase using the `lower()` method before the comparison is made, ensuring a case-insensitive check for table existence.