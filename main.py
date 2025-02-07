from trim_audio import AudioTrimmer
import configparser
import os

def read_config(config_file):
  # Set up config file
  config = configparser.ConfigParser()
  config.read(config_file, encoding="utf8")
  
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

  print("------ Confirm information ------")
  print("From {} input audio(s) to {} output audio(s)".format(info_dict['input']['type'], info_dict['output']['type']))
  
  # Read input data
  if (input_type=="single"):
    info_dict['input']['filetype'] = config['INPUT.SINGLE']['filetype']
    info_dict['input']['sub_directory']  = config['INPUT.SINGLE']['sub_directory']
    info_dict['input']['filename']  = config['INPUT.SINGLE']['filename']
    print("INPUT:")
    print("- File type: {}".format(info_dict['input']['filetype']))
    print("- File location: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['input']['directory'], 
      info_dict['input']['sub_directory'], 
      info_dict['input']['filename']))
    )
  else:
    return

  # Read output data
  print('OUTPUT')
  if (output_type=='single'):
    info_dict['output']['start'] = config['OUTPUT.SINGLE']['start']
    info_dict['output']['end'] = config['OUTPUT.SINGLE']['end']
    info_dict['output']['sub_directory'] = config['OUTPUT.SINGLE']['sub_directory']
    info_dict['output']['filename'] = config['OUTPUT.SINGLE']['filename']
    print("- Output file location: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['output']['directory'], 
      info_dict['output']['sub_directory'],
      info_dict['output']['filename']))
    )
    print("- Start time: {}".format(info_dict['output']['start']))
    print("- End time: {}".format(info_dict['output']['end']))
  elif (output_type=="multi"):
    info_dict['input']['trim_info'] = config['OUTPUT.MULTI']['trim_info']
    info_dict['output']['sub_directory'] = config['OUTPUT.MULTI']['sub_directory']
    print("- Trim info location: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['input']['directory'], 
      info_dict['input']['sub_directory'], 
      info_dict['input']['trim_info']))
    )
    print("- Output directory: {}".format(os.path.join(
      info_dict['working_directory'], 
      info_dict['output']['directory'], 
      info_dict['output']['sub_directory']))
    )
  else:
    print("Invalid output type, please check your setting type.")
    return None

  confirm = input("Confirm trimming process? (Y/n): ")
  if (confirm.lower()=='y'):
    return info_dict
  else:
    return None

def main():
  config_dict = read_config('config.ini')
  
  if (config_dict):
    audio_trimmer = AudioTrimmer(config_dict)
    audio_trimmer.trim_audio()
  else:
    print("Program closed.")

if __name__ == "__main__":
  main()