### Analysis:
The buggy function `table_exists` in the `HiveCommandClient` class is supposed to check if a table exists in a given database. The issue seems to be with the way the function is checking the existence of the table based on the output of the `run_hive_cmd` function.

### Bugs:
1. In the first branch of the `if` statement, the function checks if the `table` is in the `stdout`. However, since the `stdout` contains the string `'OK'`, this condition will always return `False`.
2. In the second branch of the `if` statement, the function constructs a command for showing partitions, but the logic to check the existence based on the response is flawed.

### Cause of the Bug:
1. The bug causes the function to incorrectly determine if the table exists based on the output of the `run_hive_cmd` function. This is due to the incorrect handling of the `stdout` response from the command.
2. The function doesn't correctly parse the output of the show partitions command, leading to incorrect determination of table existence.

### Strategy for Fixing the Bug:
1. Update the function logic to correctly interpret the `stdout` response from the table show command.
2. Ensure that the function correctly handles the response from the show partitions command and properly determines if the table exists based on the response.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
        return 'OK' in stdout.splitlines()
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1}'.format(database, table))
        partition_str = self.partition_spec(partition)
        return partition_str in stdout
```

By making the above corrections, the function should now correctly determine if a table exists in the specified database and handle partitions appropriately.