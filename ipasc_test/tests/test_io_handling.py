# BSD 3-Clause License
#
# Copyright (c) 2020, IPASC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import numpy as np
from unittest.case import TestCase

from ipasc_tool import PAData
from ipasc_tool import write_data
from ipasc_tool import load_data
from ipasc_test.tests.utils import create_complete_device_metadata_dictionary


class DeviceMetaDataCreatorTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_write_and_read_random_dictionary(self):

        device_dict = create_complete_device_metadata_dictionary()

        pa_data = PAData(binary_time_series_data=np.zeros([256, 2048]),
                         meta_data_acquisition={"test_int": 3, "test_float": 3.14, "test_string": "ipasc_test",
                                                "test_list": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                                "test_nested_list": [1, 2, 5, {"key": [1, ["1", 1]]}]},
                         meta_data_device=device_dict)

        try:
            write_data("ipasc_test.hdf5", pa_data)
            test_data = load_data("ipasc_test.hdf5")
        except Exception as e:
            raise e
        finally:
            # clean up after ipasc_test
            if os.path.exists("ipasc_test.hdf5"):
                os.remove("ipasc_test.hdf5")

        def assertEqualsRecursive(a, b):
            if isinstance(a, dict):
                for item in a:
                    self.assertTrue(item in a)
                    self.assertTrue(item in b)
                    if isinstance(a[item], dict):
                        assertEqualsRecursive(a[item], b[item])
                    else:
                        if isinstance(a[item], np.ndarray):
                            self.assertTrue((a[item] == b[item]).all())
                        elif isinstance(a[item], list):
                            for item1, item2 in zip(a[item], b[item]):
                                assertEqualsRecursive(item1, item2)
                        else:
                            self.assertEqual(a[item], b[item])
            elif isinstance(a, list):
                for item1, item2 in zip(a, b):
                    assertEqualsRecursive(item1, item2)
            else:
                if isinstance(a, np.ndarray):
                    self.assertTrue((a == b).all())
                else:
                    self.assertEqual(a, b)

        assertEqualsRecursive(pa_data.meta_data_acquisition, test_data.meta_data_acquisition)
        assertEqualsRecursive(pa_data.meta_data_device, test_data.meta_data_device)
        self.assertTrue((pa_data.binary_time_series_data == test_data.binary_time_series_data).all())
