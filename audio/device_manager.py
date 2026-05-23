import sounddevice as sd

def list_input_devices():
    devices=[]
    for i,d in enumerate(sd.query_devices()):
        if d["max_input_channels"]>0:
            devices.append((i,d["name"], d["max_input_channels"]))
    return devices