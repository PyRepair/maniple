### Bug Analysis
The buggy function `table_exists` has two branches: one where `partition` is None and another where `partition` is not None. 
- In the first branch, it runs a hive command to check if a table exists.
- In the second branch, it runs a hive command to check if a specific partition of a table exists.

However, the bug lies in how the `run_hive_cmd` function is being called, specifically with the second query in the `else` branch. The formatting of the query is incorrect, causing it to fail.

### Bug Explanation
In the else branch of the `table_exists` function, the `run_hive_cmd` function is called with a Hive query that is not correctly formatted. The issue is in the query string, which contains an error in its format specifiers and placeholders. This error causes the query execution to fail and does not correctly determine if the partition exists.

### Bug Fix Strategy
To fix the bug, the query string in the else branch needs to be correctly formatted for the Hive command to check if a specific partition exists. The placeholders `%s` need to align correctly with the variables being passed to the query.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

With this corrected version, the Hive commands for checking table and partition existence are properly formatted, which should now accurately determine if the table/partition exists in the given database.