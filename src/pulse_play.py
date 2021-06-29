import ctypes
import sys

import io


pa = ctypes.cdll.LoadLibrary('libpulse-simple.so.0')

PA_STREAM_PLAYBACK = 1
PA_SAMPLE_S16LE = 3
BUFFSIZE = 1024
RATE = 24000
CHANNEL = 1

class struct_pa_sample_spec(ctypes.Structure):
    __slots__ = [
        'format',
        'rate',
        'channels',
    ]

struct_pa_sample_spec._fields_ = [
    ('format', ctypes.c_int),
    ('rate', ctypes.c_uint32),
    ('channels', ctypes.c_uint8),
]
pa_sample_spec = struct_pa_sample_spec


def PlayAudio(buffer_data):
    da = io.BytesIO(buffer_data)
    offset = 0
    buff = da.getbuffer()

    # Defining sample format.
    ss = struct_pa_sample_spec()
    ss.rate = RATE
    ss.channels = CHANNEL
    ss.format = PA_SAMPLE_S16LE
    error = ctypes.c_int(0)

    s = pa.pa_simple_new(
        None,  # Default server.
        "InteractiveRB5",  # Application name.
        PA_STREAM_PLAYBACK,  # Stream for playback.
        None,  # Default device.
        'playback',  # Stream description.
        ctypes.byref(ss),  # Sample format.
        None,  # Default channel map.
        None,  # Default buffering attributes.
        ctypes.byref(error)  # Ignore error code.
    )
    if not s:
        print("Unable to Play Audio")
        return -1

    length = len(buff)
    while True:
        latency = pa.pa_simple_get_latency(s, error)
        if latency == -1:
            print("Failed to get latency value!")
            return -1

        buf = buff[offset:offset+BUFFSIZE]
        buf = bytes(buf)
        offset+=BUFFSIZE

        if offset > length:
            break

        pa.pa_simple_write(s, buf, len(buf), error)

    if pa.pa_simple_drain(s, error):
        print("Not able to play audio properly")
        return -1

    pa.pa_simple_free(s)

