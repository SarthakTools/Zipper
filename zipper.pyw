from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showerror, showwarning
from tkinter import ttk
import customtkinter as ct
from PIL import Image, ImageTk
import cProfile, zipfile, time, threading, os
from showinfm import show_in_file_manager

tk_title = "Zipper" 

ct.set_widget_scaling(1.2)
root = ct.CTk(fg_color="white")
root.resizable(False, False)
root.geometry("780x500")
root.title(tk_title) 
root.iconbitmap("images\\zip.ico")

class LoadZipper:
    def __init__(self, root):
        self.root = root

        threading.Thread(target=self.get_gui).start()
        threading.Thread(target=self.load_data).start()

    def get_gui(self):
        self.loaded = False

        self.loading_frame = ct.CTkFrame(root, fg_color="white")
        self.loading_frame.pack(fill=BOTH, expand=True)

        zipper_src = Image.open("images\\zip.png")
        zipper_img = ImageTk.PhotoImage(zipper_src.resize((145, 145)))
        ct.CTkLabel(self.loading_frame, text=" Zipper", font=("Poppins", 60), image=zipper_img, compound=LEFT).pack(pady=100)       

        self.progressbar = ct.CTkProgressBar(self.loading_frame, orientation="horizontal", width=300, mode="indeterminate",
                                              indeterminate_speed=1.50,
                                              fg_color="white", height=4, progress_color="gray")
        self.progressbar.start()
        self.progressbar.place(x=200, y=230)

    def load_data(self):
        time.sleep(5)
        self.loaded = True
        self.hide_loading()
        UnZipper(self.root)

    def hide_loading(self):
        self.progressbar.stop()
        self.loading_frame.destroy()

    def destroy_loader(self):
        if not self.loaded:
            self.hide_loading()
        else:
            print("Loading already completed.")

class UnZipper:
    def __init__(self, root):
        self.root = root

        style = ttk.Style()
        style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children':
        [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
            [('Notebook.label', {'side': 'top', 'sticky': ''})], })], })])
        
        style.configure('TNotebook.Tab', font=('Poppins','14'), padding=(50, 10), background= "white")

        style.map("TNotebook.Tab", background= [("selected", "black")])
        style.configure("Tab", focuscolor=style.configure(".")["background"])

        global img
        img_src = Image.open("images\\home.png")
        img = ImageTk.PhotoImage(img_src.resize((29, 25)))

        global img2
        img_src2 = Image.open("images\\settings.png")
        img2 = ImageTk.PhotoImage(img_src2.resize((25, 25)))

        global img3
        img_src3 = Image.open("images\\close.png")
        img3 = ImageTk.PhotoImage(img_src3.resize((25, 25)))
        
        self.notebook = ttk.Notebook(root)

        self.home = ct.CTkFrame(self.notebook, fg_color="white", border_color="#f6f6f6", border_width=1, corner_radius=20, bg_color="white")

        self.from_frame = ct.CTkFrame(self.home, height=78, width=600)
        ct.CTkLabel(self.from_frame, text="Zipfile Location", font=("Poppins", 16)).place(x=10, y=5)

        global folder_icon
        folder_icon_src = Image.open("images\\folder_icon.png")
        folder_icon = ImageTk.PhotoImage(folder_icon_src.resize((25, 30)))

        self.from_file_entry = ct.CTkEntry(self.from_frame, width=460, border_width=0, font=("consolas", 15))
        self.from_file_entry.insert(0, "Click the browse button and select the zip file name")
        self.from_file_entry.configure(state="disabled")
        self.from_file_entry.place(x=10, y=35)

        self.from_browser_btn = ct.CTkButton(self.from_frame, text="Browse", width=100, image=folder_icon, compound=LEFT,\
             fg_color="#f6f6f6", text_color="black", hover_color="white", command=self.browse_file_from)
        self.from_browser_btn.place(x=480, y=35)

        self.success_btn = ct.CTkButton(self.home, text="Successfully extracted files", fg_color="#489938", text_color="white",
                                        font=("Verdana", 13), hover_color="#489938", height=38, width=230, image=img3,
                                          compound=RIGHT, cursor="hand2", command=self.instant_destory_success)
        self.from_frame.pack(side=TOP, pady=45)

        self.to_frame = ct.CTkFrame(self.home, height=78, width=600)
        ct.CTkLabel(self.to_frame, text="Extract file to", font=("Poppins", 16)).place(x=10, y=5)

        self.to_file_entry = ct.CTkEntry(self.to_frame, width=460, border_width=0, font=("consolas", 15))
        self.to_file_entry.insert(0, "Click the browse button and select the folder name")
        self.to_file_entry.configure(state="disabled")
        self.to_file_entry.place(x=10, y=35)

        self.to_browser_btn = ct.CTkButton(self.to_frame, text="Browse", width=100, image=folder_icon, compound=LEFT,\
         fg_color="#f6f6f6", text_color="black", hover_color="white", command=self.browse_file_to)
        self.to_browser_btn.place(x=480, y=35)

        self.to_frame.pack(side=TOP, pady=5)

        self.extract_btn = ct.CTkButton(self.home, text="Extract", text_color="white", command=self.extract_file, 
                                        state="normal", height=35, width=150)
        self.extract_btn.pack(side=TOP, pady=10)

        self.settings = ct.CTkFrame(self.notebook, fg_color="white")
        
        self.appearence_mode = ct.CTkFrame(self.settings, height=110)
        self.appearence_mode.pack(side=LEFT, anchor="ne", pady=20, ipadx=60, ipady=20, padx=20)
        self.radio_var = StringVar(value=0)
        ct.CTkLabel(self.appearence_mode, text="Appearance Mode", font=("Poppins", 16)).place(x=20, y=5)
        self.dark = ct.CTkRadioButton(self.appearence_mode, text="Dark", variable=self.radio_var, command=lambda: self.apply_window_style("dark")).place(x=20, y=40)
        self.acrylic = ct.CTkRadioButton(self.appearence_mode, text="Light", variable=self.radio_var, command=lambda: self.apply_window_style("light")).place(x=20, y=72)
        self.normal = ct.CTkRadioButton(self.appearence_mode, text="System", variable=self.radio_var, command=lambda: self.apply_window_style("system")).place(x=20, y=104)

        self.theme_mode = ct.CTkFrame(self.settings, height=135)
        self.theme_mode.pack(side=LEFT, anchor="nw", pady=20, ipadx=60, ipady=0, padx=20)
        self.check_var = StringVar(value=0)
        ct.CTkLabel(self.theme_mode, text="Theme", font=("Poppins", 20)).place(x=12, y=5)
        self.blue = ct.CTkRadioButton(self.theme_mode, text="Blue", variable=self.check_var, command=lambda: self.apply_theme("blue")).place(x=13, y=40)
        self.green = ct.CTkRadioButton(self.theme_mode, text="Green", variable=self.check_var, command=lambda: self.apply_theme("green")).place(x=13, y=70)
        self.dark_blue = ct.CTkRadioButton(self.theme_mode, text="Dark Blue", variable=self.check_var, command=lambda: self.apply_theme("dark-blue")).place(x=13, y=100)                                                                                     

        self.about = ct.CTkFrame(self.settings, height=50, width=350, bg_color="transparent", fg_color="white")

        ct.CTkLabel(self.about, text="About this app", font=("Poppins", 30)).place(x=15, y=5)
        self.text_box = ct.CTkTextbox(self.about, fg_color="white", height=50, width=350, bg_color="transparent", font=("consolas", 13))
        self.text_box.pack(fill=BOTH, expand=True)
        self.text_box.insert(1.0, "Zipper 1.0.1\n© 2023 Zipper Limited.All rights reserved.")
        self.text_box.configure(state="disabled")

        self.about.place(x=314, y=320)

        self.notebook.add(self.home, text=' Home', image=img, compound='left')
        self.notebook.add(self.settings, text=' Settings', image=img2, compound='left')

        self.notebook.pack(fill="both", expand=True)

        global zip_file_location, extract_folder_location
        zip_file_location = False
        extract_folder_location = False

    def apply_window_style(self, style):
        if style == "dark":
            self.home.configure(fg_color="black", bg_color="black", border_color="black")
            self.settings.configure(fg_color="black", bg_color="black", border_color="#333")
            self.from_browser_btn.configure(fg_color="#333", text_color="white", hover_color="#222")
            self.to_browser_btn.configure(fg_color="#333", text_color="white", hover_color="#222")
            self.text_box.configure(fg_color="black", text_color="white", bg_color="black")

        else:
            self.home.configure(fg_color="white", bg_color="white", border_color="#f6f6f6")
            self.settings.configure(fg_color="white", bg_color="white", border_color="#f6f6f6")
            self.from_browser_btn.configure(fg_color="#f6f6f6", text_color="black", hover_color="white")
            self.to_browser_btn.configure(fg_color="#f6f6f6", text_color="black", hover_color="white")
            self.text_box.configure(fg_color="white", text_color="black", bg_color="white")
            
        self.root.update_idletasks()
        ct.set_appearance_mode(style)
        self.root.update_idletasks()

    def apply_theme(self, theme):
        self.root.update_idletasks()
        ct.set_default_color_theme(theme)
        self.root.update_idletasks()

    def browse_file_from(self):
        self.from_file_name = askopenfilename(title="Open Zip File", filetypes=[("Zip files", "*.zip")])
        print(self.from_file_name)
        if self.from_file_name is not None:
            self.from_file_entry.configure(state="normal")
            self.from_file_entry.delete(0, END) 
            self.from_file_entry.insert(0, self.from_file_name)
            self.from_file_entry.configure(state="disabled")
            global zip_file_location, zip_file_name, base_zip_name

            base_zip_name = os.path.basename(self.from_file_name)
            zip_name = base_zip_name.split(".")
            zip_file_name = zip_name[0]
            print(zip_file_name)

            zip_file_name = self.from_file_name
            zip_file_location = self.from_file_name
        else:
            print("Can't insert zip file")
            self.from_file_entry.configure(state="normal")
            self.from_file_entry.delete(0, END)
            self.from_file_entry.insert(0, "Failed to insert zip file")
            self.from_file_entry.configure(state="disabled")

    def browse_file_to(self):
        self.to_file_name = askdirectory(title="Extract file to")
        print(self.to_file_name)
        if self.to_file_name is not None:
            self.to_file_entry.configure(state="normal")
            self.to_file_entry.delete(0, END) 
            self.to_file_entry.insert(0, self.to_file_name)
            self.to_file_entry.configure(state="disabled")
            global extract_folder_location
            extract_folder_location = self.to_file_name
        else:
            print("Can't insert zip file")
            self.to_file_entry.configure(state="normal")
            self.to_file_entry.delete(0, END)
            self.to_file_entry.insert(0, "Failed to insert zip file")
            self.to_file_entry.configure(state="disabled")

    def extract_file(self):
        global extract_folder_location

        try:
            print(extract_folder_location, zip_file_name)
            self.my_file_zip_name = os.path.basename(zip_file_name).split(".")[0]
            print(self.my_file_zip_name, " is the folder name")

            self.from_ = self.from_file_entry.get()
            self.to_ = self.to_file_entry.get()

            if self.from_ != None and self.from_ != "Click the browse button and select the zip file name":
                if self.to_ != None and self.to_ != "Click the browse button and select the folder name":
                    print(f"From : {self.from_}")
                    print(f"To : {self.to_}")
                    print(f"Mkdir : {extract_folder_location}/{self.my_file_zip_name}")

                    try:
                        os.makedirs(f"{extract_folder_location}/{self.my_file_zip_name}")

                        self.extract_to_folder = f"{self.to_}/{self.my_file_zip_name}"
                        print("Explorer ", self.extract_to_folder)
                        
                        with zipfile.ZipFile(self.from_) as zip:
                            zip.extractall(self.extract_to_folder)

                        self.success_btn.pack(side=BOTTOM, anchor="ne", pady=10, padx=10)

                        show_in_file_manager(self.extract_to_folder)

                    except:
                        showerror(title="Extract Folder Error", message="Sorry ! the folder already exists...")
                else:
                    print("Select a file to unzip")
            else:
                print("No such file location")
        except Exception as e:
            showwarning(title="Error", message="Please browse the files first")

    def instant_destory_success(self):
        self.success_btn.pack_forget()   
    
def start_application():
    loader = LoadZipper(root)
    root.after(0, loader.destroy_loader)

cProfile.run("start_application()")
cProfile.run("root.mainloop()")
