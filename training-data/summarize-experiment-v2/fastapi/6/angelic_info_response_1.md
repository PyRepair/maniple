In this code, there's a bug in the `request_body_to_args` function that needs to be fixed. The function takes in a list of required parameters and a received body, and then processes the body to extract values and errors based on the required parameters.

Based on the expected test cases provided, it seems that the function is not handling the required parameters and received body properly. The expected output shows that the function should construct `values` and `errors` based on the provided `required_params` and `received_body`.

To fix the bug, the function needs to properly process the received body and handle various types of field shapes, such as lists, sets, and tuples. The function should also correctly validate the type of the received value, construct the `values` dictionary, and report any errors in the `errors` list.

The function should be modified to address the issues with the processing of required parameters and received body, and ensure that it returns the expected `values` and `errors` based on the given input parameters.