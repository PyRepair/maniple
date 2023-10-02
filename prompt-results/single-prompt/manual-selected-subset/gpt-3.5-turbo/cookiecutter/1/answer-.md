The exact nature of the bug was not mentioned which makes it challenging to provide a specific fix. However, assuming the bug might be the misapplication of overwrite context, where the values were being set in the imported JSON object 'obj' instead of the context dictionary which is what's actually returned from the function.

Here is a minimal change (only two lines!) to fix the code:

```python
def generate_context(
    context_file='cookiecutter.json', default_context=None, extra_context=None
):
    """
    Generate the context for a Cookiecutter project template.
    
    Loads the JSON file as a Python object, with key being the JSON filename.
    
    :param context_file: JSON file containing key/value pairs for populating
    the cookiecutter's variables.
    :param default_context: Dictionary containing config to take into account.
    :param extra_context: Dictionary containing configuration overrides
    """
    context = OrderedDict([])

    try:
        with open(context_file) as file_handle:
            obj = json.load(file_handle, object_pairs_hook=OrderedDict)
    except ValueError as e:
        full_fpath = os.path.abspath(context_file)
        json_exc_message = str(e)
        our_exc_message = (
            'JSON decoding error while loading "{0}".  Decoding'
            ' error details: "{1}"'.format(full_fpath, json_exc_message)
        )
        raise ContextDecodingException(our_exc_message)

    file_name = os.path.split(context_file)[1]
    file_stem = file_name.split('.')[0]
    context[file_stem] = obj

    if default_context:
        apply_overwrites_to_context(context[file_stem], default_context)
    if extra_context:
        apply_overwrites_to_context(context[file_stem], extra_context)

    logger.debug('Context generated is %s', context)
    return context
```

The changes in lines when comparing to your original function are exactly here:

```python
apply_overwrites_to_context(context[file_stem], default_context)
apply_overwrites_to_context(context[file_stem], extra_context)
```

The context for the filename taken from the context file is correctly targeted for the apply_overwrites_to_context.