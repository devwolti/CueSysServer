try:
    from kivy.support import install_twisted_reactor

    install_twisted_reactor()
except:
    print('gna')

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import DatagramProtocol
from socket import SOL_SOCKET, SO_BROADCAST
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.clock import Clock
from functools import partial

from os import listdir

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path + kv)


class CueSysServer(protocol.Protocol):

    def __init__(self,clients,app):
        self.clients = clients
        self.uuid = False
        self.app = app

    def dataReceived(self, data):
        print("received...")
        print(data)

        message = data.decode('utf-8').split('@')
        if not self.uuid:
            if message[0] == 'CueSys':
                self.uuid = message[1]
                self.clients[self.uuid] = {}
                self.clients[self.uuid]['name'] = self.uuid
                self.clients[self.uuid]['status'] = 0
                self.clients[self.uuid]['connection'] = self
                self.app.addTCPClient(self.uuid)
        if message[0] == 'Status' and message[1] == 'Confirmed':
            if self.clients[self.uuid]['status'] & 0b0001:
                self.clients[self.uuid]['status'] -= 0b0001
                self.clients[self.uuid]['status'] += 0b0010
            print('Setting Status to 2 for '+self.uuid + ' now: '+str(self.clients[self.uuid]['status']))

    def sendName(self, name):
        self.transport.write(('Name@'+str(name)).encode())

    def sendStatus(self,status):
        self.transport.write(('Status@'+str(status)).encode())


        #response = self.factory.app.handle_message(self,data)
        #if response:
        #    self.transport.write(response)

    def connectionMade(self):
        print('New Connection')

    def connectionLost(self, reason):
        print('connection Lost to '+str(self.uuid))
        self.app.removeTCPClient(self.uuid)


class CueSysServerFactory(protocol.Factory):

    def __init__(self, app, clients):
        self.app = app
        self.clients = clients

    def buildProtocol(self, addr):
        return CueSysServer(self.clients,self.app)

class BCastFactory(DatagramProtocol):

    def __init__(self, app):
        self.app = app

    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        # Set the TTL>1 so multicast will cross router hops:
        # self.transport.setTTL(5)
        # Join a specific multicast group:
        # self.transport.joinGroup("228.0.0.5")

        # going Multicast
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        self.transport.connect("255.255.255.255", 8099)
        # giving the UDP connection to the App
        app.udpBCAST = self

    def sendDatagram(self):
        datagram = self.transport.getHost()
        self.transport.write(("CueSys@"+datagram.host+"@1.0").encode())

    def datagramReceived(self, datagram, address):
        print("Datagram %s received from %s" % (repr(datagram), repr(address)))


class StbButton(Button):
    background_color_normal = ListProperty([0.7, 0, 0, 1])
    background_color_highlight = ListProperty([1, 0, 0, 1])

    def __init__(self, **kwargs):
        super(StbButton, self).__init__(**kwargs)
        self.background_color = self.background_color_normal

    def setOn(self):
        self.background_color = self.background_color_highlight

    def setOff(self):
        self.background_color = self.background_color_normal


class PresetButton(Button):
    background_color_normal = ListProperty([0.7, 0.7, 0, 1])
    background_color_highlight = ListProperty([1, 1, 0, 1])

    def __init__(self, **kwargs):
        super(PresetButton, self).__init__(**kwargs)
        self.background_color = self.background_color_normal

    def setOn(self):
        self.background_color = self.background_color_highlight

    def setOff(self):
        self.background_color = self.background_color_normal


class GoButton(Button):
    background_color_normal = ListProperty([0, 0.7, 0, 1])
    background_color_highlight = ListProperty([0, 1, 0, 1])

    def __init__(self, **kwargs):
        super(GoButton, self).__init__(**kwargs)
        self.background_color = self.background_color_normal

    def setOn(self):
        self.background_color = self.background_color_highlight

    def setOff(self):
        self.background_color = self.background_color_normal


class StbMasterButton(Button):
    background_color_normal = ListProperty([0.7, 0, 0, 1])
    background_color_highlight = ListProperty([1, 0, 0, 1])

    def __init__(self, **kwargs):
        super(StbMasterButton, self).__init__(**kwargs)
        self.background_color = self.background_color_normal

    def setOn(self):
        self.background_color = self.background_color_highlight

    def setOff(self):
        self.background_color = self.background_color_normal


class PresetMasterButton(Button):
    background_color_normal = ListProperty([0.7, 0.7, 0, 1])
    background_color_highlight = ListProperty([1, 1, 0, 1])

    def __init__(self, **kwargs):
        super(PresetMasterButton, self).__init__(**kwargs)
        self.background_color = self.background_color_normal

    def setOn(self):
        self.background_color = self.background_color_highlight

    def setOff(self):
        self.background_color = self.background_color_normal


class GoMasterButton(Button):
    background_color_normal = ListProperty([0, 0.7, 0, 1])
    background_color_highlight = ListProperty([0, 1, 0, 1])

    def __init__(self, **kwargs):
        super(GoMasterButton, self).__init__(**kwargs)
        self.background_color = self.background_color_normal

    def setOn(self):
        self.background_color = self.background_color_highlight

    def setOff(self):
        self.background_color = self.background_color_normal

class NamePopup(Popup):

    app = False
    uuid = False

    def __init__(self, app,uuid, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.app = app
        self.uuid = uuid


class Container(GridLayout):
    display = ObjectProperty()

    def addMaster(self):
        elements = {}

        # assuming, that the uuid will never be 'Master'
        btn1 = StbMasterButton(id='Stb_Master')
        btn1.bind(on_release=self.on_event)
        btn2 = PresetMasterButton(id='Prs_Master')
        btn2.bind(on_release=self.on_event)
        btn3 = GoMasterButton(id='Go_Master')
        btn3.bind(on_release=self.on_event)

        self.master.add_widget(btn1)
        self.master.add_widget(btn2)
        self.master.add_widget(btn3)

        elements['Stb_Master'] = btn1
        elements['Prs_Master'] = btn2
        elements['Go_Master'] = btn3
        return elements

    def on_event(self, obj):
        #not needed, just for debugging
        print("Typical event from", obj.id)
        # obj.togglecolor()

    def addButton(self, uuid, name,app):
        elements = {}
        self.app = app
        layout = BoxLayout(orientation='vertical', id=uuid)
        popupcallback = partial(self.app.popupName, uuid)
        #need to find a good way for the renaming thing. For now take the uuid as the name
        l = Label(text='[ref='+uuid+']'+name+'[/ref]', font_size='15sp', markup=True)
        l.bind(on_ref_press=popupcallback)
        btn1 = StbButton(id='Stb_' + uuid)
        btn1.bind(on_release=self.on_event)
        btn2 = PresetButton(id='Prs_' + uuid)
        btn2.bind(on_release=self.on_event)
        btn3 = GoButton(id='Go_' + uuid)
        btn3.bind(on_release=self.on_event)
        layout.add_widget(l)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        self.clients.add_widget(layout)

        elements['L_' + uuid] = layout
        elements['Stb_' + uuid] = btn1
        elements['Prs_' + uuid] = btn2
        elements['Go_' + uuid] = btn3
        elements['Label_' + uuid] = l
        return elements

    def deleteClient(self,layout):
        layout.clear_widgets()
        self.clients.remove_widget(layout)


class MainApp(App):
    # ------------------ Globals ----------------------
    # all my elements
    # L_X are the Layouts
    # Stb_X are the Standby buttons
    # Prs_X are the Preset Buttons
    # Go_X are the Go Buttons
    elements = {}

    display = None
    blink = {}

    # Status
    # Binary implementation
    # Position/Value
    # 1 = RedBlink
    # 2 = Red
    # 3 = yellow
    # 4 = Green
    clientstatus = {}
    TCPClients = {}

    # State of the Blink, so all of them are at the same time on or off
    onoff = False

    udpBCAST = False

    # ------------------- App Stuff --------------------
    # first setup
    def build(self):
        self.title = 'CueSys'

        # get my container
        display = Container()
        self.display = display

        # add clients
        self.addMaster()

        self.TCPClients['Master'] = {}
        self.TCPClients['Master']['name'] = 'Master'
        self.TCPClients['Master']['status'] = 0
        self.TCPClients['Master']['connection'] = False

        self.TCPClients['1'] = {}
        self.TCPClients['1']['name'] = 'Stage'
        self.TCPClients['1']['status'] = 0
        self.TCPClients['1']['connection'] = False
        self.TCPClients['2'] = {}
        self.TCPClients['2']['name'] = 'FOH'
        self.TCPClients['2']['status'] = 0
        self.TCPClients['2']['connection'] = False
        self.TCPClients['3'] = {}
        self.TCPClients['3']['name'] = 'Dirigat'
        self.TCPClients['3']['status'] = 0
        self.TCPClients['3']['connection'] = False

        self.addClient('1','Stage')
        self.addClient('2','FOH')
        self.addClient('3','Dirigat')

        # setting up the blinking stuff
        blinkerevent = Clock.schedule_interval(self.blinker, 0.5)

        try:
            reactor.listenUDP(8098, BCastFactory(self))
            reactor.listenTCP(8090, CueSysServerFactory(self,self.TCPClients))

        except:
            print('Server could not be started! Is another instance running?')

        return display

    def addMaster(self):
        self.elements['Master'] = self.display.addMaster()
        self.clientstatus['Master'] = 0

    def addClient(self, uuid, name):
        self.elements[uuid] = self.display.addButton(uuid,name,self)
        self.clientstatus[uuid] = 0

    def blinker(self, dt):
        stbMaster = False
        prsMaster = False
        goMaster = False
        for key, value in self.TCPClients.items():
            if key != 'Master':
                if self.TCPClients[key]['status'] & 0b1000:
                    self.elements[key]['Go_' + key].setOn()
                    goMaster = True
                else:
                    self.elements[key]['Go_' + key].setOff()
                if self.TCPClients[key]['status'] & 0b0100:
                    self.elements[key]['Prs_' + key].setOn()
                    prsMaster = True
                else:
                    self.elements[key]['Prs_' + key].setOff()
                if self.TCPClients[key]['status'] & 0b0010:
                    print('yes. i am '+key+' with status'+str(self.TCPClients[key]['status']))
                    self.elements[key]['Stb_' + key].setOn()
                    stbMaster = True
                elif self.TCPClients[key]['status'] & 0b0001:
                    if not self.onoff:
                        self.elements[key]['Stb_' + key].setOff()
                    else:
                        self.elements[key]['Stb_' + key].setOn()
                    stbMaster = True
                else:
                    self.elements[key]['Stb_' + key].setOff()

        if stbMaster:
            if not self.onoff:
                self.elements['Master']['Stb_Master'].setOff()
            else:
                self.elements['Master']['Stb_Master'].setOn()
        else:
            self.elements['Master']['Stb_Master'].setOff()

        if prsMaster:
            if not self.onoff:
                self.elements['Master']['Prs_Master'].setOff()
            else:
                self.elements['Master']['Prs_Master'].setOn()
        else:
            self.elements['Master']['Prs_Master'].setOff()

        if goMaster:
            if prsMaster:
                if not self.onoff:
                    self.elements['Master']['Go_Master'].setOff()
                else:
                    self.elements['Master']['Go_Master'].setOn()
            else:
                self.elements['Master']['Go_Master'].setOn()
        else:
            self.elements['Master']['Go_Master'].setOff()

        if not self.onoff:
            self.onoff = True
        else:
            self.onoff = False

        self.udpBCAST.sendDatagram()
        #for key, value in self.TCPClients.items():
    #        if self.TCPClients[key]['connection']:
    #            self.TCPClients[key]['connection'].transport.write(('Status@'+str(self.TCPClients[key]['status'])).encode())
        for key, value in self.TCPClients.items():
            if self.TCPClients[key]['connection']:
                self.TCPClients[key]['connection'].sendStatus(self.TCPClients[key]['status'])

    def btnPressed(self, obj):
        pair = obj.id.split('_')

        if pair[0] == 'Stb':
            if self.TCPClients[pair[1]]['status'] & 0b1000:
                self.TCPClients[pair[1]]['status'] -= 0b1000
            if self.TCPClients[pair[1]]['status'] & 0b0010:
                self.TCPClients[pair[1]]['status'] -= 0b0010
            if self.TCPClients[pair[1]]['status'] & 0b0001:
                self.TCPClients[pair[1]]['status'] -= 0b0001
            else:
                self.TCPClients[pair[1]]['status'] += 0b0001

        elif pair[0] == 'Prs':
            if self.TCPClients[pair[1]]['status'] & 0b0100:
                self.TCPClients[pair[1]]['status'] -= 0b0100
            else:
                self.TCPClients[pair[1]]['status'] += 0b0100
                if self.TCPClients[pair[1]]['status'] & 0b1000:
                    self.TCPClients[pair[1]]['status'] -= 0b1000

        elif pair[0] == 'Go':
            if self.TCPClients[pair[1]]['status'] & 0b0010:
                self.TCPClients[pair[1]]['status'] -= 0b0010
            if self.TCPClients[pair[1]]['status'] & 0b0001:
                self.TCPClients[pair[1]]['status'] -= 0b0001
            if self.TCPClients[pair[1]]['status'] & 0b1000:
                self.TCPClients[pair[1]]['status'] -= 0b1000
            else:
                self.TCPClients[pair[1]]['status'] += 0b1000
                if self.TCPClients[pair[1]]['status'] & 0b0100:
                    self.TCPClients[pair[1]]['status'] -= 0b0100
        # print ("{0:b}".format(self.clientstatus[pair[1]]))

    def btnMasterPressed(self, obj):
        pair = obj.id.split('_')
        stbMaster = False
        stbrdyMaster = False
        prsMaster = False
        goMaster = False
        for key, value in self.TCPClients.items():
            if self.TCPClients[key]['status'] & 0b1000 and key != 'Master':
                goMaster = True
            if self.TCPClients[key]['status'] & 0b0100 and key != 'Master':
                prsMaster = True
            if self.TCPClients[key]['status'] & 0b0010 and key != 'Master':
                stbrdyMaster = True
            if self.TCPClients[key]['status'] & 0b0001 and key != 'Master':
                stbMaster = True

        if pair[0] == 'Stb':
            if stbMaster or stbrdyMaster:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b0001 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0001
                    if self.TCPClients[key]['status'] & 0b0010 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0010
            else:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b1000 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b1000
                    self.TCPClients[key]['status'] += 0b0001

        if pair[0] == 'Prs':
            if prsMaster:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b0100 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0100
            else:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b1000 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b1000
                    self.TCPClients[key]['status'] += 0b0100

        if pair[0] == 'Go':
            # there are some GOs and some in Prs -> prs to go
            if goMaster and prsMaster:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b0100 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0100
                        self.TCPClients[key]['status'] += 0b1000
                        if self.TCPClients[key]['status'] & 0b0001 and key != 'Master':
                            self.TCPClients[key]['status'] -= 0b0001
                        if self.TCPClients[key]['status'] & 0b0010 and key != 'Master':
                            self.TCPClients[key]['status'] -= 0b0010
            # if only GOs -> delete GOs
            elif goMaster and not prsMaster:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b1000 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b1000
            # same as first
            elif prsMaster and not goMaster:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b0100 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0100
                        self.TCPClients[key]['status'] += 0b1000
                        if self.TCPClients[key]['status'] & 0b0001 and key != 'Master':
                            self.TCPClients[key]['status'] -= 0b0001
                        if self.TCPClients[key]['status'] & 0b0010 and key != 'Master':
                            self.TCPClients[key]['status'] -= 0b0010
            else:
                for key, value in self.TCPClients.items():
                    if self.TCPClients[key]['status'] & 0b0010 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0010
                    if self.TCPClients[key]['status'] & 0b0001 and key != 'Master':
                        self.TCPClients[key]['status'] -= 0b0001
                    self.TCPClients[key]['status'] += 0b1000

    def popupName(self,label,value,uuid):

        # create content and add to the popup
        name = self.TCPClients[uuid]['name']

        #layout = BoxLayout(orientation='vertical')
        layout = FloatLayout(id='layout')
        textinput = TextInput(text=self.TCPClients[uuid]['name'], multiline=False, size_hint=(1, .2),pos_hint={'x':0, 'y':.8},id='mytext')
        exitbutton = Button(text='Save', size_hint=(1, .2),pos_hint={'x':0, 'y':0})
        layout.add_widget(textinput)
        layout.add_widget(exitbutton)
        popup = NamePopup(self,uuid, content=layout,title='Change Name', auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        popup.bind(on_dismiss=partial(self.saveName,textinput,uuid))
        exitbutton.bind(on_press=popup.dismiss)
        #exitbutton.bind(on_press=)

        # open the popup
        popup.open()
        #self.TCPClients[value]['name'] = self.uuid
        #label.text = text


    def saveName(self, textinput,uuid,obj):
        self.TCPClients[uuid]['name'] = textinput.text
        self.elements[uuid]['Label_'+uuid].text = textinput.text
        if self.TCPClients[uuid]['connection']:
            self.TCPClients[uuid]['connection'].sendName(textinput.text)

    # ----------------- Network Stuff -----------------------
    def handle_message(self, msg):

        server = msg.decode('utf-8').split('@')

        self.display.mainview.text = "received:  {}\n".format(msg)
        print("received:  {}\n".format(msg))
        if msg == "ping":
            msg = "Pong"
        if msg == "plop":
            msg = "Kivy Rocks!!!"
        self.display.mainview.text += "responded: {}\n".format(msg)
        return msg.encode('utf-8')

    def addTCPClient(self, name):
        self.addClient(name,name)

    def removeTCPClient(self, name):
        print('removing '+name)
        self.display.deleteClient(self.elements[name]['L_' + name])
        self.elements.pop(name,None)
        self.TCPClients.pop(name, None)


    def on_anything(self, *args, **kwargs):
        print('The flexible function has *args of', str(args),
            "and **kwargs of", str(kwargs))


if __name__ == "__main__":
    app = MainApp()
    app.run()
