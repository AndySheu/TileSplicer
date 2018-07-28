import sys, os
from PIL import Image

def argumentInput():
    """
    Reads command line arguments.

    Returns:
        Tuple of tilesetFile, tileNamesFile, outputDirectory, tileSize, and tileSpacing if properly formatted; exits otherwise
    """
    if sys.argv == ['TileSplicer.py', 'help']:
        print('Command format:\n\tpython3 TileSplicer.py tilesetFile tileNamesFile outputDirectory tileSize tileSpacing')
        sys.exit(0)
    elif len(sys.argv) != 6: # First argument is script name
        print('Expected 5 arguments. Received', len(sys.argv)-1, 'argument(s):', str(sys.argv[1:])) # Ignore first argument
        sys.exit(0)
    tilesetFile, tileNamesFile, outputDir, tileSize, tileSpacing = sys.argv[1:] # Ignore first argument
    tileSize = checkInt('tileSize', tileSize)
    tileSpacing = checkInt('tileSpacing', tileSpacing)
    return (tilesetFile, tileNamesFile, outputDir, tileSize, tileSpacing)


def loadTileset(tilesetFile):
    """
    Loads the tileset.

    Args:
        tilesetFile: File name for the tileset image.

    Returns:
        Returns the image if found, null otherwise.
    """
    try:
        tileset = Image.open(tilesetFile)
        return tileset
    except IOError:
        print('Tileset', tilesetFile, 'not found!')
        sys.exit(0)

def loadTileNames(tileNamesFile):
    """
    Loads the names of tiles. Each name should be a single character long or space to skip an image.

    Args:
        tileNamesFile: File name for the tile names.

    Returns:
        Returns a matrix of names if found, null otherwise.
    """
    try:
        tileNamesReader = open(tileNamesFile)
        tileNames = []
        for line in tileNamesReader:
            tileNames.append(line)
        tileNamesReader.close()
        return tileNames
    except IOError:
        print('Tile Names', tileNameFile, ' not found!')
        sys.exit(0)

def makeDir(dirName):
    """
    Make a directory if it does not exist.

    Args:
        dirName: Directory name.
    """
    try:
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        else:
            print('Note: directory', dirName, 'already exists!')
    except OSError:
        print('Error making directory', dirName)
        sys.exit(0)

def spliceTileset(tileset, names, dirName, tileSize, tileSpacing):
    """
    Splices and saves tiles as a PNG.

    Args:
        tileset: Tileset Image.
        names: A matrix of tile names (list of lists).
        dirName: Name of the directory to save to.
        tileSize: Size of each tile in pixels.
        tileSpacing: Spacing between each tile.

    Returns:
        None
    """
    width, height = tileset.size
    upper = tileSpacing
    for row in names:
        left = tileSpacing
        for letter in row:
            if letter != ' ' and letter != '\n':
                if left+tileSize > width or upper+tileSize > height:
                    print(letter, 'is not in the tileset!')
                tile = tileset.crop((left, upper, left+tileSize, upper+tileSize)) # tuple
                tile.save(dirName + '/' + letter + '.png', 'PNG')
            left += tileSpacing + tileSize
        upper += tileSpacing + tileSize

def checkInt(varName, var):
    """
    Returns an integer cast of a variable. Outputs an error message if not an integer.

    Args:
        varName: Name of variable being checked.
        var: Variable to check.

    Returns:
        Integer cast of var.
    """
    try:
        return int(var)
    except ValueError:
        print(varName, 'must be an integer! Received:', var)
        sys.exit(0)

def main():
    """
    Runs the tile splicer.
    """
    tilesetFile, tileNamesFile, dirName, tileSize, tileSpacing = argumentInput()
    makeDir(dirName)
    tileset = loadTileset(tilesetFile)
    tileNames = loadTileNames(tileNamesFile)
    spliceTileset(tileset, tileNames, dirName, tileSize, tileSpacing)

main()
