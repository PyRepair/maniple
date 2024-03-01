### Bug Explanation
The bug in the `table_exists` function is due to the way it checks for the existence of a table in a Hive database. When the function receives the table name as input, it uses the `run_hive_cmd` function to execute a Hive command and then checks if the table name is present in the output. However, the current implementation fails to handle cases where the table name appears as part of another word or string in the output.

For example, in Case 2, when the table name is "MyTable", the function looks for an exact match in the output. If the output includes the word "mytable" as part of a sentence along with other characters or words, the function incorrectly determines that the table exists even though it does not match the complete table name.

### Fix Strategy
To fix this issue, a more robust approach is needed to accurately check for the existence of the table. One way to achieve this is to split the output into lines and then check each line individually to see if it matches the expected table name. This way, we can avoid false positives when the table name appears as part of another word.

### Corrected Version
Here's the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default'):
    stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

    # Check each line of the output for an exact match with the table name
    if stdout:
        return any(t.strip() == table for t in stdout.split('\n'))
    
    return False
```

By splitting the output into lines and then checking for an exact match with the table name, we can accurately determine if the table exists in the Hive database. This corrected version should pass the failing tests and provide the expected behavior for checking table existence.