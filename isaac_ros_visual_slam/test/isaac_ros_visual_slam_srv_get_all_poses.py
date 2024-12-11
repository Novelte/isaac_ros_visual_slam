# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import os
import pathlib
import sys

from isaac_ros_test import IsaacROSBaseTest
from isaac_ros_visual_slam_interfaces.srv import GetAllPoses
import pytest
import rclpy

sys.path.append(os.path.dirname(__file__))
from helpers import run_cuvslam_from_bag, wait_for_odometry_message  # noqa: I100 E402

_TEST_CASE_NAMESPACE = '/visual_slam_test_srv_get_all_poses'


@pytest.mark.rostest
def generate_test_description():
    bag_path = pathlib.Path(__file__).parent / 'test_cases/rosbags/r2b_galileo'
    override_parameters = {'load_map_folder_path': str(bag_path / 'cuvslam_map')}
    return run_cuvslam_from_bag(_TEST_CASE_NAMESPACE, bag_path, override_parameters)


class IsaacRosVisualSlamServiceTest(IsaacROSBaseTest):
    """This test checks the functionality of the `visual_slam/get_all_poses` service."""

    def test_localize_in_map_service(self):
        self.assertTrue(wait_for_odometry_message(self.node, _TEST_CASE_NAMESPACE))

        service_client = self.node.create_client(
            GetAllPoses,
            f'{_TEST_CASE_NAMESPACE}/visual_slam/get_all_poses',
        )
        self.assertTrue(service_client.wait_for_service(timeout_sec=20))

        request = GetAllPoses.Request()
        request.max_count = 10

        response_future = service_client.call_async(request)
        rclpy.spin_until_future_complete(self.node, response_future)
        response = response_future.result()
        self.assertTrue(response.success)
