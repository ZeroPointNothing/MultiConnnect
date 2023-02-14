import customtkinter as ctk
import json
import requests
import webbrowser

try:
    with open('current.json', 'r', encoding='utf-7') as f:
        version = json.load(f)["version"]
except FileNotFoundError:
    version = '???'


class App:
    def __init__(self, master: ctk.CTk) -> None:
        """
        Initializes all fields.
        """
        self.url = None
        self.command = None
        self.master = master
        ## -- WINDOW START
        self.master.geometry('850x600')
        self.master.resizable(False, False)
        self.master.wm_title(f'MUTLICONNECT INTERACTIVE GUI v{version}')
        ## -- WINDOW END

        self.toutput = ctk.CTkLabel(self.master, text='Output from host: NONE', wraplength=830)
        self.toutput.place(relx=0.5, rely=0.55, anchor='center')

        self.enurl = ctk.CTkEntry(self.master, placeholder_text='Enter MultiConnect URL', width=300)
        self.enurl.place(relx=0.5, rely=0.22, anchor='center')

        self.arg = ctk.CTkEntry(self.master,
                                placeholder_text='Enter arguements, if any in assignment form. ['
                                                 'message=, path=, etc.], seperated by &', width=490,
                                height=40)

        ## Self.runbutton's command arg must be without parenthesis or else it will not function
        ## after the first click.
        self.runbutton = ctk.CTkButton(self.master, text='CONNECT', command=self.conn, corner_radius=20)
        self.runbutton.place(relx=0.5, rely=0.44, anchor='center')

        self.cmd = ctk.CTkEntry(self.master, placeholder_text='Command to run. (WITHOUT SLASHES)', width=250)

    def conn(self):
        self.url = self.enurl.get()
        if 'http://' not in self.url:
            self.url = f'http://{self.url}'
        try:
            r = requests.get(self.url)
        except requests.exceptions.ConnectionError:
            print("Address is not valid.")
            return
        except requests.exceptions.InvalidURL:
            print("Address is not valid.")
            return

        if r.status_code == 404:
            print(404)
        elif r.json() == "Hello, world!":
            self.toutput.configure(text=f'Output from host: {r.json()}')
            self.enurl.destroy()
            self.runbutton.configure(command=self.run, text='RUN COMMAND')

            self.cmd.place(relx=0.5, rely=0.22, anchor='center')
            self.arg.place(relx=0.5, rely=0.33, anchor='center')
        else:
            print('Address is not a valid MultiConnect url.')
            return

    def run(self):
        self.command = f'/{self.cmd.get()}'
        if self.command == '/docs':
            print('To view /docs, visit it in your browser. It contains all available commands.')
            self.toutput.configure(text='Output from host: Check Console')
            return
        try:
            r = requests.get(self.url + self.command + f'?{self.arg.get()}')
        except requests.exceptions.JSONDecodeError:
            print('err. invalid argument?')
            return
        except requests.exceptions.ConnectionError:
            print("err. The host may no longer be online or you do not have permission to connect to it.")
            print("Try restarting either or both mcgui and MultiConnect and try again.")
            return

        try:
            self.toutput.configure(text=f'Output from host: {r.json()}')
        except requests.exceptions.JSONDecodeError:
            print('Data could not be displayed in GUI, attempting to open in browser...')
            webbrowser.open(self.url + self.command + f'?{self.arg.get()}')
            self.toutput.configure(text=f'Output from host: Opened in External Browser')

        print(f'ran: {self.command} with arguments: {self.arg.get()}')


if __name__ == '__main__':
    print("This console is intended for debbugging purposes, and to allow you to view any important events. Thus, "
          "it is tethered to the program. I recommend calling this from Command Prompt to allow you to see any "
          "exceptions that occur.")
    app = ctk.CTk()
    gui = App(master=app)
    app.mainloop()
