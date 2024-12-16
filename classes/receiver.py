from time import time
class Signal:
    """
    Signal class containing relevant information of signals.
    """
    def __init__(self,mac_adress,rssi,time_received) -> None:
        self.mac_adress = mac_adress 
        self.rssi = rssi
        self.time_received = time_received
        pass

class Receiver:
    """
    Receiver class containing relvant information of receivers.
    """
    def __init__(self,host_name,cordinates) -> None:
        self.cordinates = cordinates
        self.host_name = host_name
        self.signals:list[Signal] = [] 
        pass

    def HasMac(self,mac_adress):
        """
        Checks if self contains a signal with given mac adress.
        """
        all_mac = [i.mac_adress for i in self.signals]

        return mac_adress in all_mac

    def ReceivedSignal(self,signal:Signal):
        """
        Updates existing signal if mac adress exists. Else creates a new signal.
        """
        all_mac = [i.mac_adress for i in self.signals]
        if signal.mac_adress in all_mac: 
            index = all_mac.index(signal.mac_adress)
            self.signals[index] = signal
        else:
            self.signals.append(signal)

    def UpdateSignals(self,countdown=5):
        """
        Removes signals which has not been updated the last 30 seconds.
        """
        current_time = time()
        self.signals[:] = [signal for signal in self.signals if current_time - signal.time_received < countdown]    

    def RemoveSignalMac(self,mac_adress):
        """
        Removes the signal which has the given mac adress.
        """
        self.signals[:] = [signal for signal in self.signals if not signal.mac_adress == mac_adress]    

    def GetRSSIMac(self,mac_adress):
        """
        Returns the RSSI value of the signal with the given mac adress.
        """
        out = [signal for signal in self.signals if signal.mac_adress == mac_adress]    

        return out[0].rssi


