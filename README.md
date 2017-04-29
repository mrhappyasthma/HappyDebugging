# HappyDebugging

HappyDebugging is a set of LLDB macros to help make your iOS debugging a bit
more enjoyable.

(Note: This collection of scripts targets iOS. Many of them may work for MacOS,
but I don't do any testing on that so I make no guarantees.)

## Install

1. Download the scripts on your Mac. (Make note of the path where you saved
them.)
2. Open `~/.lldbinit` in your favorite text editor. (If it doesn't exist, make
the file first.)
3. Add the following command, substituting in the path for your local
`happy_debugging.py`:
    ```
    command script import /path/to/HappyDebugging/happy_debugging.py
    ```

## Command Glossary

| Command | Description                                       |
| ------- | ------------------------------------------------- |
| pv      | Prints out the current view hierarchy.            |
| pvc     | Prints out the current view controller hierarchy. |
