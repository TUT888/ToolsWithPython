import os

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk

from utils.trim_audio.ui.trim_audio import *

SMALL_PADY = 3
SMALL_PADX = 3

FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 12, "bold")
FONT_TEXT = ("Arial", 10)
FONT_URL = ("Arial", 8, "italic underline")

URL_LIMIT_LENGTH = 30

class ToolApp:
  def __init__(self):
    # --- Init window & config information --- #
    self.window = Tk()
    self.trimmer = AudioTrimmer()
    
    # --- Window general layout --- #
    self.w_width = self.window.winfo_screenwidth()//2
    self.w_height = self.window.winfo_screenheight()//2
    self.window.title('Tools with Python')
    
    # --- Window sections (frames) --- #
    # Frame 1: Top frame
    self.top_frame = Frame(self.window,
                           width = self.w_width, height=self.w_height,
                           padx=SMALL_PADX, pady=SMALL_PADY)
    
    # Frame 2: Option frame
    self.option_frame = Frame(self.window,
                              width = self.w_width, height=self.w_height,
                              padx=SMALL_PADX, pady=SMALL_PADY)

    # Frame 2.1: Option frame - Input frame
    self.input_frame = Frame(self.option_frame,
                             width = self.w_width*0.4, height=self.w_height//2, 
                             padx=SMALL_PADX, pady=SMALL_PADY)
    self.input_frame.grid_propagate(0)
    
    
    # Frame 2.2: Option frame - Output frame
    self.output_frame = Frame(self.option_frame,
                             width = self.w_width*0.4, height=self.w_height//2, 
                             padx=SMALL_PADX, pady=SMALL_PADY)   
    self.output_frame.grid_propagate(0) 
    
    # Frame 3: Action frame
    self.action_frame = Frame(self.option_frame,
                             width = self.w_width//2, height=self.w_height, 
                             padx=SMALL_PADX, pady=SMALL_PADY*3)   
    
    # --- Allocate frame's location --- #
    self.top_frame.grid(row=0)
    self.option_frame.grid(row=1)
    self.action_frame.grid(row=2, columnspan=2, sticky=E)

    self.input_frame.grid(row=0, column=0, sticky=N)
    self.output_frame.grid(row=0, column=1, sticky=N)

    # --- Window elements/widgets --- #
    # Frame 1: Top frame
    self.lb_title = None

    self.init_top_frame()
    
    # Frame 2.1: Option frame - Input frame
    self.input_type = StringVar()
    self.input_file_path = StringVar()

    self.init_option_input_frame()  

    # Frame 2.2: Option frame - Output frame
    self.output_type = StringVar()
    self.output_filename = StringVar()
    self.output_filedir = StringVar()
    self.start_time = StringVar()
    self.end_time = StringVar()

    self.init_option_output_frame()

    # Frame 3: Action frame
    self.init_action_frame()


  # OK
  def init_top_frame(self):
    self.lb_title = Label(self.top_frame, text="Audio Trimmer",
                       font=FONT_TITLE)

    self.lb_title.grid(row=0, columnspan=4)

  def init_option_input_frame(self):
    # Input type
    lb_in_type = Label(self.input_frame, text="Input Type",
                       font=FONT_LABEL)
    rb_in_type1 = Radiobutton(self.input_frame, text="Single", 
                              variable=self.input_type, value="single", 
                              highlightthickness=0, font=FONT_TEXT,
                              command=lambda: self.show_input_option('single'))
    rb_in_type2 = Radiobutton(self.input_frame, text="Multi", 
                              variable=self.input_type, value="multi", 
                              highlightthickness=0, font=FONT_TEXT,
                              command=lambda: self.show_input_option('multi'))

    self.input_type.set("single")
    lb_in_type.grid(row=0,column=0, sticky=NW)
    rb_in_type1.grid(row=0, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)
    rb_in_type2.grid(row=1, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)

    # Details (based on selected input type)
    lb_select_file = Label(self.input_frame, text="Select input file", font=FONT_LABEL)
    lb_selected_file = Label(self.input_frame, text="./data/...", font=FONT_URL)
    btn_select_file = ttk.Button(self.input_frame, text="Browse", 
                                 command=lambda: self.ask_input_file_path(lb_selected_file))
    
    lb_select_file.grid(row=2, column=0)
    btn_select_file.grid(row=2, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)
    lb_selected_file.grid(row=3, columnspan=2, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)

  def init_option_output_frame(self):
    # Output type
    lb_out_type = Label(self.output_frame, text="Output Type",
                        font=FONT_LABEL)
    rb_out_type1 = Radiobutton(self.output_frame, text="Single", 
                               variable=self.output_type, value="single", 
                               highlightthickness=0, font=FONT_TEXT,
                               command=lambda: self.show_output_option('single'))
    rb_out_type2 = Radiobutton(self.output_frame, text="Multi", 
                               variable=self.output_type, value="multi", 
                               highlightthickness=0, font=FONT_TEXT,
                               command=lambda: self.show_output_option('multi'))

    self.output_type.set("single")
    lb_out_type.grid(row=0, column=0, sticky=NW)
    rb_out_type1.grid(row=0, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=W)
    rb_out_type2.grid(row=1, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=W)

    # Details (based on selected output type)
    lb_select_dir = Label(self.output_frame, text="Select sub directory", font=FONT_LABEL)
    lb_selected_dir = Label(self.output_frame, text="./data/...", font=FONT_URL)
    btn_select_dir = ttk.Button(self.output_frame, text="Browse", 
                                 command=lambda: self.ask_output_file_directory(lb_selected_dir))
    
    lb_out_filename = Label(self.output_frame, text="Output filename", font=FONT_LABEL)
    entry_out_filename = Entry(self.output_frame, textvariable=self.output_filename, font=FONT_TEXT)
    lb_start_time = Label(self.output_frame, text="Start time", font=FONT_LABEL)
    entry_start_time = Entry(self.output_frame, textvariable=self.start_time, font=FONT_TEXT)
    lb_end_time = Label(self.output_frame, text="End time", font=FONT_LABEL)
    entry_end_time = Entry(self.output_frame, textvariable=self.end_time, font=FONT_TEXT)

    lb_select_dir.grid(row=2, column=0)
    btn_select_dir.grid(row=2, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)
    lb_selected_dir.grid(row=3, columnspan=2, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)

    lb_out_filename.grid(row=4, column=0, pady=SMALL_PADY, sticky=NW)
    entry_out_filename.grid(row=4, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=W)
    lb_start_time.grid(row=5, column=0, pady=SMALL_PADY, sticky=NW)
    entry_start_time.grid(row=5, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=W)
    lb_end_time.grid(row=6, column=0, pady=SMALL_PADY, sticky=NW)
    entry_end_time.grid(row=6, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=W)
    
    # lb_select_dir.grid(row=5, column=0)
    # btn_select_dir.grid(row=5, column=1, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)
    # lb_selected_dir.grid(row=6, columnspan=2, padx=SMALL_PADX, pady=SMALL_PADY, sticky=NW)

  def init_action_frame(self):
    btn_convert = ttk.Button(self.action_frame, text="Convert", 
                             command=lambda: self.ask_confirm_convert())

    btn_convert.grid(row=0, columnspan=4)

  def show_input_option(self, input_type):
    if (input_type=='single'):
      print("Single input")
    elif (input_type=='multi'):
      print("Multi input")
    else:
      print('Invalid input type')
  
  def show_output_option(self, output_type):
    if (output_type=='single'):
      print("Single output")
    elif (output_type=='multi'):
      print("Multi output")
    else:
      print('Invalid output type')
    
  # OK
  def ask_input_file_path(self, display_path_label):
    root_path = self.trimmer.setting.get_data_path("root")
    data_path = self.trimmer.setting.get_data_path("absolute")
    data_path = data_path.replace("\\", "/")
    
    path = filedialog.askopenfilename(title="Select a File", 
                                      initialdir=data_path,
                                      filetype=(('MP3 files', '*.mp3'), 
                                                ('All files', '*.*')))
    path = path.replace(root_path, ".")
    self.input_file_path = path

    display_path = path
    if (len(display_path)>URL_LIMIT_LENGTH):
      display_path = display_path[:URL_LIMIT_LENGTH//2-2] + "..." + display_path[-URL_LIMIT_LENGTH//2-2:]
    display_path_label.config(text=display_path)

  def ask_output_file_directory(self, display_path_label):
    root_path = self.trimmer.setting.get_data_path("root")
    data_path = self.trimmer.setting.get_data_path("absolute")
    data_path = data_path.replace("\\", "/")

    path = filedialog.askdirectory(title="Select a Directory", 
                                   initialdir=data_path)
    path = path.replace(root_path, "")
    self.output_filedir = path

    display_path = path
    if (len(display_path)>URL_LIMIT_LENGTH):
      display_path = display_path[:URL_LIMIT_LENGTH//2-2] + "..." + display_path[-URL_LIMIT_LENGTH//2-2:]
    display_path_label.config(text=display_path)

  def ask_confirm_convert(self):
    # Input
    input_type = self.input_type.get()
    if (type(self.input_file_path)==str):
      input_file_path = self.input_file_path
    else:
      input_file_path = self.input_file_path.get()

    # Output
    output_type = self.output_type.get()
    output_filename = self.output_filename.get() 
    if (type(self.output_filedir)==str):
      output_filedir = self.output_filedir # subdir
    else:
      output_filedir = self.output_filedir.get()
    start_time = self.start_time.get()
    end_time = self.end_time.get()

    # Set data
    self.trimmer.update_input_info(input_file_path)
    self.trimmer.update_output_info(output_filename, start_time, end_time)
    self.trimmer.display_setting_info()

    # Message box
    response = messagebox.askyesno("Confirm", "Are you sure you want start the process with the given information?")
    if (response):
      res = self.trimmer.trim_audio()
      messagebox.showinfo("Result", res)

def main():
  app = ToolApp()
  app.window.mainloop()

if __name__ == "__main__":
  main()