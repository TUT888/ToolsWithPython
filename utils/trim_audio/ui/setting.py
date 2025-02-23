import os

ROOT_PATH = os.getcwd().replace("\\", "/")

DATA_DIR = "data"
INPUT_DATA_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DATA_DIR = os.path.join(DATA_DIR, "output")

class Setting:
  def __init__(self):
    self.root_path = ROOT_PATH
    self.data_directory = DATA_DIR
    self.input = SingleInput()
    self.output = SingleOutput()
  
  def set_single_input(self, filepath):
    self.input.set_directory(INPUT_DATA_DIR)
    self.input.set_input_path(filepath) # should be verified to ensure it matches the directory above
  
  def set_single_output(self, filename, start, end):
    self.output.set_directory(OUTPUT_DATA_DIR)
    self.output.set_savename(filename)
    self.output.set_start_time(start)
    self.output.set_end_time(end)
  
  def get_data_path(self, opt=""):
    # Return relative path as default
    if (opt=="root"):
      return self.root_path
    elif (opt=="absolute"):
      return os.path.join(self.root_path, self.data_directory)
    else:
      return self.root_path
    

class FileInfo:
  def __init__(self):
    self.directory = ""

  # Setter
  def set_directory(self, directory):
    self.directory = directory
  
  # Getter
  def get_directory(self):
    return self.directory
  
  def get_classname(self):
      return type(self).__name__

class SingleInput(FileInfo):
  def __init__(self):
    self.input_path = ""
  
  # Setter
  def set_input_path(self, input_path):
    self.input_path = input_path

  # Getter
  def get_input_path(self):
    return self.input_path.replace("\\", "/")

class SingleOutput(FileInfo):
  def __init__(self):
    super().__init__()
    self.savename = ""
    self.start_time = ""
    self.end_time = ""
  
  # Setter
  def set_savename(self, savename):
    self.savename = savename
  
  def set_start_time(self, start_time):
    self.start_time = start_time

  def set_end_time(self, end_time):
    self.end_time = end_time
  
  # Getter
  def get_savename(self):
    return self.savename
  
  def get_start_time(self):
    return self.start_time
  
  def get_end_time(self):
    return self.end_time

  def get_save_path(self):
    return os.path.join(self.directory, self.savename).replace("\\", "/")