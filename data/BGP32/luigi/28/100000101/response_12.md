The buggy function has issues in constructing the Hive queries correctly and processing the output. The bug is particularly related to how the queries are formed and how the output is checked.

The faulty logic in the function:
1. In the first case, the buggy function only checks if the table exists based on the presence of the table name in the output. It does not consider the actual content of the output. This can lead to incorrect results.
2. In the second case, the function uses a similar flawed logic as in the first case, leading to potential inaccuracies.
3. The function also has issues with constructing the query in the else part where partitions are involved. There are formatting errors in the query that may result in incorrect output checking.

To fix the bug, the function needs to be corrected in terms of constructing the queries and properly handling the output checking logic.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
        return stdout != ""
```

This corrected version should now correctly check for the existence of the table and its partitions in the Hive database. It splits the output by newline characters to accurately check for the table presence in the stdout. Additionally, the partition checking logic has been fixed to properly construct the queries and handle the output check.