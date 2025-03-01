# Solar Plus Intelbras Notification System

## Using the notification system in your automations

You can trigger custom alerts using the `solar_plus_intelbras.send_alert` service in your automations:

```yaml
automation:
  - alias: "Notify on inverter disconnection"
    trigger:
      platform: state
      entity_id: binary_sensor.solar_inverter_connected
      to: "off"
    action:
      - service: solar_plus_intelbras.send_alert
        data:
          title: "Inverter Alert"
          message: "Solar inverter has disconnected!"
          priority: "critical"
```

## Available priority levels

- `normal`: Standard notification
- `warning`: Warning level notification
- `critical`: Critical alert notification
- `info`: Information notification

## From Python code

If you need to create notifications from your component's Python code:

```python
# Get the notifier
notifier = hass.data["solar_plus_intelbras"]["notifier"]

# Send an alert
notifier.send_alert(
    message="Battery level is critical: 10%",
    title="Battery Alert",
    priority="warning"
)

# Send a system status update
notifier.send_system_status_alert("degraded", "Performance is below expected levels")
```
