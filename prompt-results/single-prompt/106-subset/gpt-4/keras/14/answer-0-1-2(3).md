The problem arises because in `tf.keras.metrics.sparse_top_k_categorical_accuracy` and `tf.keras.metrics.sparse_categorical_accuracy`, y_true (true labels) is assumed to have the shape (num_samples, 1). However, it can also have the shape (num_samples,), and this leads to incorrect results. 

To correct this, the shape of y_true should be checked and squeezed if required. This operation should be performed both in `sparse_top_k_categorical_accuracy` and `sparse_categorical_accuracy`.

Here is the corrected source code:

```python
def sparse_top_k_categorical_accuracy(y_true, y_pred, k=5):
    if len(y_true.shape) == 2:
      y_true = K.squeeze(y_true, axis=-1)

    return K.mean(K.in_top_k(y_pred, K.cast(y_true, 'int32'), k),
                  axis=-1)


def sparse_categorical_accuracy(y_true, y_pred):
    if len(y_true.shape) == 2:
        y_true = K.squeeze(y_true, axis=-1)

    return K.cast(K.equal(K.cast(y_true, K.floatx()),
                          K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
                  K.floatx())
```

The `K.squeeze` operation is used to squeeze out unnecessary dimensions (if exist) of `y_true`. Then `K.mean` and `K.cast` calls become correct as they expect `y_true` to have the shape (num_samples,).