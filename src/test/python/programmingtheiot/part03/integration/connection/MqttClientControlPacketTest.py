import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):
    """
    Integration tests to generate all MQTT 3.1.1 control packets:
      - CONNECT / CONNACK
      - PINGREQ / PINGRESP (keep-alive)
      - PUBLISH / PUBACK (QoS 1)
      - PUBLISH / PUBREC / PUBREL / PUBCOMP (QoS 2)
      - SUBSCRIBE / SUBACK
      - UNSUBSCRIBE / UNSUBACK
      - DISCONNECT
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Executing the MqttClientControlPacketTest class...")
        cls.cfg = ConfigUtil()
        # Use a different clientID from your CDA
        cls.mcc = MqttClientConnector(clientID="MyTestMqttClient")
        # Attach a listener to handle incoming messages
        cls.mcc.setDataMessageListener(DefaultDataMessageListener())

    def setUp(self):
        # Tear down any leftover connection
        try:
            self.mcc.disconnectClient()
        except Exception:
            logging.info("Failed to disconnect client in setUp.")
        sleep(1)

        # Re‑create a fresh client for this test
        self.mcc = MqttClientConnector(clientID="MyTestMqttClient")
        self.mcc.setDataMessageListener(DefaultDataMessageListener())

    def tearDown(self):
        # Fully disconnect after each test
        try:
            self.mcc.disconnectClient()
        except Exception:
            logging.info("Failed to disconnect client in tearDown.")
        sleep(1)

    def testConnectAndDisconnect(self):
        """
        Generate CONNECT → CONNACK and then DISCONNECT.
        """
        # CONNECT packet
        self.mcc.connectClient()
        # allow time for CONNACK
        sleep(2)
        # DISCONNECT packet
        self.mcc.disconnectClient()

    def testServerPing(self):
        """
        Generate PINGREQ / PINGRESP via keep-alive mechanism.
        """
        keep_alive = self.cfg.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE,
            ConfigConst.KEEP_ALIVE_KEY,
            ConfigConst.DEFAULT_KEEP_ALIVE
        )

        self.mcc.connectClient()
        # wait past keep-alive interval to force PINGREQ/PINGRESP
        sleep(keep_alive + 5)
        self.mcc.disconnectClient()

    def testPubSub(self):
        """
        For QoS 1 and QoS 2:
          - SUBSCRIBE → SUBACK
          - PUBLISH → PUBACK (QoS 1) or PUBREC/PUBREL/PUBCOMP (QoS 2)
          - UNSUBSCRIBE → UNSUBACK
        """
        topic = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        for qos in (1, 2):
            logging.info(f"--- Testing Pub/Sub with QoS={qos} ---")
            self.mcc.connectClient()

            # SUBSCRIBE → SUBACK
            self.mcc.subscribeToTopic(resource=topic, qos=qos)
            sleep(1)

            ad = ActuatorData()
            adJson = DataUtil().actuatorDataToJson(ad)

            # PUBLISH → PUBACK / PUBREC+PUBREL+PUBCOMP
            #payload = f"CONTROL_PACKET_TEST_QOS_{qos}"
            payload = adJson
            self.mcc.publishMessage(resource=topic, msg=payload, qos=qos)
            sleep(1)

            # UNSUBSCRIBE → UNSUBACK
            self.mcc.unsubscribeFromTopic(resource=topic)
            sleep(1)

            self.mcc.disconnectClient()
            sleep(1)

            # --- Sensor data ---
            topic = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
            self.mcc.connectClient()
            self.assertTrue(self.mcc.subscribeToTopic(resource=topic, qos=qos))
            sleep(1)

            sd = SensorData()
            sdJson = DataUtil().sensorDataToJson(sd)
            self.assertTrue(self.mcc.publishMessage(resource=topic, msg=sdJson, qos=qos))
            sleep(1)

            self.assertTrue(self.mcc.unsubscribeFromTopic(resource=topic))
            sleep(1)
            self.mcc.disconnectClient()
            sleep(1)

            # --- System performance data ---
            topic = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE
            self.mcc.connectClient()
            self.assertTrue(self.mcc.subscribeToTopic(resource=topic, qos=qos))
            sleep(1)

            sp = SystemPerformanceData()
            spJson = DataUtil().systemPerformanceDataToJson(sp)
            self.assertTrue(self.mcc.publishMessage(resource=topic, msg=spJson, qos=qos))
            sleep(1)

            self.assertTrue(self.mcc.unsubscribeFromTopic(resource=topic))
            sleep(1)
            self.mcc.disconnectClient()
            sleep(1)

if __name__ == "__main__":
    unittest.main()
