
directories = {}

# Custom exception for handling cases where directories are not found
class NotFoundException(Exception):
    def __init__(self,msg):
        self.msg=msg

# Helper function to navigate to a specific location in the directory structure
def traverseLocation(fullPath):
    path = fullPath.split("/")
    location = directories
    # Traverse each component of the path except the last one
    for i in range(len(path)-1):
        if path[i] not in location:
            raise NotFoundException(path[i] + " does not exist")
        location = location[path[i]]

    return location

# Create a directory at the specified path
def createDirectory(fullPath):
    path = fullPath.split("/")
    location = traverseLocation(fullPath)
    location[path[-1]] = {} # Add a new directory

# List all directories recursively starting from a given location
def listDirectory(location, depth=0):
    keys = list(location.keys())
    keys.sort() # Ensure alphabetical order

    for directory in keys:
        print(" "*(depth*2) + directory)
        listDirectory(location[directory], depth+1)

# Delete a directory at a specified path
def deleteDirectory(fullPath):
    path = fullPath.split("/")
    try:
        location = traverseLocation(fullPath)
        try:
            # Remove the directory
            location.pop(path[-1])
        except:
            raise NotFoundException(path[-1] + " does not exist")
    except NotFoundException as e:
        print("Cannot delete " + fullPath + " - " + e.msg)

# Move a directory from one location to another
def moveDirectory(fullPathFrom, fullPathTo):
    pathFrom = fullPathFrom.split("/")
    pathTo = fullPathTo.split("/")

    # Traverse to the source and destination locations
    sourceLocation = traverseLocation(fullPathFrom)
    destinationLocation = traverseLocation(fullPathTo)

    directoryToMove = sourceLocation.pop(pathFrom[-1]) # Removes old location

    # Check if the destination directory already has an entry with that name
    # If not, create it
    if pathTo[-1] not in destinationLocation:
        destinationLocation[pathTo[-1]] = {}

    # Add the directory to its new location as a subdirectory
    destinationLocation[pathTo[-1]][pathFrom[-1]] = directoryToMove

# Parse and execute commands related to directory operations
def parseCommand(command):
    words = command.split(" ")
    match words[0]:
        case "CREATE":
            createDirectory(words[1])
        case "LIST":
            listDirectory(directories)
        case "MOVE":
            moveDirectory(words[1], words[2])
        case "DELETE":
            deleteDirectory(words[1])

# Main loop
def main():
    while True:
        # Handle the EOF case to exit if input is provided on STDIN
        try:
            command = input()
        except EOFError:
            return
        print(command)
        parseCommand(command)

if __name__ == "__main__":
    main()
