# Audio Trimmer

Audio Trimmer tool

## Table of Contents
1. Table of Contents [Go](#table-of-contents)
2. Run with Terminal [Go](#run-with-terminal)
3. Run with UI (Only support single -> single) [Go](#run-with-ui)

## Run With Terminal
### How to run
- Step 1: Create or edit the `config.ini` file. 
- Step 2: Run
  ```
  python main.py
  ```

### Configuration
Supported features
| Feature | Feature    | Status | Setting type |
| ------- | -------- | ------- | ------- |
| 1 | From single audio -> trimmed audio  | OK | single-single |
| 2 | From single audio -> multiple trimmed audios | OK | single-multi |
| 3 | Comming soon    | ...    | ... |

Global configuration for all features (`config.ini`):
[SETTING] section
- type: refer to the setting type for each features from the above table
- directory: the working directory where stores your data, including input files and output files

#### 1. Single to single
[INPUT.SINGLE] section: required information for all features extracting from **SINGLE INPUT** audio
- filetype: input audio file type (Currently only tested on mp3 files)
- filename: input audio file name. *Ex: myaudio.mp3*
- sub_directory (optional): a sub directory contains input audio file

[OUTPUT.SINGLE] section: required information for all features extracting audio(s) to **SINGLE OUTPUT** audio
- start: start time, format as hh:mm:ss. *Ex: 1:30*
- end: end time, format as hh:mm:ss. *Ex: 1:2:32*
- filename: output audio file name. *Ex: myaudio1.mp3*
- sub_directory (optional): a sub directory contains output audio file

#### 2. Single to multiple
[INPUT.SINGLE] section: required information for all features extracting from **SINGLE INPUT** audio
- filetype: input audio file type (Currently only tested on mp3 files)
- filename: input audio file name. *Ex: myaudio.mp3*
- sub_directory (optional): a sub directory contains input audio file

[OUTPUT.MULTI] section: required information for all features extracting audio(s) to **MULTILE OUTPUT** audio
- trim_info: the trim information stored in a text file. *Ex: VDTH_bgm_info.txt*

  Format:
  ```
  [Number.] [Output name] [start time]
  ```
  Example:
  ```
  1. 100%凌妙妙 (100% Ling Miaomiao) 00:00
  2. 100%凌妙妙 (100% Ling Miaomiao) 01:20
  ```
- sub_directory (optional): a sub directory contains output audio files

## Run With UI
### How to run
- Run the following command
  ```
  python ui.py
  ```
- Input the value and see the result (**the value must be the same format as written in config.ini**)