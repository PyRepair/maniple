### Bug Explanation

The bug in the `table_exists` function arises from a case-sensitivity issue when comparing the `table` name with the output from the `run_hive_cmd` function. Hive is case-insensitive, so the comparison needs to be case-insensitive as well, otherwise, tests fail when checking for tables with different case variations.

In the failing test, when checking for the existence of the table 'MyTable' in a case-insensitive environment, the function fails to correctly handle the comparison and returns False instead of True, leading to an assertion error.

### Bug Fix Strategy

To address this bug, the comparison between the `table` name and the `stdout` output should be made case-insensitive by converting both strings to lowercase before the comparison. This adjustment will ensure that the function behaves correctly in a case-insensitive context and passes the failing tests.

### Corrected Code

Here is the corrected version of the `table_exists` function:

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

By converting both the `table` variable and the `stdout` output to lowercase during the comparison, the function will now handle case-insensitive checks correctly. This fix ensures that the function behaves as expected, passing the failing tests and resolving the reported GitHub issue regarding case sensitivity.