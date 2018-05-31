#!/usr/bin/env python3

# Imports---------------------------------------------------------------------------------------------------------------
import os
import platform
import time
import tkinter as tk
from tkinter import LEFT, TOP, X, FLAT, RAISED
from threading import Thread
from Modules import csrf, funksjoner

if os.name == "posix" and platform.system() == "Linux":  # Check system
    from Modules import adc as ADC
    from Modules import pwm as PWM
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    from Modules import relestyring
    rpi = 1
    # os.system("sudo pigpiod")
    # PWM.hpwm(500000,750000)
else:
    print("Feil: programvare kjøres fra feil platform eller os")
    rpi = 0

# Global variables------------------------------------------------------------------------------------------------------

lanse_type = None
placement = None
auto_man = None

serverDict = {}
sendDict = {}

creds = 'tempfile.temp' # Variable that becomes login data document
lanse_info = "lanse.temp"  # Lagret lansetype
plass_info = "plass.temp"  # Lagret plassering
analoge_maalinger = "maal.temp"
LARGE_FONT = ("Verdana", 12)# Font type og størrelse



# Functions ------------------------------------------------------------------------------------------------------------


def CheckLogin(cntrl,nameEL,pwordEL):  # Used to check if username and password is correct.
    with open(creds) as f:
        data = f.readlines()  # This takes the entire document we put the info into and puts it into the data variable
        uname = data[0].rstrip()  # Data[0], 0 is the first line, 1 is the second and so on.
        pword = data[1].rstrip()  # Using .rstrip() will remove the \n (new line) word from before when we input it

    if ((nameEL.get() == "admin" and pwordEL.get() == "admin") or
            (nameEL.get() == uname and pwordEL.get() == pword)):  # Checks to see if you entered the correct data.
        cntrl.show_frame(SnTypePage)
    else:
        cntrl.frames[Login].signuptext.set("Feil brukernavn/passord")


def CheckReLogin(cntrl):  # Used to check if username and password is correct.
    nameEL = cntrl.frames[ReLogin].nameEL.get()
    pwordEL = cntrl.frames[ReLogin].pwordEL.get()

    with open(creds) as f:
        data = f.readlines()  # This takes the entire document we put the info into and puts it into the data variable
        uname = data[0].rstrip()  # Data[0], 0 is the first line, 1 is the second and so on.
        pword = data[1].rstrip()  # Using .rstrip() will remove the \n (new line) word from before when we input it

    if (((nameEL == "admin" and pwordEL) == "admin") or
        (nameEL == uname and pwordEL == pword)):  # Checks to see if you entered the correct data.
        cntrl.show_frame(Home)
        cntrl.frames[ReLogin].clear_text()  # Tømmer inntastingsfelt
        cntrl.frames[ReLogin].signuptext.set("")  # For å resette feilmeldingsteksten
    else:
        cntrl.frames[ReLogin].signuptext.set("Feil brukernavn/passord")


def lanseType(Type, jump, cntrl):#Used to change value of global variable, and change GUI window
    global lanse_type
    lanse_type = Type
    global placement

    with open(lanse_info, "w") as f:  # lagrer info til fil
        f.write(lanse_type)
        f.close()

    if Type == "Viking V2":
        csrf.serverSend("bronn" + str(placement), {'lanse_kategori':'VikingV2'})
        global serverDict
        serverDict['lanse_kategori'] = 'VikingV2'
    elif Type == "Snokanon TG3":
        csrf.serverSend("bronn" + str(placement), {'lanse_kategori':'TG3'})
        # global serverDict
        serverDict['lanse_kategori'] = 'TG3'

    cntrl.frames[Home].lanse_Type.set("Type: " + str(lanse_type))
    if jump == 1:
        cntrl.show_frame(PlacementPage)# Changes GUI window to PlacementPage
    else:
        cntrl.show_frame(Home)


def Place(place, cntrl):  #Used to change value of global variable, and change GUI window
    global placement
    placement = place

    with open(plass_info, "w") as f:  # lagrer info til fil
        f.write(str(placement))
        f.close()

    cntrl.frames[Home].lanse_plassering.set("Plassering: " + str(placement))
    cntrl.show_frame(Home)# Changes GUI window to Home


def FSSignup(cntrl, jump):  # Used to add a user to the GUI. So far only one user can be added.
    nameE = cntrl.frames[Signup].nameE.get()
    pwordE = cntrl.frames[Signup].pwordE.get()
    confirm_pwordE = cntrl.frames[Signup].confirm_pwordE.get()

    if jump == 1:
        cntrl.frames[Signup].clear_text()  # Tømmer inntastingsfelt
        cntrl.show_frame(Home)
    else:
        if (nameE == "") or (pwordE == "") or (confirm_pwordE == ""):
            print("Tomme felter")
            cntrl.frames[Signup].signuptext.set("Ingen felt kan stå tomme")
        elif (pwordE != confirm_pwordE):
            print("Ulike passordfelt")
            cntrl.frames[Signup].signuptext.set("Ulike passordfelt")
        else:
            with open(creds, 'w') as f:  # Creates a document using the variable we made at the top.
                f.write(
                    nameE)           #nameE is the variable we were storing the input to. app.frames[Signup].nameE.get()
                                           #Tkinter makes us use .get() to get the actual string.
                f.write('\n')  # Splits the line so both variables are on different lines.
                f.write(pwordE)  # Same as nameE just with pword var
                f.close()  # Closes the file
            cntrl.frames[Signup].signuptext.set("")  # For å resette feilmeldingsteksten
            cntrl.frames[Signup].clear_text()  # Tømmer inntastingsfelt
            cntrl.show_frame(Home)
            print("Bruker registrert \n Brukernavn:", nameE, "\n Passord   :", pwordE)


# Analoge avlesninger
def adcRead():  # Funksjon for avlesning av analoge innganger
    try:
        global sendDict
        while True:

            for i in range(4):
                if app.frames[MaalingPage].var2['variable' + str(i)].get() == True:
                    a = ADC.lesADC(i)
                    app.frames[MaalingPage].var3['variable' + str(i)].set(a)
                    print(app.frames[MaalingPage].var["variable" + str(i)].get())
                    if app.frames[MaalingPage].var["variable" + str(i)].get() == "Vanntrykk":
                        vanntrykk = round(((60/1023)* a), 2)
                        app.frames[MaalingPage].var3['variable' + str(i)].set(str(vanntrykk) + ' Bar')
                        sendDict['vanntrykk'] = float(vanntrykk)
                    elif app.frames[MaalingPage].var["variable" + str(i)].get() == "Lufttrykk":
                        lufttrykk = round(((16/1023)* a), 2)
                        app.frames[MaalingPage].var3['variable' + str(i)].set(str(lufttrykk) + ' Bar')
                        sendDict['lufttrykk'] = float(lufttrykk)
                    elif app.frames[MaalingPage].var["variable" + str(i)].get() == "Vannstrøm":
                        flow = round(((500/1023)* a), 2)
                        app.frames[MaalingPage].var3['variable' + str(i)].set(str(flow) + ' l/min')
                        sendDict['flow'] = float(flow)
                    elif app.frames[MaalingPage].var["variable" + str(i)].get() == "Vanntemp":
                        temperatur_vann = round(((100/1023)* a), 2) -50
                        app.frames[MaalingPage].var3['variable' + str(i)].set(str(temperatur_vann) + ' ºC')
                        sendDict['temperatur_vann'] = float(temperatur_vann)
                    #with open(analoge_maalinger, "r") as f:  # lagrer målinger
                    #    f.write(str(a))
                    #    f.close()
                else:
                    app.frames[MaalingPage].var3['variable' + str(i)].set("Ikke i bruk")

            time.sleep(1)
    except:
        print("Feil: ADC crash")


# Kommunikasjon med server
def sendTilServer(data):  # Funksjon for sending av data til server

    global serverDict
    for x in data:
        serverDict["lanse"][x] = data[x]

    csrf.serverSend('bronn'+str(placement), data)


def sendTilServerThreaded():
    global sendDict
    while True:
        try:
            if len(sendDict) > 0:
                sendTilServer(sendDict)
                sendDict = {}
            time.sleep(2)
        except:
            print('sendthreadfeil')
            time.sleep(1)


def hentFraServer():  # Funksjon for henting fra server, for threading

    global serverDict
    global placement

    while True:
        try:
            if placement == None:
                print("Do nothing")
            else:
                serverDictBuffer = csrf.serverHent("bronn" + str(placement))
                if serverDictBuffer == None:
                    print("Feil: Ugyldig serverdata")
                else:
                    serverDict = serverDictBuffer
                # print(serverDict)
            time.sleep(4)
        except:
            time.sleep(2)
            print('hentefeil')

def oppd_reg_steg(steg):
    global serverDict
    global sendDict
    if 'modus' in sendDict:
        if sendDict['modus'] != steg:
            sendDict['modus'] = steg
            serverDict["lanse"]['modus'] = steg
    else:
        if serverDict["lanse"]['modus'] != steg:
            sendDict['modus'] = steg
            serverDict["lanse"]['modus'] = steg


def Viking_V3_styring():  # Utkast  #fremdeles utkast
    while True:
        try:
            wb = -4
            if len(serverDict) == 0:                                    ###MIDLERTIDIG FIX (håper jeg, vi trenger en form for datahåndtering)
                raise reguleringsException('har ikke henta data fra server ')

            # Sleng in kode for WB-utregning? #fiksa, ligger nå lenger nede

            if serverDict["lanse"]['auto_man'] == 0:  # Sjekk om den er i auto eller manuell
                print("Stiller inn til ønsket manuelt steg")
                if serverDict["lanse"]['modus'] == 0:
                    relestyring.on_off(0,relestyring.Steg1)
                    relestyring.on_off(0,relestyring.Steg2)
                    relestyring.stengVann()
                else:
                    relestyring.startVann()
                    if serverDict["lanse"]['modus'] == 1:
                        relestyring.on_off(0,relestyring.Steg1)
                        relestyring.on_off(0,relestyring.Steg2)
                    elif serverDict["lanse"]['modus'] == 2:
                        relestyring.on_off(1,relestyring.Steg1)
                        relestyring.on_off(0,relestyring.Steg2)
                    elif serverDict["lanse"]['modus'] == 3:
                        relestyring.on_off(0,relestyring.Steg1)
                        relestyring.on_off(1,relestyring.Steg2)
                    elif serverDict["lanse"]['modus'] == 4:
                        relestyring.on_off(1,relestyring.Steg1)
                        relestyring.on_off(1,relestyring.Steg2)
        
            elif serverDict["lanse"]['auto_man'] == None:
                print("Feil: Står verken i auto eller man")
            else:
                if serverDict["verstasjon"]["wind"] >= 10:  # Sjekk om det er for sterk vind
                    print("For sterk vind, stopp produksjon")
                    # Sjekke om det er en endelanse, hvis det er det: ikke stopp men laveste steg?
                    if serverDict['lanse']['plassering_bronn'] == 19 or serverDict['lanse']['plassering_bronn'] == 27:
                         print('setter i laveste steg pga endelanse')
                         relestyring.on_off(0,relestyring.Steg1)
                         relestyring.on_off(0,relestyring.Steg2)
                         oppd_reg_steg(1)

                    else:
                        print('avslutter produksjon pga vind')
                        relestyring.on_off(0,relestyring.Steg1)
                        relestyring.on_off(0,relestyring.Steg2)
                        oppd_reg_steg(0)
                        
                        relestyring.stengVann()
                else:  # Styring i auto
                    wb = funksjoner.wetBulbMedAtmTrykk(serverDict['verstasjon']['hum'],serverDict['verstasjon']['temp_2'],serverDict['verstasjon']['press'])

                    if wb <= -9:
                        print("Perfekte forhold, høyeste steg")
                        relestyring.startVann()
                        relestyring.on_off(1,relestyring.Steg1)
                        relestyring.on_off(1,relestyring.Steg2)
                        oppd_reg_steg(4)

                    elif wb > -9 and wb <= -7:
                        print("Greie forhold, middels høyt steg") 
                        relestyring.startVann()
                        relestyring.on_off(0,relestyring.Steg1)
                        relestyring.on_off(1,relestyring.Steg2)
                        oppd_reg_steg(3)

                    elif wb > -7 and wb <= -5:
                        print("Greie forhold, middels lavt steg") 
                        relestyring.startVann()
                        relestyring.on_off(1,relestyring.Steg1)
                        relestyring.on_off(0,relestyring.Steg2)
                        oppd_reg_steg(2)

                    elif wb > -5 and wb <= -3:
                        print("Dårlige forhold, laveste steg")
                        relestyring.startVann()
                        relestyring.on_off(0,relestyring.Steg1)
                        relestyring.on_off(0,relestyring.Steg2)
                        oppd_reg_steg(1)

                    else:
                        print("Forferdelige forhold, stopper produksjon")
                        # Sjekke om det er en endelanse, hvis det er det: ikke stopp men laveste steg?
                        if serverDict['lanse']['plassering_bronn'] == 19 or serverDict['lanse']['plassering_bronn'] == 27:
                            print('setter i laveste steg pga endelanse')
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(1)

                        else:
                            print('avslutter produksjon')
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(0)
                            relestyring.stengVann()
            time.sleep(1)

        except reguleringsException:
            print('venter på data')
            time.sleep(2)

def Viking_V2_styring():
    hysterese = 0.5
    while True:
        try:
            if len(serverDict) == 0:    #ser om den har noen styreparametre
                raise reguleringsException('har ikke henta data fra server ')

            if serverDict["lanse"]['auto_man'] == None:   #feilsjekk
                print("Feil: Står verken i auto eller man")
            else:

                if serverDict["lanse"]['auto_man'] == 0:  # Sjekk om den er i auto eller manuell
                    print("Stiller inn til ønsket manuelt steg")
                    if serverDict["lanse"]['modus'] == 0:
                        relestyring.on_off(0,relestyring.Steg1)
                        relestyring.on_off(0,relestyring.Steg2)
                        relestyring.stengVann()
                    else:
                        relestyring.startVann()
                        if serverDict["lanse"]['modus'] == 1:   #steg 1
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                        elif serverDict["lanse"]['modus'] == 2: #steg 2
                            relestyring.on_off(1,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                        elif serverDict["lanse"]['modus'] == 3: #steg 3
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(1,relestyring.Steg2)
                        elif serverDict["lanse"]['modus'] == 4: #steg 4
                            relestyring.on_off(1,relestyring.Steg1)
                            relestyring.on_off(1,relestyring.Steg2)

                if serverDict["lanse"]['auto_man'] == 1:    #sjekker om lansen står i auto

                    if (serverDict["verstasjon"]["wind"] >= 10):  # Sjekk om det er for sterk vind
                            print("For sterk vind, stopp produksjon")
                            # Sjekke om det er en endelanse, hvis det er det: ikke stopp men sett i laveste steg
                            if serverDict['lanse']['plassering_bronn'] == 19 or serverDict['lanse']['plassering_bronn'] == 27:
                                 print('setter i laveste steg pga endelanse')
                                 relestyring.on_off(0,relestyring.Steg1)
                                 relestyring.on_off(0,relestyring.Steg2)
                                 oppd_reg_steg(1)

                            else:
                                print('avslutter produksjon pga vind')
                                relestyring.on_off(0,relestyring.Steg1)
                                relestyring.on_off(0,relestyring.Steg2)
                                oppd_reg_steg(0)
                        
                                relestyring.stengVann()

                    else:
                        #rekner ut wetbulb
                        wb = funksjoner.wetBulbMedAtmTrykk(serverDict['verstasjon']['hum'],serverDict['verstasjon']['temp_2'],serverDict['verstasjon']['press'])
                    
                        # 0 til 1
                        if (serverDict["lanse"]['modus'] == 0 and wb <= -3) :
                            print("Dårlige forhold, laveste steg")
                            relestyring.startVann()
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(1)
                        
                        # 1 til 0
                        if (serverDict["lanse"]['modus'] == 1 and wb >= (-3 + hysterese) ):
                            print('avslutter produksjon')
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(0)
                            relestyring.stengVann()

                        # 1 til 2
                        if (serverDict["lanse"]['modus'] == 1 and wb <= -5 ):
                            print("Greie forhold, middels lavt steg") 
                            relestyring.startVann()
                            relestyring.on_off(1,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(2)

                        # 2 til 1
                        if (serverDict["lanse"]['modus'] == 2 and wb >= (-5 + hysterese)):
                            print("Dårlige forhold, laveste steg")
                            relestyring.startVann()
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(1)

                        # 2 til 3
                        if (serverDict["lanse"]['modus'] == 2 and wb <= -7 ):
                            print("Greie forhold, middels høyt steg") 
                            relestyring.startVann()
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(1,relestyring.Steg2)
                            oppd_reg_steg(3)

                        # 3 til 2
                        if (serverDict["lanse"]['modus'] == 3 and wb >= (-7 + hysterese) ):
                            print("Greie forhold, middels lavt steg") 
                            relestyring.startVann()
                            relestyring.on_off(1,relestyring.Steg1)
                            relestyring.on_off(0,relestyring.Steg2)
                            oppd_reg_steg(2)

                        # 3 til 4
                        if (serverDict["lanse"]['modus'] == 3 and wb <= -9):
                            print("Perfekte forhold, høyeste steg")
                            relestyring.startVann()
                            relestyring.on_off(1,relestyring.Steg1)
                            relestyring.on_off(1,relestyring.Steg2)
                            oppd_reg_steg(4)

                        # 4 til 3
                        if (serverDict["lanse"]['modus'] == 4 and wb >= (-9 + hysterese)):
                            print("Greie forhold, middels høyt steg") 
                            relestyring.startVann()
                            relestyring.on_off(0,relestyring.Steg1)
                            relestyring.on_off(1,relestyring.Steg2)
                            oppd_reg_steg(3)



        except reguleringsException:
            print('venter på data')
            time.sleep(2)

        time.sleep(0.5)

# Exeption Classes------------------------------------------------------------------------------------------------------

class reguleringsException(Exception):
    pass

# Classes---------------------------------------------------------------------------------------------------------------
class AppGui(tk.Tk):  # Main GUI class (Dette er tydeligvis controller)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Snøstyring")  # Sets GUI title
        # tk.Tk.iconbitmap(self, default="standard_trondheim.ico")

        # self._geom="200x200+0+0"
        if rpi == 1:
            self.geometry("{0}x{1}+0+0".format((self.winfo_screenwidth() - 2), (self.winfo_screenheight() - 66)))  # For "fullscreen"

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)  # Define window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        toolbar = tk.Frame(self, bg="grey")

        homeButton = tk.Button(toolbar, text="Hjem", command=lambda: self.show_frame(Home))
        homeButton.pack(side=LEFT, padx=2, pady=2)
        lanseButton = tk.Button(toolbar, text="Lansetype", command=lambda: self.show_frame(SnTypePage2))
        lanseButton.pack(side=LEFT, padx=2, pady=2)
        placementButton = tk.Button(toolbar, text="Lanseplassering", command=lambda: self.show_frame(PlacementPage))
        placementButton.pack(side=LEFT, padx=2, pady=2)
        maalingButton = tk.Button(toolbar, text="Målinger", command=lambda: self.show_frame(MaalingPage))
        maalingButton.pack(side=LEFT, padx=2, pady=2)

        styringButton = tk.Button(toolbar, text="Styring", command=lambda: self.show_frame(StyringPage))
        styringButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side="bottom", fill=X)

        self.frames = {}


        for F in (Home, SnTypePage2, PlacementPage, MaalingPage, StyringPage):  # Includes all pages, old:(Signup, Login, SnTypePage, ReLogin,)

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)  # Starting page

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


'''
class Login(tk.Frame):  # Login page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.signuptext = tk.StringVar()  # Deklarerer variabel for feilmeldinger
        self.signuptext.set("")

        intruction = tk.Label(self, text='Innlogging\n')
        intruction.grid(sticky="E")

        nameL = tk.Label(self, text='Brukernavn: ')
        pwordL = tk.Label(self, text='Passord: ')
        melding = tk.Label(self, textvariable=self.signuptext, fg="red")  # Feilmeldinger
        nameL.grid(row=1, sticky="E")
        pwordL.grid(row=2, sticky="E")
        melding.grid(row=4, columnspan=2)

        nameEL = tk.Entry(self)
        pwordEL = tk.Entry(self, show='*')
        nameEL.grid(row=1, column=1)
        pwordEL.grid(row=2, column=1)

        loginB = tk.Button(self, text='Logg inn',
                              command=lambda: CheckLogin(controller,nameEL,pwordEL))
        loginB.grid(row=3, columnspan=2, sticky="E")


class ReLogin(tk.Frame):  # Login page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.signuptext = tk.StringVar()  # Deklarerer variabel for feilmeldinger
        self.signuptext.set("")

        intruction = tk.Label(self, text='Innlogging\n')
        intruction.grid(sticky="E")

        nameL = tk.Label(self, text='Brukernavn: ')
        pwordL = tk.Label(self, text='Passord: ')
        melding = tk.Label(self, textvariable=self.signuptext, fg="red")  # Feilmeldinger
        nameL.grid(row=1, sticky="W")
        pwordL.grid(row=2, sticky="W")
        melding.grid(row=4, columnspan=2)

        self.nameEL = tk.Entry(self)
        self.pwordEL = tk.Entry(self, show='*')
        self.nameEL.grid(row=1, column=1)
        self.pwordEL.grid(row=2, column=1)

        loginB = tk.Button(self, text='Logg inn',
                              command=lambda: CheckReLogin(controller))
        loginB.grid(columnspan=2, sticky="E")

    def clear_text(self):  # metode for å etterlate blanke entry-felt
        self.nameEL.delete(0, 'end')
        self.pwordEL.delete(0, "end")


class SnTypePage(tk.Frame):  # Snowgun type page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Hvilken type lanse er dette?", font=LARGE_FONT)
        label.grid(sticky="N")

        button0 = tk.Button(self, text="Ikke regulerbar",
                            command=lambda: lanseType("Ikke regulerbar", 1, controller))
        button0.grid(row=1, sticky="W")

        button1 = tk.Button(self, text="2-trinn",
                                command=lambda: lanseType("2-trinn", 1, controller))
        button1.grid(row=2, sticky="W")

        button2 = tk.Button(self, text="3-trinn",
                                command=lambda: lanseType("3-trinn", 1, controller))
        button2.grid(row=3,sticky="W")
'''

class SnTypePage2(tk.Frame): # Snowgun type page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Hvilken type lanse er dette?", font=LARGE_FONT)
        label.grid(sticky="N")

        button0 = tk.Button(self, text="Udefinert",
                            command=lambda:lanseType("Udefinert", 0, controller))
        button0.grid(row=1, sticky="W")

        button1 = tk.Button(self, text="Snökanon TG3",
                                command=lambda:[controller.frames[StyringPage].show_frame(tg3ManPage),
                                                lanseType("Snokanon TG3", 0, controller)])
        button1.grid(row=2, sticky="W")

        button2 = tk.Button(self, text="Viking V2",
                                command=lambda:[controller.frames[StyringPage].show_frame(vikingManPage),
                                                lanseType("Viking V2", 0, controller)])
        button2.grid(row=3,sticky="W")


'''
class Signup(tk.Frame): # Signup page
  
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.signuptext = tk.StringVar()  # Deklarerer variabel for feilmeldinger
        self.signuptext.set("")

        intruction = tk.Label(self, text="Skriv inn ny innloggingsinformasjon")
        intruction.grid(sticky="E", columnspan=2)

        nameL = tk.Label(self, text='Brukernavn: ')
        pwordL = tk.Label(self, text='Passord: ')
        confirm_pwordL = tk.Label(self, text='Gjenta passord: ')
        melding = tk.Label(self, textvariable=self.signuptext, fg="red")  # Feilmeldinger
        nameL.grid(row=1, sticky="E")
        pwordL.grid(row=2, sticky="E")
        confirm_pwordL.grid(row=3, sticky="E")
        melding.grid(row=5, columnspan=2)


        self.nameE = tk.Entry(self)
        self.pwordE = tk.Entry(self)
        self.confirm_pwordE = tk.Entry(self)
        self.nameE.grid(row=1, column=1)
        self.pwordE.grid(row=2, column=1)
        self.confirm_pwordE.grid(row=3, column=1)

        signupButton = tk.Button(self, text='Registrer', command=lambda: FSSignup(controller, 0))
        avbrytButton = tk.Button(self, text="Avbryt", command=lambda: FSSignup(controller, 1))
        signupButton.grid(row=4, column=0, sticky="E")
        avbrytButton.grid(row=4, column=1, sticky="E")

    def clear_text(self):  # metode for å etterlate blanke entry-felt
        self.nameE.delete(0, 'end')
        self.pwordE.delete(0, "end")
        self.confirm_pwordE.delete(0, "end")
'''

class PlacementPage(tk.Frame):  # This has to be cleaned up

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        toolbar = tk.Frame(self, bg="grey")

        label = tk.Label(self, text="Hvor er snølansen plassert?", font=LARGE_FONT)
        label.pack(side="bottom")

        h=4
        w=8

        button1 = tk.Button(toolbar,
                            text="9",
                            command=lambda: Place(9, controller),height = h, width = w)
        button1.grid(row=1,column = 1)

        button2 = tk.Button(toolbar, text="10",
                            command=lambda: Place(10, controller),height = h, width = w)
        button2.grid(row=1,column=2)
        button3 = tk.Button(toolbar, text="11",
                            command=lambda: Place(11, controller),height = h, width = w)
        button3.grid(row=1,column=3)

        button4 = tk.Button(toolbar, text="12",
                            command=lambda: Place(12, controller),height = h, width = w)
        button4.grid(row=1,column=4)
        button5 = tk.Button(toolbar, text="13",
                            command=lambda: Place(13, controller),height = h, width = w)
        button5.grid(row=1,column=5)

        button6 = tk.Button(toolbar, text="14",
                            command=lambda: Place(14, controller),height = h, width = w)
        button6.grid(row=2,column=1)
        button7 = tk.Button(toolbar, text="15",
                            command=lambda: Place(15, controller),height = h, width = w)
        button7.grid(row=2,column=2)

        button8 = tk.Button(toolbar, text="16",
                            command=lambda: Place(16, controller),height = h, width = w)
        button8.grid(row=2,column=3)
        button9 = tk.Button(toolbar, text="17",
                            command=lambda: Place(17, controller),height = h, width = w)
        button9.grid(row=2,column=4)

        button10 = tk.Button(toolbar, text="18",
                            command=lambda: Place(18, controller),height = h, width = w)
        button10.grid(row=2,column=5)
        button11 = tk.Button(toolbar, text="19",
                            command=lambda: Place(19, controller),height = h, width = w)
        button11.grid(row=3,column=1)

        button12 = tk.Button(toolbar, text="20",
                            command=lambda: Place(20, controller),height = h, width = w)
        button12.grid(row=3,column=2)
        button13 = tk.Button(toolbar, text="21",
                            command=lambda: Place(21, controller),height = h, width = w)
        button13.grid(row=3,column=3)

        button14 = tk.Button(toolbar, text="22",
                            command=lambda: Place(22, controller),height = h, width = w)
        button14.grid(row=3,column=4)
        button15 = tk.Button(toolbar, text="23",
                            command=lambda: Place(23, controller),height = h, width = w)
        button15.grid(row=3,column=5)

        button16 = tk.Button(toolbar, text="24",
                             command=lambda: Place(24, controller),height = h, width = w)
        button16.grid(row=4,column=1)
        button17 = tk.Button(toolbar, text="25",
                            command=lambda: Place(25, controller),height = h, width = w)
        button17.grid(row=4,column=2)

        button18 = tk.Button(toolbar, text="26",
                            command=lambda: Place(26, controller),height = h, width = w)
        button18.grid(row=4,column=3)

        button19 = tk.Button(toolbar, text="27",
                             command=lambda: Place(27, controller),height = h, width = w)
        button19.grid(row=4,column=4)

        toolbar.pack()


class MaalingPage(tk.Frame):  # Side for målinger

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        defVal = "Udefinert"
        self.aktiveMaalinger = tk.Label(self, text="Aktive målinger")
        self.typeMaaling = tk.Label(self, text="Type måling")
        self.maaltVerdi = tk.Label(self, text="Målt verdi")
        self.aktiveMaalinger.grid(row=0, column=0)
        self.typeMaaling.grid(row=0, column=1)
        self.maaltVerdi.grid(row=0, column=2)

        self.var = {}
        self.var2 = {}
        self.var3 = {}
        for x in range(4):
            self.var["variable{}".format(str(x))] = tk.StringVar()
            self.var["variable{}".format(str(x))].set(defVal)
            self.var2["variable{}".format(str(x))] = tk.BooleanVar()
            self.var3["variable{}".format(str(x))] = tk.StringVar()
            self.var3["variable{}".format(str(x))].set(defVal)



        for x in range(4):
            maalTyp = tk.OptionMenu(self, self.var["variable{}".format(str(x))],
                                     "Udefinert", "Vanntrykk", "Lufttrykk", "Vannstrøm", "Vanntemp")
            maalTyp.grid(row=(x+1), column=1)
            c = tk.Checkbutton(self, text="Analog inngang {}".format(str(x)),
                               variable=self.var2["variable{}".format(str(x))])
            c.grid(row=(x+1), column=0)
            labelq = tk.Label(self, textvariable=self.var3["variable{}".format(str(x))])
            labelq.grid(row=(x+1), column=2)
            #  app.frames[MaalingPage].var3['variable7'].set('gg')

    #def contUpdate(self,value,attr,element):
    #    setattr(attr,element,value)
    #    #delay
    #    contUpdate(self,value,attr,element)


class StyringPage(tk.Frame):  # Side for styring

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Auto/man
        autoButton = tk.Button(self, text="Auto", command=lambda: sendTilServer({'auto_man':1}))
        autoButton.pack(side=TOP, padx=2, pady=2)
        manButton = tk.Button(self, text="Man", command=lambda: sendTilServer({'auto_man':0}))
        manButton.pack(side=TOP, padx=2, pady=2)

        # For testing
        # byttButton = tk.Button(self, text="TG3", command=lambda: self.show_frame(tg3ManPage))
        # byttButton.pack(side="bottom", padx=2, pady=2)
        # battButton = tk.Button(self, text="VIKING", command=lambda: self.show_frame(vikingManPage))
        # battButton.pack(side="bottom", padx=2, pady=2)

        # Auto styring kommer an på lansevalg

        container = tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)  # Define window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (tg3ManPage, vikingManPage, Home):  # Home er her kun for debug

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # StyringPage.show_frame(self, vikingManPage)  # Starting page
        if lanse_type == "Viking V2":
            self.show_frame(vikingManPage)
        elif lanse_type == "Snokanon TG3":
            self.show_frame(tg3ManPage)
        else:
            self.show_frame(Home)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        # Hvis man, hvilket steg?


class vikingManPage(tk.Frame):  # Side for styring

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global serverDict

        steg0Button = tk.Button(self, text="Steg 0", command=lambda: sendTilServer({'modus':0}))
        steg0Button.pack(side=LEFT, padx=2, pady=2)
        steg1Button = tk.Button(self, text="Steg 1", command=lambda: sendTilServer({'modus':1}))
        steg1Button.pack(side=LEFT, padx=2, pady=2)
        steg2Button = tk.Button(self, text="Steg 2", command=lambda: sendTilServer({'modus':2}))
        steg2Button.pack(side=LEFT, padx=2, pady=2)
        steg3Button = tk.Button(self, text="Steg 3", command=lambda: sendTilServer({'modus':3}))
        steg3Button.pack(side=LEFT, padx=2, pady=2)
        steg4Button = tk.Button(self, text="Steg 4", command=lambda: sendTilServer({'modus':4}))
        steg4Button.pack(side=LEFT, padx=2, pady=2)


class tg3ManPage(tk.Frame):  # Side for styring

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        avButton = tk.Button(self, text="Av", command=lambda: sendTilServer({'modus':0}))
        avButton.pack(side=LEFT, padx=2, pady=2)
        paaButton = tk.Button(self, text="På", command=lambda: sendTilServer({'modus':1}))
        paaButton.pack(side=LEFT, padx=2, pady=2)


class Home(tk.Frame):  # Main page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.lanse_Type = tk.StringVar()
        self.lanse_plassering = tk.StringVar()

        '''
        self.serverHent = tk.StringVar()

        if rpi == 1:
            try:  # Testing
                csrf.serverCom("bronn2", 0, {"vtrykk":4})  # Oppdatere informasjon på database
                testData = csrf.serverCom("bronn2", 1, {})  # Hente informasjon fra database
                print("Brønn 2 har lanse " + testData["lansetype"]["lansetype"])  # Debug
                self.serverHent.set(testData["lansetype"]["lansetype"])  # Endre GUI basert på database
            except:
                print('Feil: mangler forbindelse til server (Home init)')
        '''

        with open(lanse_info, "r") as f:  # leser av lansetype
            s = f.read()
            f.close()

            if s == "":
                self.lanse_Type.set("Type: " + 'Ikke definert')  # Udefinert dersom lanse.temp er tom
            else:
                self.lanse_Type.set("Type: " + s)
                global lanse_type
                lanse_type = s

        with open(plass_info, "r") as f:  # leser av plassering
            s = f.read()
            f.close()

            if s == "":
                self.lanse_plassering.set("Plassering: " + 'Ikke definert')  # Udefinert dersom plass.temp er tom
            else:
                self.lanse_plassering.set("Plassering: " + s)
                global placement
                placement = s

        label = tk.Label(self, textvariable=self.lanse_Type, font=LARGE_FONT)
        label.grid(row=0)
        labe2 = tk.Label(self, textvariable=self.lanse_plassering, font=LARGE_FONT)
        labe2.grid(row=1)

        '''
        label3 = tk.Label(self, textvariable=self.serverHent, font=LARGE_FONT)
        label3.grid(row=3)
        '''


#"Main loop"------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    tSH = Thread(target=hentFraServer, daemon=True)
    tSH.start()

    app = AppGui()



    if rpi == 1:
        tREG = Thread(target=Viking_V2_styring, daemon=True)
        tREG.start()

        t = Thread(target=adcRead, daemon=True)  # Lager en thread for en spesifikk oppgave
        t.start()  # Starter threaden

        tSDS = Thread(target=sendTilServerThreaded, daemon=True)
        tSDS.start()

    app.mainloop()


