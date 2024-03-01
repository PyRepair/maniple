### Analysis:
The buggy function `table_exists` checks if a table exists in a given database with optional partition information. It calls the `run_hive_cmd` function to execute a hive command and check the output to determine if the table exists.

The bug lies in the logic of checking the stdout for table existence. In the first case, the function checks if the table name is in the stdout directly, while in the second case, it checks for the table name preceded by 'OK\n'. This inconsistency can lead to incorrect results.

### Bug:
The bug occurs due to inconsistent checking of the stdout to determine table existence. The function is not handling the stdout consistently for different cases, leading to incorrect results.

### Fix:
To fix the bug, we need to check the presence of the table name in the stdout consistently. We should update the logic to handle both cases by splitting the stdout appropriately and checking for the table name within the split.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout and table in stdout.split('\n')
``` 

This corrected version of the function splits the stdout by '\n' and checks if the table name is present in the split result. This ensures consistent handling of stdout for all cases and fixes the bug.