
# Right now, we are storing directories as dictionaries.
# This is fine for simplicity, but on scaling the structure,
# we may encounter performance issues. For instance, using a more advanced
# data structure (such as defaultdict from the collections module) could 
# help simplify some code parts.
directories = {}

# Other note we should consider using a logging library instead of just
# printing for production, but for simplicity for this project we do not

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
            raise NotFoundException(f"{path[i]} does not exist")
        location = location[path[i]]

    return location

# Create a directory at the specified path
def createDirectory(fullPath):
    path = fullPath.split("/")
    try:
        location = traverseLocation(fullPath)
        if path[-1] not in location:
            location[path[-1]] = {} # Add a new directory
        else:
            print(f"{fullPath} already exists")
    except NotFoundException as e:
        print(f"Cannot create {fullPath} - {e.msg}")

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
        except KeyError:
            raise NotFoundException(f"{path[-1]} does not exist")
    except NotFoundException as e:
        print(f"Cannot delete {fullPath} - {e.msg}")

# Move a directory from one location to another
def moveDirectory(fullPathFrom, fullPathTo):
    pathFrom = fullPathFrom.split("/")
    pathTo = fullPathTo.split("/")

    try:
        sourceLocation = traverseLocation(fullPathFrom)
        directoryToMove = sourceLocation.pop(pathFrom[-1]) # Removes old location
    except NotFoundException as e:
        print(f"Cannot move {fullPathFrom} - {e.msg}")
        return
    except KeyError:
        print(f"Cannot move {fullPathFrom} - {pathFrom[-1]} does not exist")
        return

    try:
        destinationLocation = traverseLocation(fullPathTo)

        # Check if the destination directory already has an entry with that name
        # If not, create it
        if pathTo[-1] not in destinationLocation:
            destinationLocation[pathTo[-1]] = directoryToMove
        else:
            # Add the directory to its new location as a subdirectory
            destinationLocation[pathTo[-1]][pathFrom[-1]] = directoryToMove



    except NotFoundException as e:
        # Restore the directory if moving fails
        sourceLocation[pathFrom[-1]] = directoryToMove
        print(f"Cannot move to {fullPathTo} - {e.msg}")

# Parse and execute commands related to directory operations
def parseCommand(command):
    words = command.split(" ")
    match words[0]:
        case "CREATE":
            if len(words) != 2:
                print("CREATE command requires a path.")
            else:
                createDirectory(words[1])
        case "LIST":
            listDirectory(directories)
        case "MOVE":
            if len(words) != 3:
                print("MOVE command requires two paths: source and destination.")
            else:
                moveDirectory(words[1], words[2])
        case "DELETE":
            if len(words) != 2:
                print("DELETE command requires a path.")
            else:
                deleteDirectory(words[1])
        case _:
            print(f"{words[0]} command not found")

# Main loop
def main():
    while True:
        # Handle the EOF case to exit if input is provided on STDIN or CTRL+D
        try:
            command = input()
        except EOFError:
            return
        print(command)
        parseCommand(command)

if __name__ == "__main__":
    main()
