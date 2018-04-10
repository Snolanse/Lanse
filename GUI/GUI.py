# Imports---------------------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import LEFT, TOP, X, FLAT, RAISED
from threading import Thread
import time
# import RPi.GPIO as GPIO
import adc as ADC

# Global variables------------------------------------------------------------------------------------------------------

lanse_type = None
placement = None
creds = 'tempfile.temp' # Variable that becomes login data document
lanse_info = "lanse.temp"  # Lagret lansetype
plass_info = "plass.temp"  # Lagret plassering
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

    with open(lanse_info, "w") as f:  # lagrer info til fil
        f.write(lanse_type)
        f.close()

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


#Classes----------------------------------------------------------------------------------------------------------------
class AppGui(tk.Tk):  # Main GUI class (Dette er controller)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="standard_trondheim.ico")  # Sets GUI icon
        tk.Tk.wm_title(self, "Snøstyring")  # Sets GUI title

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)  # Define window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        toolbar = tk.Frame(self, bg="grey")

        homeButton = tk.Button(toolbar, text="Home", command=lambda: self.show_frame(Home))
        homeButton.pack(side=LEFT, padx=2, pady=2)
        lanseButton = tk.Button(toolbar, text="Lansetype", command=lambda: self.show_frame(SnTypePage2))
        lanseButton.pack(side=LEFT, padx=2, pady=2)
        placementButton = tk.Button(toolbar, text="Lanseplassering", command=lambda: self.show_frame(PlacementPage))
        placementButton.pack(side=LEFT, padx=2, pady=2)
        maalingButton = tk.Button(toolbar, text="Målinger", command=lambda: self.show_frame(MaalingPage))
        maalingButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)

        self.frames = {}


        for F in (Home, SnTypePage2, PlacementPage, MaalingPage):  # Includes all pages, old:(Signup, Login, SnTypePage, ReLogin)


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

        button0 = tk.Button(self, text="Ikke regulerbar",
                            command=lambda: lanseType("Ikke regulerbar", 0, controller))
        button0.grid(row=1, sticky="W")

        button1 = tk.Button(self, text="2-trinn",
                                command=lambda: lanseType("2-trinn", 0, controller))
        button1.grid(row=2, sticky="W")

        button2 = tk.Button(self, text="3-trinn",
                                command=lambda: lanseType("3-trinn", 0, controller))
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

        label = tk.Label(self, text="Hvor er lansa plassert?", font=LARGE_FONT)
        label.pack(side=TOP)

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

        toolbar.pack(side=LEFT)


class MaalingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        defVal = "one"
        # var2 = True

        self.var = {}
        self.var2 = {}
        self.var3 = {}
        for x in range(8):
            self.var["variable{}".format(str(x))] = tk.StringVar()
            self.var["variable{}".format(str(x))].set(defVal)
            self.var2["variable{}".format(str(x))] = tk.BooleanVar()
            self.var3["variable{}".format(str(x))] = tk.StringVar()
            self.var3["variable{}".format(str(x))].set(defVal)

        for x in range(8):
            maalTyp0 = tk.OptionMenu(self, self.var["variable{}".format(str(x))], "one", "two", "three")
            maalTyp0.grid(row=x, column=1)
            c = tk.Checkbutton(self, text="Analog inngang {}".format(str(x)), variable=self.var2["variable{}".format(str(x))])
            c.grid(row=x, column=0)
            labelq = tk.Label(self, textvariable=self.var3["variable{}".format(str(x))])
            labelq.grid(row=x, column=2)
            #     app.frames[MaalingPage].var3['variable7'].set('gg')

    def contUpdate(self,value,attr,element):
        setattr(attr,element,value)
        #delay
        contUpdate(self,value,attr,element)


class Home(tk.Frame):# Main page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.lanse_Type = tk.StringVar()
        self.lanse_plassering = tk.StringVar()

        with open(lanse_info, "r") as f:  # leser av lansetype
            s = f.read()
            f.close()

            if s == "":
                self.lanse_Type.set("Type: " + 'Ikke definert')  # Udefinert dersom lanse.temp er tom
            else:
                self.lanse_Type.set("Type: " + s)

        with open(plass_info, "r") as f:  # leser av plassering
            s = f.read()
            f.close()

            if s == "":
                self.lanse_plassering.set("Plassering: " + 'Ikke definert')  # Udefinert dersom plass.temp er tom
            else:
                self.lanse_plassering.set("Plassering: " + s)

        label = tk.Label(self, textvariable=self.lanse_Type, font=LARGE_FONT)
        label.grid(row=0)
        labe2 = tk.Label(self, textvariable=self.lanse_plassering, font=LARGE_FONT)
        labe2.grid(row=1)


def midl():
    count = 0
    while count < 100:
        count = count + 1
        v = ADC.lesADC(2)
        app.frames[MaalingPage].var3['variable2'].set(str(v))
        app.frames[MaalingPage].var3['variable7'].set(str(count))
        time.sleep(1)


#"Main loop"------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    app = AppGui()

    t = Thread(target=midl, daemon=True)  # Lager en thread for en spesifikk oppgave
    t.start()  # Starter threaden

    app.mainloop()


