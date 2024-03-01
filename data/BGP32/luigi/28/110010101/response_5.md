### Analysis
1. The buggy function `table_exists` checks if a table exists in the database using Hive commands.
2. The function utilizes the `run_hive_cmd` function to execute Hive commands and check the output.
3. The bug is likely related to how the function processes the output of the `run_hive_cmd` function.
4. Based on the failing test cases, the bug causes incorrect evaluation of the existence of tables.
5. We need to ensure that the function correctly interprets the output of Hive commands to determine table existence.

### Bug Explanation
- In the buggy function, when checking for table existence, the function logic is reversed. 
- In the case where `stdout` is not empty (indicating that the table exists), the function returns `True`. However, it should be returning `False`.
- Likewise, when `stdout` contains the table name, the function should return `True`, but wrongly returns `False`.

### Bug Fix Strategy
1. Reverse the return values in the if-else conditions to ensure correct evaluation of table existence.
2. Modify the function's logic to return `True` only if the table is found in the `stdout`.

### Corrected Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return table in stdout if stdout else False
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
            return True if stdout else False
```