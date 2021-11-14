From: https://github.com/confluentinc/cp-all-in-one/

### Changes

To `broker` was added things below, so services from other `docker-compose` 
configuration could connect through `host.docker.internal`:
- `DHOST://host.docker.internal:9093` in `KAFKA_ADVERTISED_LISTENERS` env variable
- `DHOST:PLAINTEXT` in `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP` env variable
- `9093:9093` port routing to container configuration