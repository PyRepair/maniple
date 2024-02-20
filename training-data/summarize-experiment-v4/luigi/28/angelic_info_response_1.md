Case 1: Given the input parameters `database='default'` and `table='mytable'`, the function should return `stdout='OK'`, indicating that the table exists in the specified database.

Case 2: Given the input parameters `database='default'` and `table='MyTable'`, the function should return `stdout='OK\nmytable'`, also indicating that the table exists in the specified database.

Case 3: Given the input parameters `database='default'` and `table='mytable'`, the function should return `stdout='OK'`, indicating that the table exists in the specified database.

Case 4: Given the input parameters `database='default'` and `table='MyTable'`, the function should return `stdout='OK\nmytable'`, indicating that the table exists in the specified database.

In summary, the function should return the expected output values for the given input parameters, indicating whether the specified table exists in the specified database.