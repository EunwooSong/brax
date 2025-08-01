# Copyright 2025 The Brax Authors.
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

"""Tests the gym wrapper."""

from absl.testing import absltest
from brax import envs
from brax.envs.wrappers import gym
from brax.envs.wrappers import training
import numpy as np


class GymTest(absltest.TestCase):

  def test_action_space(self):
    """Tests the action space of the GymWrapper."""
    base_env = envs.create('pusher')
    env = gym.GymWrapper(base_env)
    np.testing.assert_array_equal(
        env.action_space.low, base_env.sys.actuator.ctrl_range[:, 0]
    )
    np.testing.assert_array_equal(
        env.action_space.high, base_env.sys.actuator.ctrl_range[:, 1]
    )


  def test_vector_action_space(self):
    """Tests the action space of the VectorGymWrapper."""
    base_env = envs.create('pusher')
    env = gym.VectorGymWrapper(training.VmapWrapper(base_env, batch_size=256))
    np.testing.assert_array_equal(
        env.action_space.low,
        np.tile(base_env.sys.actuator.ctrl_range[:, 0], [256, 1]),
    )
    np.testing.assert_array_equal(
        env.action_space.high,
        np.tile(base_env.sys.actuator.ctrl_range[:, 1], [256, 1]),
    )


if __name__ == '__main__':
  absltest.main()
