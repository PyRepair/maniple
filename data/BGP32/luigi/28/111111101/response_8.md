### Bug Explanation
The bug lies in the comparison logic where the function checks if the `table` exists in the output of the Hive command. In the first case, the bug occurs because when the stdout is 'OK', the function returns True instead of False. This inconsistency leads to the failing test. Similarly, in the second case, the function incorrectly returns True when the table should not exist in the given output.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly checks if the given table exists in the stdout from the Hive command. We can modify the logic to properly analyze the stdout and return the correct boolean value based on the presence or absence of the table in the output.

### Corrected Version of the Buggy Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_str = self.partition_spec(partition)
        stdout = run_hive_cmd("use {}; show partitions {} partition ({})".format(database, table, partition_str))
        return bool(stdout)
``` 

By modifying the table_exists function to check the existence of the table in the stdout correctly, we address the bug and ensure that the function returns the expected boolean values. This corrected version should pass the failing tests and provide the desired output.