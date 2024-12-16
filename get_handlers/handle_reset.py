import misc_elements
def handleReset():
    """
    Handles resetting of receivers.
    """
    for receiver in misc_elements.RECEIVERS:
        receiver.signals = []
    print("Reset receivers")
    return ""
