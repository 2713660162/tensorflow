# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Operator overloads for `RaggedTensor`."""

from tensorflow.python.framework import ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops.ragged import ragged_getitem
from tensorflow.python.ops.ragged import ragged_tensor
from tensorflow.python.util import tf_decorator


def _right(operator):
  """Right-handed version of an operator: swap args x and y."""
  return tf_decorator.make_decorator(operator, lambda y, x: operator(x, y))


def ragged_hash(self):
  """The operation invoked by the `RaggedTensor.__hash__` operator."""
  g = getattr(self.row_splits, "graph", None)
  # pylint: disable=protected-access
  if (ops.Tensor._USE_EQUALITY and ops.executing_eagerly_outside_functions() and
      (g is None or g.building_function)):
    raise TypeError("RaggedTensor is unhashable.")
  else:
    return id(self)


def ragged_tensor_equals(self, other):
  """Returns result of elementwise `==` or False if not broadcast-compatible.

  Compares two ragged tensors elemewise for equality if they are
  broadcast-compatible; or returns False if they are not broadcast-compatible.
  Note that this behavior differs from `tf.math.equal`, which raises an
  exception if the two ragged tensors are not broadcast-compatible.

  For example:

  >>> rt1 = tf.ragged.constant([[1, 2], [3]])
  >>> rt1 == rt1
  <tf.RaggedTensor [[True, True], [True]]>

  >>> rt2 = tf.ragged.constant([[1, 2], [4]])
  >>> rt1 == rt2
  <tf.RaggedTensor [[True, True], [False]]>

  >>> rt3 = tf.ragged.constant([[1, 2], [3, 4]])
  >>> # rt1 and rt3 are not broadcast-compatible.
  >>> rt1 == rt3
  False

  >>> # You can also compare a `tf.RaggedTensor` to a `tf.Tensor`.
  >>> t = tf.constant([[1, 2], [3, 4]])
  >>> rt1 == t
  False
  >>> t == rt1
  False
  >>> rt4 = tf.ragged.constant([[1, 2], [3, 4]])
  >>> rt4 == t
  <tf.RaggedTensor [[True, True], [True, True]]>
  >>> t == rt4
  <tf.RaggedTensor [[True, True], [True, True]]>

  Args:
    self: The left-hand side of the `==` operator.
    other: The right-hand side of the `==` operator.

  Returns:
    The ragged tensor result of the elementwise `==` operation, or `False` if
    the arguments are not broadcast-compatible.
  """
  return math_ops.tensor_equals(self, other)


# Indexing
ragged_tensor.RaggedTensor.__getitem__ = ragged_getitem.ragged_tensor_getitem

# Equality
ragged_tensor.RaggedTensor.__eq__ = ragged_tensor_equals
ragged_tensor.RaggedTensor.__ne__ = math_ops.tensor_not_equals
ragged_tensor.RaggedTensor.__hash__ = ragged_hash

# Ordering operators
ragged_tensor.RaggedTensor.__ge__ = math_ops.greater_equal
ragged_tensor.RaggedTensor.__gt__ = math_ops.greater
ragged_tensor.RaggedTensor.__le__ = math_ops.less_equal
ragged_tensor.RaggedTensor.__lt__ = math_ops.less

# Logical operators
ragged_tensor.RaggedTensor.__and__ = math_ops.logical_and
ragged_tensor.RaggedTensor.__rand__ = _right(math_ops.logical_and)
ragged_tensor.RaggedTensor.__invert__ = math_ops.logical_not
ragged_tensor.RaggedTensor.__ror__ = _right(math_ops.logical_or)
ragged_tensor.RaggedTensor.__or__ = math_ops.logical_or
ragged_tensor.RaggedTensor.__xor__ = math_ops.logical_xor
ragged_tensor.RaggedTensor.__rxor__ = _right(math_ops.logical_xor)

# Arithmetic operators
ragged_tensor.RaggedTensor.__abs__ = math_ops.abs
ragged_tensor.RaggedTensor.__add__ = math_ops.add
ragged_tensor.RaggedTensor.__radd__ = _right(math_ops.add)
ragged_tensor.RaggedTensor.__div__ = math_ops.div
ragged_tensor.RaggedTensor.__rdiv__ = _right(math_ops.div)
ragged_tensor.RaggedTensor.__floordiv__ = math_ops.floordiv
ragged_tensor.RaggedTensor.__rfloordiv__ = _right(math_ops.floordiv)
ragged_tensor.RaggedTensor.__mod__ = math_ops.floormod
ragged_tensor.RaggedTensor.__rmod__ = _right(math_ops.floormod)
ragged_tensor.RaggedTensor.__mul__ = math_ops.multiply
ragged_tensor.RaggedTensor.__rmul__ = _right(math_ops.multiply)
ragged_tensor.RaggedTensor.__neg__ = math_ops.negative
ragged_tensor.RaggedTensor.__pow__ = math_ops.pow
ragged_tensor.RaggedTensor.__rpow__ = _right(math_ops.pow)
ragged_tensor.RaggedTensor.__sub__ = math_ops.subtract
ragged_tensor.RaggedTensor.__rsub__ = _right(math_ops.subtract)
ragged_tensor.RaggedTensor.__truediv__ = math_ops.truediv
ragged_tensor.RaggedTensor.__rtruediv__ = _right(math_ops.truediv)


# Dummy methods
def _dummy_bool(_):
  """Dummy method to prevent a RaggedTensor from being used as a Python bool."""
  raise TypeError("RaggedTensor may not be used as a boolean.")


ragged_tensor.RaggedTensor.__bool__ = _dummy_bool
ragged_tensor.RaggedTensor.__nonzero__ = _dummy_bool
