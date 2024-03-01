### Bug Explanation:
The bug in the `table_exists` function lies in the conditional checks when determining if a table exists in the specified database. In the first part of the function, when `partition` is `None`, the function checks if the table exists by looking for the table name in the output of the `SHOW TABLES` command in Hive. However, the comparison `table in stdout` is incorrect because when the `SHOW TABLES` command is executed, it outputs all table names separated by newlines (`\n`). 

In the failing test cases, the `OK` response from the `run_hive_cmd` function is misleading as it does not represent the actual output of the `SHOW TABLES` command.

In the second part of the function, when a partition is specified, the function queries partitions for a table in Hive with the specified partition key-value pair. Similar to the first part, the success or failure of the query is not accurately reflected.

The code lacks proper handling of Hive command responses and does not correctly parse and interpret the results to determine table existence.

### Bug Fix Strategy:
To fix the bug, the function needs to properly capture and process the output of the Hive commands to accurately determine whether a table exists in the specified database. This involves handling newline-separated output from `SHOW TABLES` and ensuring that the specified partition is correctly queried.

### Corrected Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
        tables = stdout.split("\n")
        
        return table in tables
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
        
        return stdout != "Partition not found."
```

In this corrected version:
1. The `SHOW TABLES` query output is split by newline and stored in a list to accurately check if the table name is in the list of tables.
2. The output of the partition query is checked to ensure that the specified partition exists for the table.

This corrected version should address the issues present in the original buggy function and pass the failing test cases.