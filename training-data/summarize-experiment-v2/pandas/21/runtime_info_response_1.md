The `_get_with` function is intended to handle different types of keys for indexing a Series. It includes logic to handle slices, DataFrames, tuples, non-list-like scalars, lists, and various other scenarios.

However, it seems that the logic for determining the type of the key (`key_type`) is not working correctly. In all the provided cases, the `key_type` ends up being `'string'`, which is not the expected behavior.

This can be a result of incorrect handling of different key types, where the function consistently infers the key type as a string, even when the input is of a different type.

To fix this issue, the logic for determining the `key_type` needs to be carefully reviewed and potentially updated to correctly identify the type of the input key. This could involve checking the type of the key using appropriate methods for different input types such as lists, ndarrays, DataFrames, etc., and then setting the `key_type` accordingly. Additionally, it may be necessary to handle Index objects differently in order to correctly infer the type of the key.