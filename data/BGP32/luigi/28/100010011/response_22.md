3. Explanation of the bug:
The bug exists in the `table_exists` function where it checks for the existence of a table in a case-sensitive manner. The problem arises when the table names are defined with different letter cases (e.g., "mytable" vs. "MyTable"), causing the test to fail due to case sensitivity.

4. Strategy for fixing the bug:
To fix the bug and make the `table_exists` function case insensitive, we need to ensure that the comparison between the table name and the output from Hive is done in a case-insensitive manner. This can be achieved by converting both the table name and the output to lowercase before comparison.

5. Corrected version of the `table_exists` function:

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

By converting both the table name and stdout to lowercase during comparison, the corrected function ensures that the test is case insensitive, addressing the issue reported on GitHub.