import argparse
import os
from tqdm import tqdm
from pydub import AudioSegment 
import configparser

class AudioTrimmer():
  def __init__(self, config):
    self.working_directory = config['working_directory']
    self.input = config['input']
    self.output = config['output']
  
  def read_audio(self):
    print("Reading files...")

    path = os.path.join(self.working_directory, self.input['directory'], self.input['sub_directory'], self.input['filename'])
    song = AudioSegment.from_file(path, format=self.input['filetype'])
    return song

  def trim_audio(self):
    if (self.output['type']=="single"):
      self.trim_single_audio()
    elif (self.output['type']=="multi"):
      self.trim_multi_audio()
    else:
      print("Invalid setting type, output type setting '" + self.output['type'] + "' is not supported.")

  def trim_single_audio(self):
    # Input: an audio file
    # Output: a trimmed audio file
    input_audio = self.read_audio()

    print("Trimming audio...")

    savedir = os.path.join(self.working_directory, self.output['directory'], self.output['sub_directory'])
    if (not os.path.exists(savedir)):
      os.makedirs(savedir)
    savepath = os.path.join(savedir, self.output['filename'])
    # Process input
    start_min, start_sec = [int(x) for x in self.output['start'].split(":")]
    start_time = ((start_min*60)+start_sec)*1000

    if (self.output['end']):
      end_min, end_sec = [int(x) for x in self.output['end'].split(":")]
      end_time = ((end_min*60)+end_sec)*1000

      # Process file
      output_song = input_audio[start_time:end_time]
    else:
      # Process file
      output_song = input_audio[start_time:]

    # Export file
    output_song.export(savepath, format=self.input['filetype'])
  
  def trim_multi_audio(self):
    # Input: an audio file
    # Output: multiple audio files extracted from the original one

    # ------ Process information ------ #
    input_audio = self.read_audio()
    info = self.process_trim_info()

    # ------ Process video ------ #
    print("Trimming audio...")
    savedir = os.path.join(self.working_directory, self.output['directory'], self.output['sub_directory'])
    if (not os.path.exists(savedir)):
      os.makedirs(savedir)
    pbar = tqdm(len(info))
    for i in range(len(info)):
      outname, start = info[i]
      
      savepath = os.path.join(savedir, outname) + ".mp3"
      if (i==len(info)-1):
        # Process input
        start_time = self.unpack_time(start)

        output_song = input_audio[start_time:]
        output_song.export(savepath, format=self.input['filetype'])
      else:
        end = info[i+1][1]
        # Process input
        start_time = self.unpack_time(start)
        end_time = self.unpack_time(end)
        
        output_song = input_audio[start_time:end_time]
        output_song.export(savepath, format=self.input['filetype'])
      
      print("Trim {}: {} - {} => DONE".format(outname, start_time, end_time))
      pbar.update(1)
      pbar.refresh()
    return

  def process_trim_info(self):
    # Input: directory (file location), file type (mp3), trim info (path to text file storing information of sub parts)
    # Output: a list storing information about each part:
    # - name: the output filename WITHOUT EXTENSION for this part (Ex: trim_part1)
    # - time: the start time of this part (Ex: 10:02)
    print("Processing information...")
    
    with open(os.path.join(self.working_directory, self.input['directory'], self.input['sub_directory'], self.input['trim_info']), encoding="utf8") as f:
      data = [x.replace('\n', '') for x in f.readlines()]
    info = []
    for x in data:
      x = x.split(" ")[1:]
      name = " ".join(x[:-1])
      time = x[-1]
      info.append([name, time])
    return info

  def unpack_time(self, str_time):
    try:
      # Process input
      split_time = str_time.split(":")
      if len(split_time) > 2:
        t_hour, t_min, t_sec = [int(x) for x in split_time]
        t_final = ((t_hour*60*60)+(t_min*60)+t_sec)*1000
      else:
        t_min, t_sec = [int(x) for x in split_time]
        t_final = ((t_min*60)+t_sec)*1000
      return t_final
    except:
      print("There was an error when unpacking time from provided trim info.")