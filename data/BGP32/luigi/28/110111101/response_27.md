### Bug Explanation
The bug in the `table_exists` function lies in the logic that checks whether the specified table exists in the output of the Hive command. The issue arises from the comparison logic used after running the command. The function checks if the table name is present in the entire output string, leading to incorrect results in certain scenarios.

In the failing test cases, the bug causes incorrect evaluations when checking for table existence, leading to failed assertions where the expected value does not match the actual value.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to check for the table name in each line of the output separately, rather than searching for the table name in the entire output string. This change will ensure that the function accurately determines the existence of the specified table.

### Updated Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return any(table in line for line in stdout.splitlines())
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

By updating the `table_exists` function as shown above, the function will correctly identify the existence of the specified table in the Hive command output, addressing the bug and ensuring the passing of the failing tests.