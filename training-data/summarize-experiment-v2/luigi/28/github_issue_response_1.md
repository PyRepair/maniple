GitHub Bug Title:
Hive table_exists should be case insensitive?

Description:
The table_exists function should be case insensitive when checking if a table exists in a hive database. The current implementation does not handle this and can cause tests to fail if the table names are defined as capitalized. This issue arises because hive is case insensitive and will return table names as lower case, causing the tests to fail. A fix is proposed to check the stdout against the table name in lower case to avoid case issues.

Expected Output:
The table_exists function should check for the existence of a table in a hive database in a case-insensitive manner.

Environment:
- luigi: 2.8.12
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0