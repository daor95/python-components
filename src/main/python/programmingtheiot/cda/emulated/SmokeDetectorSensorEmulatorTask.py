#####
#
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import random
from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from pisense import SenseHAT


class SmokeDetectorSensorEmulatorTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, dataSet=None):
        super(SmokeDetectorSensorEmulatorTask, self).__init__(name = ConfigConst.SMOKE_PARTICLE_SENSOR_NAME,
															  typeID = ConfigConst.SMOKE_PARTICLE_SENSOR_TYPE,)

        enableEmulation = ConfigUtil().getBoolean(ConfigConst.CONSTRAINED_DEVICE,
                                                  ConfigConst.ENABLE_EMULATOR_KEY)

        self.sh = SenseHAT(emulate = enableEmulation)

    def generateTelemetry(self) -> SensorData:
        """
        Method to generate particles with a chance
        """

        sensorData = SensorData(name = self.getName(),
                                typeID = self.getTypeID())

        # 80% chance to simulate normal levels (0–20 ppm), 20% chance for elevated levels (20–100 ppm)
        if random.random() < 0.8:
            pm_2_5 = random.uniform(0, 35)
        else:
            pm_2_5 = random.uniform(36, 100)

        # Set the simulated CO value
        sensorData.setValue(pm_2_5)
        self.latestSensorData = sensorData

        return sensorData