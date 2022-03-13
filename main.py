from tkinter import *
import time
import numpy
import create_password
import check_password

THRESHOLD = 0.5

N_TRIALS = 10
UNFILLED = -1

ACCEPT = "qwertyuioplkjhgfdsazxcv bnm"

class App:

    def __init__(self, collecting=False):
        self.collecting = collecting
        self.test_count = 0
        self.name = ""
        if self.collecting:
            self.name = input("enter name: ")

        # set up window
        self.window = Tk()
        self.window.geometry("300x300")
        self.window.resizable(False, False)
        self.window.columnconfigure(0,weight=1)
        self.window.columnconfigure(1,weight=2)
        self.window.rowconfigure(0,weight=10)
        self.window.rowconfigure(1,weight=1)
        self.window.rowconfigure(2,weight=1)

        # set up output box
        self.output_txt = StringVar()
        self.output_txt.set("Welcome to P(you).")
        self.output = Label(
            self.window, textvariable=self.output_txt,
            bg='white', anchor="nw", height=8, width=6, justify=LEFT
        )
        self.output.grid(column=0, row=0, columnspan=2, sticky='nsew')

        # set up input box
        self.input_txt = StringVar()
        self.input = Entry(self.window, width=15, textvariable=self.input_txt)
        self.input.grid(column=0, row=1, columnspan=2, sticky='new', pady=5, padx=10)
        self.input.config(state="disabled")
        self.input.bind("<Key>", self.empty_func)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<KeyRelease>", self.empty_func)

        # set up buttons
        self.cancel_button = Button(self.window, text="Cancel", command=self.cancel)
        self.cancel_button.grid(column=0, row=2, columnspan=2, sticky='new', padx=3)
        self.cancel_button.grid_remove()
        self.new_pass_button = Button(self.window, text="Create New Password", command=self.create_password_button)
        self.new_pass_button.grid(column=0, row=2, sticky='new', padx=3)
        self.try_pass_button = Button(self.window, text="Try Password", command=self.try_password_button)
        self.try_pass_button.grid(column=1, row=2, sticky='new', padx=3)

    def empty_func(self, event):
        return

    def try_password_button(self):
        self.input.config(state='normal')
        self.output_txt.set("Please enter your password")
        self.input_txt.set("")
        self.new_pass_button.grid_remove()
        self.try_pass_button.grid_remove()
        self.cancel_button.grid()
        self.password = check_password.get_password()
        self.input.bind("<Key>", self.time_password_check)
        self.input.bind("<KeyRelease>", self.register_up)
        self.input.bind("<Return>", self.empty_func)
        self.key_count = 0
        self.times = []
        self.data = []
        self.time = time.time()
        self.map_key_to_ind = {}
        self.press_times = []
        self.hold_times = []
        for i in range(len(self.password)):
            self.hold_times.append(UNFILLED)

    def time_password_check(self, event):
        if event.char not in ACCEPT:
            self.output_txt.set("Invalid key, press enter to retry")
            self.input.bind("<Return>", self.restart_trying)
            self.input.bind("<Key>", self.empty_func)
            self.input.bind("<KeyRelease>", self.empty_func)
            self.input.config(state='disabled')
            return
        if event.char != self.password[self.key_count]:
            self.output_txt.set("Incorrect password, press enter to retry")
            self.input.bind("<Return>", self.restart_trying)
            self.input.bind("<Key>", self.empty_func)
            self.input.bind("<KeyRelease>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')
            return
        self.press_times.append(time.time())
        self.map_key_to_ind[event.char] = self.key_count
        self.key_count += 1
        if self.key_count >= 2:
            self.times.append((time.time()-self.time)*1000)
        self.time = time.time()
        if self.key_count == len(self.password):
            self.input.bind("<KeyRelease>", self.empty_func)
            for h in range(len(self.hold_times)):
                if self.hold_times[h] < 0:
                    self.hold_times[h] = 1000*(time.time()-self.press_times[h])
            for holder in self.hold_times[:-1]:
                self.times.append(holder)
            
            # if self.collecting:
            #    f = open(self.password+"_")

            prob_correct = check_password.check(self.times)

            if prob_correct > THRESHOLD:
                self.input.bind("<Return>", self.restart_trying)
                self.input.bind("<Key>", self.empty_func)
                self.input.bind("<KeyRelease>", self.empty_func)
                self.input_txt.set(self.input_txt.get()+event.char)
                self.input.config(state='disabled')
                self.output_txt.set("password correct \nprobability: "+ str(prob_correct)+"\npress enter to return to main menu")
                return
            print("probability below threshold: p =", prob_correct)
            self.output_txt.set("Incorrect password, press enter to retry")
            self.input.bind("<Return>", self.restart_trying)
            self.input.bind("<Key>", self.empty_func)
            self.input.bind("<KeyRelease>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')

    def restart_trying(self, event):
        self.input.config(state='normal')
        self.times = []
        self.time = time.time()
        self.key_count = 0
        self.output_txt.set("Please enter your password")
        self.input.delete(0, END)
        self.map_key_to_ind = {}
        self.press_times = []
        self.hold_times = []
        for i in range(len(self.password)):
            self.hold_times.append(UNFILLED)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_check)
        self.input.bind("<KeyRelease>", self.register_up)


    def enter_password_first(self, event):
        # entering password for first time
        self.password = self.input_txt.get().strip().lower()
        self.input_txt.set("")
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_create)
        self.input.bind("<KeyRelease>", self.register_up)
        self.count = 0
        self.key_count = 0
        self.times = []
        self.data = []
        self.map_key_to_ind = {}
        self.press_times = []
        self.hold_times = []
        for i in range(len(self.password)-1):
            self.hold_times.append(UNFILLED)
        self.time = time.time()
        self.output_txt.set("password: "+self.password+"\nplease enter password "+str(N_TRIALS)+" times \n0/"+str(N_TRIALS))
    
    def time_password_create(self, event):
        # timing password
        if event.char not in ACCEPT:
            # invalid character
            self.output_txt.set("Invalid key, press enter to retry")
            self.input.bind("<Return>", self.restart_timing)
            self.input.bind("<Key>", self.empty_func)
            self.input.bind("<KeyRelease>", self.empty_func)
            self.input.config(state='disabled')
            return
        if event.char != self.password[self.key_count]:
            # not right character
            self.output_txt.set("password: "+self.password+"\nplease enter password "+str(N_TRIALS)+" times \n"+str(self.count)+"/"+str(N_TRIALS)+"\npress enter to retry")
            self.input.bind("<Return>", self.restart_timing)
            self.input.bind("<Key>", self.empty_func)
            self.input.bind("<KeyRelease>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')
            return
        self.press_times.append(time.time())
        self.map_key_to_ind[event.char] = self.key_count
        self.key_count += 1
        if self.key_count >= 2:
            self.times.append((time.time()-self.time)*1000)
        self.time = time.time()
        if self.key_count == len(self.password):
            for h in range(len(self.hold_times)):
                if self.hold_times[h] < 0:
                    self.hold_times[h] = 1000*(time.time()-self.press_times[h])
            self.input.bind("<Return>", self.enter_time)
            self.input.bind("<Key>", self.empty_func)
            self.input.bind("<KeyRelease>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')
            self.output_txt.set("password: "+self.password+"\n please enter password "+str(N_TRIALS)+" times \n"+str(self.count)+"/"+str(N_TRIALS)+"\npress enter to continue")

    def register_up(self, event):
        if event.char in self.map_key_to_ind.keys():
            ind = self.map_key_to_ind[event.char]
            self.hold_times[ind] = 1000*(time.time()-self.press_times[ind])

    def restart_timing(self, event):
        self.input.config(state='normal')
        self.times = []
        self.time = time.time()
        self.key_count = 0
        self.output_txt.set("password: "+self.password+"\nplease enter password "+str(N_TRIALS)+" times \n"+str(self.count)+"/"+str(N_TRIALS))
        self.input.delete(0, END)
        self.map_key_to_ind = {}
        self.press_times = []
        self.hold_times = []
        for i in range(len(self.password)-1):
            self.hold_times.append(UNFILLED)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_create)
        self.input.bind("<KeyRelease>", self.register_up)
    
    def enter_time(self, event):
        self.input.config(state='normal')
        for holder in self.hold_times:
            self.times.append(holder)
        self.data.append(self.times)
        self.times = []
        self.count += 1
        self.map_key_to_ind = {}
        self.press_times = []
        self.hold_times = []
        for i in range(len(self.password)-1):
            self.hold_times.append(UNFILLED)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_create)
        self.input.bind("<KeyRelease>", self.register_up)
        self.input.delete(0, END)
        self.output_txt.set("password: "+self.password+"\nplease enter password "+str(N_TRIALS)+" times \n"+str(self.count)+"/"+str(N_TRIALS))
        self.key_count = 0
        if self.count == N_TRIALS:
            self.finish_create()

    def finish_create(self):
        self.output_txt.set("Input complete.\nProcessing...")
        self.window.update()
        create_password.create(self.password, self.data)
        self.output_txt.set("Password created! \npress enter to return to main menu")
        self.input.bind("<Return>", self.cancel_enter)
        self.input.bind("<Key>", self.empty_func)
        self.input.config(state='disabled')

    def create_password_button(self):
        # set state to entering new password
        self.input.config(state='normal')
        self.output_txt.set("Please enter new password")
        self.input_txt.set("")
        self.input.bind("<Key>", self.empty_func)
        self.input.bind("<Return>", self.enter_password_first)
        self.input.bind("<KeyRelease>", self.empty_func)
        self.new_pass_button.grid_remove()
        self.try_pass_button.grid_remove()
        self.cancel_button.grid()
        self.password = ""
    
    def cancel_enter(self, event):
        # back to main menu
        self.cancel()

    def cancel(self):
        # back to main menu
        self.input_txt.set("")
        self.input.config(state='disabled')
        self.input.bind("<Key>", self.empty_func)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<KeyRelease>", self.empty_func)
        self.cancel_button.grid_remove()
        self.new_pass_button.grid()
        self.try_pass_button.grid()
        self.output_txt.set("Welcome to passw0rd")

def main():
    app = App()
    app.window.mainloop()


if __name__=="__main__":
    main()