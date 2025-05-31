#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 by Andrew D. King
#

import logging
import unittest

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.SmokeDetectorSensorSimTask import SmokeDetectorSensorSimTask


class SmokeDetectorSensorSimTaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing CoParticleSensorSimTask class...")
        self.sdSimTask = SmokeDetectorSensorSimTask()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip("Ignore for now.")
    def testGenerateTelemetry(self):
        sd = self.sdSimTask.generateTelemetry()

        self.assertIsNotNone(sd)

        # default simulator generates temp values > 0.0C
        self.assertGreaterEqual(sd.getValue(), ConfigConst.DEFAULT_VAL)
        logging.info("Smoke size SensorData: %s", str(sd))

    # @unittest.skip("Ignore for now.")
    def testGetTelemetryValue(self):
        val = self.sdSimTask.getTelemetryValue()

        self.assertGreater(val, 0.0)
        logging.info("Smoke size data: %f", val)


if __name__ == "__main__":
    unittest.main()