import tkinter as tk
from tkinter import filedialog

class DatasetManager:

    def __init__(self, on_file_change=None) -> None:
        self.on_file_change = on_file_change
        self.used_ports = []
        self.app = tk.Tk()
        self.app.config(bg="white")
        self.app.title("Wordalizer")
        # self.app.minsize(640, 120)
        label = tk.Label(self.app, text="Select your database file:", font=("Calibari", 20), width=64, bg="white") \
            .grid(row=0, column=0, columnspan=10, padx=(10, 10), pady=(20, 20))
        self.lst_datasets = tk.Listbox(self.app, width=48)
        self.lst_datasets.grid(row=1, column=0, rowspan=9, columnspan=9, sticky='nwse', padx=(10,10), pady=(20,20))
        # self.lst_datasets.bind("<<ListboxSelect>>", self.change_contact)
        self.list_scrollbar = tk.Scrollbar(self.app)
        self.lst_datasets.config(yscrollcommand=self.list_scrollbar.set)
        self.list_scrollbar.config(command=self.lst_datasets.yview)

        btn_submit = tk.Button(self.app, text="Open", command=self.open_database, font=("Calibari", 14), width=16) \
            .grid(row=9, column=9 , padx=(10, 10), pady=(20, 20))


    def show(self):
        self.app.mainloop()

    def open_database(self):
        database_file = filedialog.askopenfile(mode='r')
        short_filename = database_file.name.split('\\')[-1] if '\\' in database_file.name else database_file.name.split('/')[-1]
        if self.on_file_change:
            port = 8000
            self.lst_datasets.insert(tk.END, f"{short_filename} @ {port}")
            self.on_file_change(database_file.name, port)
            self.used_ports.append(port)
        else:
            self.lst_datasets.insert(tk.END, f"{short_filename} @ ???")

        return database_file

if __name__ == '__main__':
    DatasetManager().show()
