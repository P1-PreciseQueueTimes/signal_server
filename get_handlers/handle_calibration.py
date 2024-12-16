import misc_elements
import json

def handleCalibrate():
    """
    Handles whenever the calibration mode is changed in html.
    """
    misc_elements.CALIBRATION_MODE = not misc_elements.CALIBRATION_MODE
    print(f"Set calibrate to {misc_elements.CALIBRATION_MODE}")
    return json.dumps({"mode":misc_elements.CALIBRATION_MODE}) 
