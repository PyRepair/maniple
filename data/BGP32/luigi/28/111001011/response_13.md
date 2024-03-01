### Analysis:
1. The `table_exists` function is responsible for checking if a table exists in a specific database in Hive.
2. The bug arises from the fact that the function compares the table name in a case-sensitive manner with the output of the Hive command, causing test failures when the case mismatches.
3. The issue reported on GitHub highlights the need to make the `table_exists` function case insensitive to handle tables with different cases.
4. The proposed fix suggests converting the table name to lowercase before comparison with the Hive output.
5. By implementing a case-insensitive comparison, we can address the test failures and align with the feature request on GitHub.

### Bug Fix Strategy:
1. Modify the `table_exists` function to convert the table name to lowercase before comparing with the Hive command output.
2. Adjust the comparison logic to check if the lowercase table name exists in the lowercase Hive command output.
3. Return `True` if the table exists and `False` if it does not.

### Corrected Version of the `table_exists` function:
```python
def table_exists(self, table, database='default', partition=None):
    table_lower = table.lower()
    
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table_lower))
        return stdout and table_lower in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table_lower, self.partition_spec(partition)))
        return bool(stdout)
```

In the corrected version of the function, we convert the `table` parameter to lowercase (`table_lower`) and perform a case-insensitive comparison with the output of the Hive command. This modification addresses the reported bug and aligns with the suggested fix on GitHub.