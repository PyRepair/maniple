To fix the bug in the `table_exists` function and make it case-insensitive, we need to modify the comparison between the table name and the output from the Hive command. The comparison should convert both strings to lowercase before checking for equality. 

Here is the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2})'.format(database, table, self.partition_spec(partition)))
    
            return bool(stdout)

```

Explanation:
- We modified the comparison in the first `if` block to compare the lowercase versions of `table` and `stdout`.
- In the second `else` block, we simplified the code to directly return whether `stdout` exists or not.

With this modification, the `table_exists` function should now correctly handle case-insensitive comparisons between table names and Hive command outputs, resolving the failing tests related to case sensitivity.