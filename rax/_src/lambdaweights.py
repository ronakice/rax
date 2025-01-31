# Copyright 2022 Google LLC.
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

"""Implementations of lambdaweight functions for Rax pairwise losses.

Lambdaweight functions dynamically adjust the weights of a pairwise loss based
on the scores and labels. Rax provides a number of lambdaweight functions as JAX
functions that are implemented according to the
:class:`~rax.types.LambdaweightFn` interface.

Example usage:

>>> scores = jnp.array([1.2, 0.4, 1.9])
>>> labels = jnp.array([1.0, 2.0, 0.0])
>>> loss = rax.pairwise_logistic_loss(
...     scores, labels, lambdaweight_fn=rax.labeldiff_lambdaweight)
>>> print(loss)
1.8923712
"""

import operator
from typing import Optional

import jax.numpy as jnp
from rax._src import utils
from rax._src.types import Array


def labeldiff_lambdaweight(scores: Array,
                           labels: Array,
                           *,
                           where: Optional[Array] = None,
                           weights: Optional[Array] = None) -> Array:
  r"""Absolute label difference lambdaweights.

  Definition:

  .. math::
      \lambda_{ij}(s, y) = |y_i - y_j|

  Args:
    scores: A ``[..., list_size]``-:class:`~jax.numpy.ndarray`, indicating the
      score of each item.
    labels: A ``[..., list_size]``-:class:`~jax.numpy.ndarray`, indicating the
      relevance label for each item.
    where: An optional ``[..., list_size]``-:class:`~jax.numpy.ndarray`,
      indicating which items are valid for computing the lambdaweights. Items
      for which this is False will be ignored when computing the lambdaweights.
    weights: An optional ``[..., list_size]``-:class:`~jax.numpy.ndarray`,
      indicating the weight for each item.

  Returns:
    Absolute label difference lambdaweights.
  """
  del scores, where, weights  # Unused.
  return jnp.abs(utils.compute_pairs(labels, operator.sub))
