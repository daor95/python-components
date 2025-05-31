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

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.emulated.SmokeDetectorSensorEmulatorTask import SmokeDetectorSensorEmulatorTask

class SmokeDetectorSensorEmulatorTaskTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	SmokeDetectorEmulatorTaskTest. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	
	NOTE: This test requires the sense_emu_gui to be running
	and must have access to the underlying libraries that
	support the pisense module. On Windows, one way to do
	this is by installing pisense and sense-emu within the
	Bash on Ubuntu on Windows environment and then execute this
	test case from the command line, as it will likely fail
	if run within an IDE in native Windows.
	
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing SmokeDetectorEmulatorTask class [using SenseHAT emulator]...")
		self.sdTask = SmokeDetectorSensorEmulatorTask()
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testReadEmulator(self):
		sd = self.sdTask.generateTelemetry()
		
		if sd:
			self.assertEqual(sd.getTypeID(), ConfigConst.SMOKE_PARTICLE_SENSOR_TYPE)
			logging.info("SensorData: %f - %s", sd.getValue(), str(sd))
			
			# wait 5 seconds
			sleep(5)
		else:
			logging.warning("FAIL: SensorData is None.")

			
if __name__ == "__main__":
	unittest.main()
	