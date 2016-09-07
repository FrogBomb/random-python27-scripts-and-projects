from Tkinter import *

class tkSimpleWindow(Tk):
    def __init__(self, title = None):

        Tk.__init__(self)

        if title:
            self.title(title)

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

##        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
##                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.update_idletasks()

        self.apply()

    def cancel(self, event=None):

##        # put focus back to the parent window
##        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override


class DadCalculator(tkSimpleWindow):
    def body(self, master):
        Label(master, text="P_0").grid(row=0)
        Label(master, text="P_1").grid(row=1)
        Label(master, text="months").grid(row=2)
        Label(master, text="Annual % Change:").grid(row=3)

        self.P_0 = Entry(master)
        self.P_1 = Entry(master)
        self.months = Entry(master)
        self.output = Entry(master)
        self.output.config(state="readonly")

        self.P_0.grid(row=0, column=1)
        self.P_1.grid(row=1, column=1)
        self.months.grid(row=2, column=1)
        self.output.grid(row=3, column=1)
        
        
    def buttonbox(self):

        box = Frame(self)

        w = Button(box, text="Calculate", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Clear", width=10, command=self.clear)
        w.pack(side=LEFT, padx=5, pady=5)
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        self.bind("<Control-BackSpace>", self.clear)

        box.pack()
        
    def apply(self):
        try:
            result = 100*(((float(self.P_1.get())/float(self.P_0.get()))**(1/(float(self.months.get())/12.0)))-1)
        except ValueError:
            result = 0
        self.output.config(state=NORMAL)
        self.output.delete(0, END)
        self.output.insert(0, str(result))
        self.output.config(state="readonly")
        
    def clear(self, *args):
        self.P_0.delete(0, END)
        self.P_1.delete(0, END)
        self.months.delete(0, END)
        self.output.config(state=NORMAL)
        self.output.delete(0, END)
        self.output.config(state="readonly")

if __name__ == "__main__":
    d = DadCalculator()
    
