import argparse
import os
from tqdm import tqdm

from pydub import AudioSegment 

def edit_title():
  src_dir = os.path.join("data", "src")
  dst_dir = os.path.join("data", "result")
  cover_path = os.path.join("data", "cover.png")

  filenames = os.listdir(src_dir)
  pbar = tqdm(len(filenames))
  for fn in filenames:
    src_path = os.path.join(src_dir, fn)
    dst_path = os.path.join(dst_dir, fn)
    outname = fn.split(".")[0]

    src_audio = AudioSegment.from_file(src_path, format="mp3")
    src_audio.export(dst_path, format='mp3', 
                    #  tags={"title": outname},
                     cover=cover_path)
    pbar.update(1)
    pbar.refresh()

def edit_cover():
  src_dir = os.path.join("data", "src")
  dst_dir = os.path.join("data", "result")
  cover_path = os.path.join("data", "cover.png")

  filenames = os.listdir(src_dir)
  pbar = tqdm(len(filenames))
  for fn in filenames:
    src_path = os.path.join(src_dir, fn)
    dst_path = os.path.join(dst_dir, fn)

    src_audio = AudioSegment.from_file(src_path, format="mp3")
    src_audio.export(dst_path, format='mp3',
                     cover=cover_path)
    pbar.update(1)
    pbar.refresh()

def main():
  edit_cover()

if __name__ == "__main__":
  main()