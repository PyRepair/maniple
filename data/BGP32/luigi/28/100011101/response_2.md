### Bug Explanation
The bug in the `table_exists` function is related to how the function checks for the presence of a table in a Hive database. In the current implementation, the function checks if the response string from the Hive command contains the table name, which can lead to false positives or negatives if the table name is a substring of another table name. The function does not accurately parse the output to determine if the exact table exists.

### Bug Location
The bug is located in the `if stdout:` block where the function checks if the `stdout` string is not empty. Instead of accurately verifying the existence of the table, the function merely checks for the presence of any output in this block.

### Fix Strategy
To fix the bug, we need to enhance the function to accurately determine if the table exists in the database. This can be achieved by parsing the `stdout` string to extract the exact table names and then checking if the specified table is among those extracted. This will provide a more reliable check for table existence.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    command = 'use {0}; show tables like "{1}";'.format(database, table)
    stdout = run_hive_cmd(command)

    tables = [t.strip() for t in stdout.split('\n') if t.strip()]
    return table in tables
``` 

In the corrected function:
1. We split the `stdout` by newline characters and remove empty strings to extract individual table names.
2. Then we check if the specified `table` is in the extracted table names list to accurately determine table existence.

This corrected implementation ensures a more precise check for table existence in the Hive database.