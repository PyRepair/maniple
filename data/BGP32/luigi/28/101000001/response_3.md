## Analysis:
The buggy function `table_exists` is used to check if a table exists in a Hive database. It receives parameters like `table`, `database`, and `partition`. The issue seems to be with the way the SQL queries are constructed and executed using the `run_hive_cmd` function. The condition for checking the existence of a table is not properly handled, leading to incorrect results.

## Identified Issue:
The bug lies in the construction of the SQL queries in the `table_exists` function. The formatting of the query string in the `else` block is incorrect, leading to potential syntax errors or incorrect queries being executed.

## Cause of the Bug:
The buggy condition is:

```python
stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
```

The issue here is the syntax of the `show partitions` command. It should not have "partition" in the query. Additionally, the usage of `%s` for string formatting is not optimal in this context.

## Strategy for Fixing the Bug:
1. Fix the formatting of the SQL query in the `else` block to follow the correct syntax for the `show partitions` command.
2. Utilize the `format` method for string formatting instead of `%` formatting for cleaner and safer code.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1}".format(database, table))
        
        return True if stdout else False
```

In the corrected version:
1. The SQL query syntax in the `else` block is fixed to ensure proper execution.
2. String formatting is done using the `format` method for more readability and safety.
3. The return statement is simplified for better clarity.

By making these adjustments, the functionality of the `table_exists` function should be improved and the bug addressed.