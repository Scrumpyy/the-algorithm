# pylint: disable=no-member, invalid-name
"""
Implementing Writer Layer
"""
from typing import List, Tuple

import libtwml
import tensorflow.compat.v1 as tf

from .layer import Layer


class BatchPredictionTensorWriter(Layer):
    """
    A layer that packages keys and dense tensors into a BatchPredictionResponse.
    Typically used at the out of an exported model for use in a the PredictionEngine
    (that is, in production) when model predictions are dense tensors.

    Args:
        keys: keys to hashmap

    Output:
        output:
            a BatchPredictionResponse serialized using Thrift into a uint8 tensor.
    """

    def __init__(self, keys: List[str], **kwargs):
        super(BatchPredictionTensorWriter, self).__init__(**kwargs)
        self.keys = keys

    def compute_output_shape(
        self, input_shape: Tuple[tf.TensorShape]
    ):  # pylint: disable=unused-argument
        """Computes the output shape of the layer given the input shape.

        Args:
            input_shape: A (possibly nested tuple of) `TensorShape`.  It need not
                be fully defined (e.g. the batch size may be unknown).

        Raise NotImplementedError.
        """
        raise NotImplementedError

    def call(
        self, values: List[tf.Tensor], **kwargs
    ):  # pylint: disable=unused-argument
        """The logic of the layer lives here.

        Args:
            values:
                dense tensors corresponding to keys in hashmap

        Returns:
            The output from the layer
        """
        write_op = libtwml.ops.batch_prediction_tensor_response_writer(
            self.keys, values
        )
        return write_op
