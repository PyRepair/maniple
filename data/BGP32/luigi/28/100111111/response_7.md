To fix the buggy function `table_exists`, we need to make sure that the comparison between the table name and the table names extracted from the `stdout` is case insensitive. This will address the failing test cases where the table names are in different cases than expected.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = [t.lower() for t in stdout.split('\n') if t]
        return table.lower() in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        partitions = [p.lower() for p in stdout.split('\n') if p]
        return table.lower() in partitions
```

Explanation:
- In the corrected version, we first extract the table names from `stdout` (either tables or partitions depending on the case) and convert them to lowercase using a list comprehension.
- Then we compare the lowercase version of the input `table` with the lowercase table names extracted from `stdout` to perform a case-insensitive check.
- This change ensures that the comparison is consistent across different cases of table names.

By updating the function as shown above, the failing test cases should pass successfully, satisfying the expected input/output values and resolving the GitHub issue related to making `table_exists` case insensitive.