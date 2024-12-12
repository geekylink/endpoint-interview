# Mock Directory System

This Python program simulates a simple in-memory directory system using Python dictionaries. The directories are not physically created on the filesystem; instead, they are represented and manipulated within a Python dictionary. This application supports creating, listing, moving, and deleting directories through a command-line interface.

## Features

- **Create Directories**: Simulate the creation of directories.
- **List Directories**: Recursively list all available directories in a structured format.
- **Move Directories**: Move directories from one location to another.
- **Delete Directories**: Remove directories from the directory tree.

## Commands

Below is a list of commands supported by the program:

- **CREATE `<directory-path>`**: Creates a new directory at the specified path. The path must be valid, and all parent directories must exist.

  *Example:* `CREATE fruits/apples`

- **LIST**: Displays all directories starting from the root in a formatted, hierarchical view.

  *Example:* `LIST`

- **MOVE `<source-path>` `<destination-path>`**: Moves a directory from the source path to the destination path. The destination can be an existing directory, in which case the source directory will become a subdirectory of the destination.

  *Example:* `MOVE fruits food` - This will move the entire `fruits` directory under `food`.

- **DELETE `<directory-path>`**: Deletes the specified directory. The directory must exist.

  *Example:* `DELETE fruits/apples`

## Running the Program

To run the program, execute the script through a Python interpreter.

My expectation is that you will likely be piping in the STDIN from an input file like so:

```bash
$ cat input | python directories.py
```

### Example input:
```plaintext
CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
MOVE grains food
LIST
```

### Output from example:
```plaintext
CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
fruits
  apples
    fuji
grains
vegetables
MOVE grains food
LIST
food
  grains
fruits
  apples
    fuji
vegetables
```

### You can also provide commands interactively via standard input:

```bash
$ python directories.py
CREATE example
CREATE example
CREATE test
CREATE test
MOVE example test
MOVE example test
LIST
LIST
test
  example
DELETE test/example
DELETE test/example
LIST
LIST
test
```

The program will continually accept input until an EOF (End-Of-File) signal is sent, which typically occurs when input is piped into the program or when a manual EOF trigger (like `Ctrl+D` in many terminals) is used.
