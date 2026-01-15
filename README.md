# Siemens S7 Cloud Gateway ☁️🏭

A production-ready asynchronous bridge to connect Siemens S7-1200/1500 PLCs to MQTT brokers (and by extension, any cloud like AWS, Azure, or Thingsboard).

## Features

- **Asynchronous I/O**: High-performance polling and subscriptions using `opcua-asyncio`.
- **Secure**: Supports OPC UA Certificate-based authentication.
- **Dockerized**: Easy deployment as a microservice.
- **Configurable**: Define tags and MQTT topics in `config.yaml`.

## Architecture

```mermaid
graph LR
    PLC[Siemens S7-1500] -- OPC UA --> Gateway[Python Gateway]
    Gateway -- MQTT --> Broker[MQTT Broker / Cloud]
```

## Quick Start

1. **Configure**: Edit `config/config.yaml`.
2. **Run**:
   ```bash
   docker-compose up -d
   ```
