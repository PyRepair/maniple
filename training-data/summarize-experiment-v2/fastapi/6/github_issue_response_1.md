GitHub Bug Title:
Support repeated key=value in form data

Description:
When using URL encoded data with repeated keys, only the last key=value pair is being considered. This does not work as expected when defining a variable as a list. The request.form() method should collect repeated keys and assign their values as a list to the same key before validation happens.

Expected Output:
FastAPI should collect repeated keys in the 2-tuple list that request.form() gives and assign those values as a list to the same key before validation happens.

Environment:
- Python: 3.7.3.final.0