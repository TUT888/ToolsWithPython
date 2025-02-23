from pydub import AudioSegment 

from utils.trim_audio.ui.setting import Setting

class AudioTrimmer():
  def __init__(self):
    self.setting = Setting()
  
  def update_input_info(self, filepath):
    self.setting.set_single_input(filepath)
  
  def update_output_info(self, filename, start, end):
    self.setting.set_single_output(filename, start, end)
  
  def display_setting_info(self):
    messages = [
      " Confirm information ",
      "TYPE: From {} input audio(s) to {} output audio(s)".format("single".upper(), "single".upper()),
    ]
    messages.append("INPUT:")
    messages.append("- File type: {}".format(self.setting.input.get_classname()))
    messages.append("- File location: {}".format(self.setting.input.get_input_path()))
    messages.append('OUTPUT')
    messages.append("- Output file location: {}".format(self.setting.output.get_save_path()))
    messages.append("- Start time: {}".format(self.setting.output.get_start_time()))
    messages.append("- End time: {}".format(self.setting.output.get_end_time()))
  
    # Print messages
    max_length = max([len(str_val) for str_val in messages])
    max_pad = max_length + 10
    print(messages[0].center(max_pad+4, '-'))
    for mess in messages[1:]:
      out_mess = "| " + mess.ljust(max_pad) + " |"
      print(out_mess)
    print("".center(max_pad+4, '-'))

  def read_audio(self):
    print("Reading files...")
    input_path = self.setting.input.get_input_path()
    song = AudioSegment.from_file(input_path, format=input_path.split('.')[-1])

    return song

  def trim_audio(self):
    print("HERE")
    output_type = self.setting.output.get_classname()
    if (output_type=="SingleOutput"):
      self.trim_single_audio()
      mes = "Done."
      print(mes)
      return mes
    elif (output_type=="MultiOutput"):
      self.trim_multi_audio()
      mes = "Done."
      print(mes)
      return mes
    else:
      mes = "Invalid setting type, output type setting '" + output_type + "' is not supported."
      print(mes)
      return mes

  def trim_single_audio(self):
    # Input: an audio file
    # Output: a trimmed audio file
    input_audio = self.read_audio()

    print("Trimming audio...")
    savepath = self.setting.output.get_save_path()
    start_as_str = self.setting.output.get_start_time()
    end_as_str = self.setting.output.get_end_time()
    # Process input
    start_time = self.convert_time_to_ms(start_as_str)
    end_time = self.convert_time_to_ms(end_as_str)

    if (end_time):
      output_song = input_audio[start_time:end_time]
    else:
      output_song = input_audio[start_time:]

    # Export file
    output_song.export(savepath, format=savepath.split('.')[-1])
  
  # unpack_time
  def convert_time_to_ms(self, str_time):
    try:
      if (str_time):
        # Process input
        split_time = str_time.split(":")
        if len(split_time) > 2:
          t_hour, t_min, t_sec = [int(x) for x in split_time]
          t_final = ((t_hour*60*60)+(t_min*60)+t_sec)*1000
        else:
          t_min, t_sec = [int(x) for x in split_time]
          t_final = ((t_min*60)+t_sec)*1000
        return t_final
      else: 
        # Return -1 if the input time is an empty string
        return -1
    except:
      print("There was an error when unpacking time from provided trim info.")