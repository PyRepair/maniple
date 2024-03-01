### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class of `luigi/contrib/hive.py` is supposed to check if a table exists in a given database.
2. The bug involves failing to account for case sensitivity when checking table names in the `stdout` returned by `run_hive_cmd`.
3. The failing test cases indicate that the function fails when dealing with table names that have varying cases.
4. To fix the bug, we need to ensure that the comparison between the table name and the `stdout` is case insensitive.
5. The proposed solution is to convert both the table name and the `stdout` to lowercase before comparing them.

### Solution:
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

By converting both the table name and the `stdout` to lowercase before comparison, the `table_exists` function now becomes case insensitive, addressing the bug described in the GitHub issue.