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

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.FireExtinguisherActuatorSimTask import FireExtinguisherActuatorSimTask


class FireExtinguisherActuatorSimTaskTest(unittest.TestCase):
    DEFAULT_VAL_A = 5.5
    DEFAULT_VAL_B = 70.3

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing FireExtinguisherActuatorSimTask class...")
        self.feeSimTask = FireExtinguisherActuatorSimTask()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdateActuator(self):
        ad = ActuatorData(typeID=ConfigConst.FIRE_EXTINGUISHER_ACTUATOR_TYPE)
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        self.assertEqual(adr.getValue(), self.DEFAULT_VAL_A)
        logging.info("ActuatorData: " + str(adr))

        ad.setValue(self.DEFAULT_VAL_B)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        self.assertEqual(adr.getValue(), self.DEFAULT_VAL_B)
        logging.info("ActuatorData: " + str(adr))

        ad.setCommand(ConfigConst.COMMAND_OFF)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        self.assertEqual(adr.getCommand(), ConfigConst.COMMAND_OFF)
        logging.info("ActuatorData: " + str(adr))

    #@unittest.skip("Ignore for now.")
    def testUpdateActuatorRepeatCommands(self):
        ad = ActuatorData(typeID=ConfigConst.FIRE_EXTINGUISHER_ACTUATOR_TYPE)

        # new command ON with new value - should succeed
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        self.assertEqual(adr.getValue(), self.DEFAULT_VAL_A)
        logging.info("ActuatorData: " + str(adr))

        # same command ON with same value - should fail
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNone(adr)
        logging.info("ActuatorData: " + str(adr))

        # new command OFF with same value - should succeed
        ad.setCommand(ConfigConst.COMMAND_OFF)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        self.assertEqual(adr.getValue(), self.DEFAULT_VAL_A)
        logging.info("ActuatorData: " + str(adr))

        # same command OFF with different value - should succeed
        ad.setCommand(ConfigConst.COMMAND_OFF)
        ad.setValue(self.DEFAULT_VAL_B)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        logging.info("ActuatorData: " + str(adr))

        # new command ON with same value - should succeed
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(self.DEFAULT_VAL_B)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        logging.info("ActuatorData: " + str(adr))

        # same command ON with new value - should succeed
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        logging.info("ActuatorData: " + str(adr))

        # new command OFF with same value - should succeed
        ad.setCommand(ConfigConst.COMMAND_OFF)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNotNone(adr)
        self.assertEqual(adr.getValue(), self.DEFAULT_VAL_A)
        logging.info("ActuatorData: " + str(adr))

        # same command OFF with same value - should fail
        ad.setCommand(ConfigConst.COMMAND_OFF)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.feeSimTask.updateActuator(ad)

        self.assertIsNone(adr)
        logging.info("ActuatorData: " + str(adr))


if __name__ == "__main__":
    unittest.main()