from flask import Flask, jsonify
from flask_cors import CORS
import random

# COM handling
import pythoncom
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

app = Flask(__name__)
CORS(app)

def set_system_volume(percent):
    pythoncom.CoInitialize()  # ✅ Initialize COM
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
    pythoncom.CoUninitialize()  # ✅ Clean up COM

@app.route('/status')
def status():
    song_types = ['Beat-heavy', 'Slow', 'Medium']
    song_type = random.choice(song_types)

    # Volume logic
    if song_type == 'Beat-heavy':
        volume = 40
    elif song_type == 'Slow':
        volume = 50
    else:
        volume = 45

    set_system_volume(volume)

    return jsonify({
        'song_type': song_type,
        'volume': volume
    })

if __name__ == '__main__':
    app.run(debug=True)
