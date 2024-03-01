## Bug in the Buggy Function
The bug in the `table_exists` function is related to the condition check for the existence of a table. The function is designed to check if a table exists in a given database using a Hive command. However, the bug arises from how the function handles the output of the Hive command.

When the function is checking for the existence of a table without a partition, it runs a Hive command to show tables like the specified table name. If the table exists, the command's output will contain the table name. The function incorrectly checks for the table name in the output without splitting it into individual table names. This causes a false positive result, leading to incorrect behavior in the tests.

Similarly, when the function is checking for the existence of a table with a partition, it does not handle the output of the Hive command properly. Also, there is a missing space in the Hive command text in this condition.

## Strategy for Fixing the Bug
To fix the bug, we need to ensure that the function correctly processes the output of the Hive command to accurately determine if a table exists. Specifically, when checking for the existence of a table without a partition, the function should split the output by newline characters and then check if the table name is present in the list of tables.

When checking for the existence of a table with a partition, the function should correctly format the Hive command text and process the output in a similar manner to the first case.

## Corrected Version of the Function
Here is the corrected version of the `table_exists` function:

```python
# The relative path of the corrected file: luigi/contrib/hive.py

class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables;'.format(database))
            tables = stdout.split('\n')
            return table in tables
        else:
            stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
            return "OK" in stdout
```

In this corrected version:
- When checking for the existence of a table without a partition, the function splits the output of the `show tables` Hive command by newline characters and then checks if the table name is present in the list of tables.
- When checking for the existence of a table with a partition, the function formats the Hive command correctly and checks for the existence of "OK" in the output.

By implementing these changes, the function should now correctly determine the existence of tables in both cases based on the Hive command outputs, addressing the bug and passing the failing tests.