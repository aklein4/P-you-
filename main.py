from tkinter import *
import time
import numpy
import create_password

ACCEPT = "1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;'zxcvbnm,./<>?:"

class App:

    def __init__(self):
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
        self.output_txt.set("Welcome to passw0rd.")
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
        with open("data.txt") as f:
            lines = f.readlines()
        self.password = lines[0].strip()
        self.mus = lines[1].strip().split(',')
        self.stds = lines[1].strip().split(',')
        self.input.bind("<Key>", self.time_password_check)
        self.input.bind("<Return>", self.empty_func)
        self.key_count = 0
        self.times = []
        self.data = []
        self.time = time.time()

    def time_password_check(self, event):
        if event.char not in ACCEPT:
            self.output_txt.set("Invalid key, press enter to retry")
            self.input.bind("<Return>", self.restart_trying)
            self.input.bind("<Key>", self.empty_func)
            self.input.config(state='disabled')
            return
        if event.char != self.password[self.key_count]:
            self.output_txt.set("Incorrect password, press enter to retry")
            self.input.bind("<Return>", self.restart_trying)
            self.input.bind("<Key>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')
            return
        self.key_count += 1
        if self.key_count >= 2:
            self.times.append((time.time()-self.time)*1000)
            self.time = time.time()
        if self.key_count == len(self.password):
            with open("hack_data.txt") as f:
                lines = f.readlines()
            p_hackers = lines[0].strip().split(',')
            t_hackers = lines[1].strip().split(',')
            p_you = 1
            for h in range(len(p_hackers)):
                p_hackers[h] = float(p_hackers[h])
                t_hackers[h] = float(t_hackers[h])
                p_you -= p_hackers[h]
            p_not = 0
            for i in range(1,len(self.password)):
                p_you *= norm.pdf(float(self.times[i-1]), float(self.mus[i]), float(self.stds[i]))
            for j in range(len(p_hackers)):
                p_this = p_hackers[j]
                for i in range(1,len(self.password)):
                    p_this *= norm.pdf(t_hackers[j], float(self.mus[i]), float(self.stds[i]))
                p_not += p_this
            prob_correct = p_you/(p_you+p_not)

            if prob_correct > THRESHOLD:
                self.input.bind("<Return>", self.cancel_enter)
                self.input.bind("<Key>", self.empty_func)
                self.input_txt.set(self.input_txt.get()+event.char)
                self.input.config(state='disabled')
                self.output_txt.set("password correct \n probability: "+ str(prob_correct)+"\n press enter to return to main menu")
                return
            print("probability below threshold: p =", prob_correct)
            self.output_txt.set("Incorrect password, press enter to retry")
            self.input.bind("<Return>", self.restart_trying)
            self.input.bind("<Key>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')

    def restart_trying(self, event):
        self.input.config(state='normal')
        self.times = []
        self.time = time.time()
        self.key_count = 0
        self.output_txt.set("Please enter your password")
        self.input.delete(0, END)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_check)

    def enter_password_first(self, event):
        self.password = self.input_txt.get().strip().lower()
        self.input_txt.set("")
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_create)
        self.count = 0
        self.key_count = 0
        self.times = []
        self.data = []
        self.time = time.time()
        self.output_txt.set("password: "+self.password+"\n please enter password 10 times \n 0/10")
    
    def time_password_create(self, event):
        if event.char not in ACCEPT:
            self.output_txt.set("Invalid key, press enter to retry")
            self.input.bind("<Return>", self.restart_timing)
            self.input.bind("<Key>", self.empty_func)
            self.input.config(state='disabled')
            return
        if event.char != self.password[self.key_count]:
            self.output_txt.set("password: "+self.password+"\n please enter password 10 times \n"+str(self.count)+"/10 \n press enter to retry")
            self.input.bind("<Return>", self.restart_timing)
            self.input.bind("<Key>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')
            return
        self.key_count += 1
        if self.key_count >= 2:
            self.times.append((time.time()-self.time)*1000)
            self.time = time.time()
        if self.key_count == len(self.password):
            self.input.bind("<Return>", self.enter_time)
            self.input.bind("<Key>", self.empty_func)
            self.input_txt.set(self.input_txt.get()+event.char)
            self.input.config(state='disabled')
            self.output_txt.set("password: "+self.password+"\n please enter password 10 times \n"+str(self.count)+"/10 \n press enter to continue")

    def restart_timing(self, event):
        self.input.config(state='normal')
        self.times = []
        self.time = time.time()
        self.key_count = 0
        self.output_txt.set("password: "+self.password+"\n please enter password 10 times \n"+str(self.count)+"/10")
        self.input.delete(0, END)
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_create)
    
    def enter_time(self, event):
        self.input.config(state='normal')
        self.data.append(self.times)
        self.times = []
        self.count += 1
        self.input.bind("<Return>", self.empty_func)
        self.input.bind("<Key>", self.time_password_create)
        self.input.delete(0, END)
        self.output_txt.set("password: "+self.password+"\n please enter password 10 times \n"+str(self.count)+"/10")
        self.key_count = 0
        if self.count == 10:
            self.finish_create()

    def finish_create(self):
        
        self.output_txt.set("Password created! \n press enter to return to main menu")
        self.input.bind("<Return>", self.cancel_enter)
        self.input.bind("<Key>", self.empty_func)
        self.input.config(state='disabled')

    def create_password_button(self):
        self.input.config(state='normal')
        self.output_txt.set("Please enter new password")
        self.input_txt.set("")
        self.input.bind("<Key>", self.empty_func)
        self.input.bind("<Return>", self.enter_password_first)
        self.new_pass_button.grid_remove()
        self.try_pass_button.grid_remove()
        self.cancel_button.grid()
        self.password = ""
    
    def cancel_enter(self, event):
        self.cancel()

    def cancel(self):
        self.input_txt.set("")
        self.input.config(state='disabled')
        self.input.bind("<Key>", self.empty_func)
        self.input.bind("<Return>", self.empty_func)
        self.cancel_button.grid_remove()
        self.new_pass_button.grid()
        self.try_pass_button.grid()
        self.output_txt.set("Welcome to passw0rd")

def main():
    app = App()
    app.window.mainloop()


if __name__=="__main__":
    main()