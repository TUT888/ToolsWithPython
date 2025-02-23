from utils.trim_audio.terminal.trim_audio import AudioTrimmer
import configparser
import os

MODE_NAME = ["Quit", "Audio Trimmer"]

def read_config(config_file, mode=-1):
  # Set up config file
  config = configparser.ConfigParser()
  config.read(config_file, encoding="utf8")
  
  if (mode < 0 and mode >= len(MODE_NAME)):
    print("This tool is not supported.")
    return None
  
  print(f"Tool > {MODE_NAME[mode]}")
  if (mode==1):
    return read_audio_trimmer_config(config)
  return None
    
def read_audio_trimmer_config(config):
  input_type, output_type = config['SETTING']['type'].split("-")
  info_dict = { 
    'working_directory': config['SETTING']['directory'],
    'input': {
      'directory': 'input',
      'type': input_type
    },
    'output': {
      'directory': 'output',
      'type': output_type
    }
  }

  messages = [
    " Confirm information ",
    "TYPE: From {} input audio(s) to {} output audio(s)".format(info_dict['input']['type'].upper(), info_dict['output']['type'].upper()),
  ]
  
  # Read input data
  if (input_type=="single"):
    info_dict['input']['filetype'] = config['INPUT.SINGLE']['filetype']
    info_dict['input']['sub_directory']  = config['INPUT.SINGLE']['sub_directory']
    info_dict['input']['filename']  = config['INPUT.SINGLE']['filename']
    
    messages.append("INPUT:")
    messages.append("- File type: {}".format(info_dict['input']['filetype']))
    messages.append("- File location: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['input']['directory'], 
      info_dict['input']['sub_directory'], 
      info_dict['input']['filename']))
    )
  else:
    return None

  # Read output data
  messages.append('OUTPUT')
  if (output_type=='single'):
    info_dict['output']['start'] = config['OUTPUT.SINGLE']['start']
    info_dict['output']['end'] = config['OUTPUT.SINGLE']['end']
    info_dict['output']['sub_directory'] = config['OUTPUT.SINGLE']['sub_directory']
    info_dict['output']['filename'] = config['OUTPUT.SINGLE']['filename']

    messages.append("- Output file location: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['output']['directory'], 
      info_dict['output']['sub_directory'],
      info_dict['output']['filename']))
    )
    messages.append("- Start time: {}".format(info_dict['output']['start']))
    messages.append("- End time: {}".format(info_dict['output']['end']))
  elif (output_type=="multi"):
    info_dict['input']['trim_info'] = config['OUTPUT.MULTI']['trim_info']
    info_dict['output']['sub_directory'] = config['OUTPUT.MULTI']['sub_directory']

    messages.append("- Trim info location: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['input']['directory'], 
      info_dict['input']['sub_directory'], 
      info_dict['input']['trim_info']))
    )
    messages.append("- Output directory: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['output']['directory'], 
      info_dict['output']['sub_directory']))
    )
  else:
    print("Invalid output type, please check your setting type.")
    return None

  # Print messages
  max_length = max([len(str_val) for str_val in messages])
  max_pad = max_length + 10
  print(messages[0].center(max_pad+4, '-'))
  for mess in messages[1:]:
    out_mess = "| " + mess.ljust(max_pad) + " |"
    print(out_mess)
  print("".center(max_pad+4, '-'))

  confirm = input("Confirm trimming process? (Y/n): ")
  if (confirm.lower()=='y'):
    return info_dict
  else:
    return None

def select_option():
  print("--{:-^50}--".format(" Available tools "))
  print("| {:<50} |".format("1. Audio Trimmer"))
  print("| {:<50} |".format("0. Quit"))
  print("--{:-^50}--".format(""))
  mode = input("Enter the tool number you want to use: ")
  return mode
  
def main():
  mode = select_option()
  try:
    mode = int(mode)
    config_dict = read_config('./utils/trim_audio/terminal/config.ini', mode)
    if (config_dict):
      audio_trimmer = AudioTrimmer(config_dict)
      audio_trimmer.trim_audio()
    else:
      print("Program closed.")
  except:
    print("Input mode was invalid or there was an error occured, please try again later.")
    print("Program closed.")

if __name__ == "__main__":
  main()