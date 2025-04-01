
class BusMaster:
    def __init__(self,uart_radio):
        self.uart_radio = uart_radio
        print("Initializing bus master...")


    def send(self, msg):
        print(msg['radio'], msg['pwr'])
        bus_msg = "<,Y,R,{},P,{},N,{},S,{},T,{},>\n".format(msg['radio'], msg['pwr'], msg['nbr'],msg['base_rssi'],msg['remote_rssi'])
        print("BusMaster sending:", bus_msg)
        self.uart_radio.write(bus_msg.encode())

    def set_base_node(self):
        bus_msg = "<,X,R,0,P,10,N,0,S,0,T,0,>\n"
        # print("BusMaster set base node:", bus_msg)
        self.uart_radio.write(bus_msg.encode()) 

    def relay_msg(self, pmsg):
        bus_msg = "<,Y,R,{},P,{},N,{},S,{},T,{},>\n".format(pmsg['radio'], pmsg['pwr'], pmsg['nbr'],pmsg['base_rssi'],pmsg['remote_rssi'])
        # print("BusMaster relaying message:", bus_msg)
        self.uart_radio.write(bus_msg.encode()) 

    def ack_msg(self, pmsg):
        bus_msg = "<,Y,R,{},P,{},N,{},S,{},T,{},>\n".format(pmsg['radio'], pmsg['pwr'], pmsg['nbr'],pmsg['base_rssi'],pmsg['remote_rssi'])
        # print("BusMaster acknowledge message:", bus_msg)
        self.uart_radio.write(bus_msg.encode()) 
    
    def log_msg(self, pmsg):
        # send via RFM69 regardless of the messege radio type
        bus_msg = "<,Z,R,{},P,{},N,{},S,{},T,{},>\n".format(pmsg['radio'], pmsg['pwr'], pmsg['nbr'],pmsg['base_rssi'],pmsg['remote_rssi'])
        #print("BusMaster log message:", bus_msg)
        self.uart_radio.write(bus_msg.encode())
    
    def receive(self):
        # print("BusMaster receiving message...")
        data = self.uart_radio.read(64)  # read up to 64 bytes
        if data is not None:
            # convert bytearray to string
            data_string = ''.join([chr(b) for b in data])
            # print(data_string, end="")
            return data_string
        

        
# bus_master = BusMaster()

