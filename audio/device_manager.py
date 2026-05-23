import sounddevice as sd


def list_input_devices():
    devices = []

    for idx, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0:
            devices.append({
                "id": idx,
                "name": dev["name"],
                "channels": dev["max_input_channels"]
            })

    return devices