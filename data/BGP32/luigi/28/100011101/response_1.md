## Bug Explanation
The bug in the `table_exists` function stems from the conditional statements that check the presence of a table in the output of the Hive command. In the case where `partition` is not None, the function constructs the Hive query incorrectly, leading to incorrect results. Additionally, the comparison of the table name with the output in both cases is not accurate.

## Bug Fix Strategy
To fix the bug, we need to ensure that the Hive queries are constructed correctly and that the comparison of the table name with the output is accurate. It involves modifying the way the Hive queries are built and how the presence of the table is verified.

## The corrected version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        return stdout and table in stdout.split()
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
        return stdout.strip() != ""
```

In the corrected version:
1. When `partition` is None, the function runs a query to show all tables in the database and checks if the target table is present in the list.
2. When `partition` is not None, the function correctly constructs the query to show partitions of the table and checks if any partitions are listed.

These fixes ensure that the function correctly determines the existence of a table or its partitions in the Hive database.