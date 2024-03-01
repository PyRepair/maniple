## Analysis:
1. The function `table_exists` is supposed to check if a table exists in a specified Hive database.
2. The function takes parameters `table`, `database`, and `partition`.
3. The function conditionally runs a Hive command based on the presence of a partition.
4. The function returns `True` if the table exists and `False` if it does not.

## Identified Issue:
The bug lies in the way the Hive commands are constructed and executed within the function.
1. In the conditional branch where a partition exists, the Hive command appears to be incorrectly formatted.
2. The `run_hive_cmd` function, which is responsible for executing Hive commands, is called within the function but not provided in the snippet.
3. The current logic for checking table existence based on the command output is not robust.

## Bug Cause:
1. The Hive command in the `else` branch is incorrectly formatted, causing it to not function as intended.
2. Without the definition and implementation of the `run_hive_cmd` function, the actual execution of the Hive commands is missing.

## Strategy for Fixing the Bug:
1. Correct the formatting of the Hive command in the `else` branch to properly check for partitions.
2. Implement a function `run_hive_cmd` that can run the provided Hive command and return the output for checking table existence.

## Corrected Version:
```python
# The corrected version of the function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout.strip() == table
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
        return len(stdout.strip()) > 0
```

In the corrected version:
- The Hive commands are properly formatted and should work as intended.
- The `run_hive_cmd` function should be implemented outside of this function to execute the Hive commands.
- The return values are modified to improve the logic for checking table existence based on the command output.
  
Remember to define and implement the `run_hive_cmd` function appropriately for the function to work correctly.