#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.FireExtinguisherActuatorSimTask import FireExtinguisherActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.dataMsgListener = dataMsgListener

		self.configUtil = ConfigUtil()

		self.useSimulator = \
			self.configUtil.getBoolean(
				section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_SIMULATOR_KEY)
		self.useEmulator = \
			self.configUtil.getBoolean(
				section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_EMULATOR_KEY)
		self.deviceID = \
			self.configUtil.getProperty(
				section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.DEVICE_LOCATION_ID_KEY,
				defaultVal=ConfigConst.NOT_SET)
		self.locationID = \
			self.configUtil.getProperty(
				section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.DEVICE_LOCATION_ID_KEY,
				defaultVal=ConfigConst.NOT_SET)

		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None

		"""Actuator for fire extinguisher control."""
		self.fireExtinguisherActuator = None

		# Log emulator/simulator usage
		if self.useEmulator:
			logging.info("Emulators will be used for environmental actuation.")
		else:
			logging.info("Simulators will be used for environmental actuation.")

		# see PIOT-CDA-03-007 description for thoughts on the next line of code
		self._initEnvironmentalActuationTasks()

	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		if data and not data.isResponseFlagEnabled():
			# first check if the actuation event is destined for this device
			if data.getLocationID() == self.locationID or data.getLocationID() == "ConstrainedDevice":
				logging.info("Actuator command received for location ID %s. Processing...", str(data.getLocationID()))

				aType = data.getTypeID()
				responseData = None

				# TODO: implement appropriate logging and error handling

				try:
					if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
						logging.info("Updating humidifier actuator with data: %s", str(data))
						responseData = self.humidifierActuator.updateActuator(data)
					elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
						logging.info("Updating HVAC actuator with data: %s", str(data))
						responseData = self.hvacActuator.updateActuator(data)
					elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
						logging.info("Updating LED display actuator with data: %s", str(data))
						responseData = self.ledDisplayActuator.updateActuator(data)

					#NEW ACTUATOR TYPE - Fire Extinguisher Actuator
					elif aType == ConfigConst.FIRE_EXTINGUISHER_ACTUATOR_TYPE and self.fireExtinguisherActuator:
						logging.info("Updating CO PARTICLE Actuator with data: %s", data)
						responseData = self.fireExtinguisherActuator.updateActuator(data)

					else:
						logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())
				except Exception as e:
					logging.error("Error occurred while processing actuator command: %s", str(e), exc_info=True)

				# TODO: in a later lab module, the responseData instance will be
				# passed to a callback function implemented in DeviceDataManager
				# via IDataMessageListener

				return responseData
			else:
				logging.warning("Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s",
								str(self.locationID), str(data.getLocationID()))
		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")

		return None

	def setDataMessageListener(self, listener: IDataMessageListener):
		if listener:
			self.dataMsgListener = listener

	def _initEnvironmentalActuationTasks(self):
		if not self.useEmulator:
			# load the environmental tasks for simulated actuation
			self.humidifierActuator = HumidifierActuatorSimTask()

			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()

			"""Task for fire extinguisher control."""
			self.fireExtinguisherActuator = FireExtinguisherActuatorSimTask()

		else:
			hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidiferEmulatorTask')
			hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
			self.humidifierActuator = hueClazz()

			# create the HVAC actuator emulator
			hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
			hveClazz = getattr(hveModule, 'HvacEmulatorTask')
			self.hvacActuator = hveClazz()

			# create the LED display actuator emulator
			leDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
			leClazz = getattr(leDisplayModule, 'LedDisplayEmulatorTask')
			self.ledDisplayActuator = leClazz()

			"""Emulator for fire extinguisher control."""
			feeModule = import_module('programmingtheiot.cda.emulated.FireExtinguisherEmulatorTask', 'FireExtinguisherEmulatorTask')
			feeClazz = getattr(feeModule, 'FireExtinguisherEmulatorTask')
			self.particleActuator = feeClazz()

