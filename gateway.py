import asyncio
import logging
import yaml
from asyncua import Client, ua
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubscriptionHandler:
    """
    Handles OPC UA DataChange events and publishes them to MQTT.
    """
    def __init__(self, mqtt_c, topic_prefix):
        self.mqtt_c = mqtt_c
        self.topic_prefix = topic_prefix

    def datachange_notification(self, node, val, data):
        topic = f"{self.topic_prefix}/{node.nodeid.Identifier}"
        logger.info(f"New Value for {node}: {val}")
        self.mqtt_c.publish(topic, str(val))

async def main():
    # 1. Load Config
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # 2. Setup MQTT
    mqtt_c = mqtt_client.Client()
    mqtt_c.connect(config['mqtt']['host'], config['mqtt']['port'])
    mqtt_c.loop_start()

    # 3. Setup OPC UA
    url = f"opc.tcp://{config['plc']['ip']}:4840"
    async with Client(url=url) as client:
        # Load security certificates if enabled
        if config['plc'].get('cert'):
            await client.set_security_IDs(
                uri="urn:example:client",
                certificate=config['plc']['cert'],
                private_key=config['plc']['key']
            )

        logger.info(f"Connected to Siemens PLC at {url}")
        
        # 4. Subscribe to Nodes
        handler = SubscriptionHandler(mqtt_c, config['mqtt']['topic_prefix'])
        sub = await client.create_subscription(500, handler)
        
        nodes = []
        for tag in config['tags']:
            node = await client.get_node(tag['node_id'])
            nodes.append(node)
        
        await sub.subscribe_data_change(nodes)

        # Keep alive
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
