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

## Testing

The test environment requires an iOS app to be running on the simulator.
Therefore, the project includes `TestApp`, a folder containing a dummy
Xcode project that we can attach a debugger to for testing.

1. Open `TestApp/TestApp.xcodeproj` in Xcode.
2. Press `⌘ + R` to run the dummy app.
3. Wait until the simulator launches and runs the app.
4. Execute `./run_all_tests.py`.
5. Once you're done, you can close Xcode and the simulator.

## Command Glossary

| Command | Description                                       |
| ------- | ------------------------------------------------- |
| pv      | Prints out the current view hierarchy.            |
| pvc     | Prints out the current view controller hierarchy. |
| screenshot \<UIView\> | Saves a screenshot of the given `UIView` instance and opens it in Preview. Multiple calls will overwrite the temporary file, so save a local copy of the `.png` file if needed. |
