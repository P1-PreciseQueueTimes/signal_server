from time import time
class Signal:
    def __init__(self,mac_adress,rssi,time_received) -> None:
        self.mac_adress = mac_adress 
        self.rssi = rssi
        self.time_received = time_received
        pass
class Receiver:
    def __init__(self,host_name) -> None:
        self.host_name = host_name
        self.signals:list[Signal] = [] 
        pass

    def HasMac(self,mac_adress):
        all_mac = [i.mac_adress for i in self.signals]

        return mac_adress in all_mac

    def ReceivedSignal(self,signal:Signal):
        all_mac = [i.mac_adress for i in self.signals]
        if signal.mac_adress in all_mac: 
            index = all_mac.index(signal.mac_adress)
            self.signals[index] = signal
        else:
            self.signals.append(signal)

    def UpdateSignals(self,countdown=5):
        current_time = time()
        self.signals[:] = [signal for signal in self.signals if current_time - signal.time_received < countdown]    

    def RemoveSignalMac(self,mac_adress):
        self.signals[:] = [signal for signal in self.signals if not signal.mac_adress == mac_adress]    

    def GetRSSIMac(self,mac_adress):
        out = [signal for signal in self.signals if signal.mac_adress == mac_adress]    

        return next(iter(out))


