
def parseCell(cell, intMaximum):
    # The checks for a "valid cell" are done here as follows:
    #  - Is it actually an int?
    #  - Is it within range of 1 to col*rows?
    try:
        intCell = int(cell)
        if (intCell > 0) & (intCell < intMaximum):
            return intCell
        return False
    except:
        return False

def isValidMagicSquare(listSquare):
    intDiagTotal = 0
    intContraDiagTotal = 0
    intTotalRows = len(listSquare)
    # The first rows length will be our number of columns
    # All rows should equal this, as all cells for every column should be filled
    intTotalColumns = len(listSquare[0])

    # Ensure we actually have a square
    # This avoids fatal "list index out of range" errors later with invalid files
    if intTotalRows != intTotalColumns:
        print("Unequal number of rows/columns")
        return False

    # This is really just n ^ 2, but without importing any square method
    intMaximum = (intTotalColumns * intTotalRows) + 1

    # This is a very clever loop that may look deceivingly complex. It works as follows:
    # - Loop over each column index:
    #    - Loop over each row index:
    #        - Validate the next cell on the row and increment the total
    #        - Validate the next cell on the column and increment the total
    #    - Check if the current row's length is same as the first - quit early if so!
    #    - If the row/column totals don't match, we quit early here too
    #    - Otherwise, we can also grab the next cell on the diagonals,
    #      and increment those totals too
    #      Unfortunately we have to wait later to validate these as we must go over EVERY row/col
    # - Now validate ALL totals match. If there is a problem here, it must be related to the
    #   diagonal totals as we checked the rows and columns earlier
    for y in range(len(listSquare)):
        intRowTotal = 0
        intColumnTotal = 0
        if len(listSquare[y]) != intTotalColumns:
            print("Row "+str(y+1)+" has an incorrect length")
            return False
        for x in range(len(listSquare)):
            cellNextRow = listSquare[x][y]
            intNextRow = parseCell(cellNextRow, intMaximum)
            if intNextRow == False:
                print("Invalid cell '"+cellNextRow+"'")
                return False
            cellNextCol = listSquare[y][x]
            intNextCol = parseCell(cellNextCol, intMaximum)
            if intNextCol == False:
                print("Invalid cell '"+cellNextCol+"'")
                return False
            intRowTotal += intNextRow
            intColumnTotal += intNextCol
        if intRowTotal != intColumnTotal:
            print("There is a problem with your column / row totals")
            return False
        # We dont need to re-run parseCell here as all cells should be caught above
        intDiagTotal += int(listSquare[y][y])
        intContraDiagTotal += int(listSquare[len(listSquare)-y-1][y])
    if intRowTotal == intColumnTotal == intDiagTotal == intContraDiagTotal:
        return True
    print("There is a problem with your diagonal totals")
    return False

def hasDuplicates(readContents):
    # A simple way to duplicate check the values in the square
    # is to compare the length of the contents against a Set (which removes duplicates)
    listContents = readContents.split()
    return len(listContents) != len(set(listContents))

def writeFile(readContents, strFilename):
    fileOpen = open("VALID_"+strFilename, "w")
    fileOpen.write(readContents)
    fileOpen.close()

def parseFile(readContents):
    # We want to validate the square in as FEW iterations as possible
    # So we will parse the file contents into a matrix, where each nested list
    # contains the row's values
    # This will help us loop efficiently later
    listStringRows = readContents.splitlines()

    listListRows = []

    # We could do a map here as this is only one line per itt, but then we'd have to convert back to list
    # Would probably end up being more confusing to the next reader
    for row in listStringRows:
        listListRows.append(row.split())
    return listListRows

def readData():
    # While a valid file is NOT found, prompt the user to input a filename
    while True:
        try:
            strFileName = input("> ")
            io = open(strFileName, 'r')
            return [io, strFileName]
        except FileNotFoundError:
            print("'"+strFileName+"' not found")

if __name__ == "__main__":
    print("This program reads a text file and validates if the contents are a magic square\nEnter the filename below")
    # Pull out the file contents plus the filename we will be using later if valid
    # Firstly check for duplicates, if found we can quit before any iteration is needed
    # Then validate the file contents by iterating through the square
    # If successful we can write the VALID_ file
    # Otherwise, print and quit
    listReturn = readData()
    io = listReturn[0]
    strFilename = listReturn[1]
    readContents = io.read()
    io.close()

    bDuplicates = hasDuplicates(readContents)
    if bDuplicates:
        print("Square has duplicates")
        exit()

    listSquare = parseFile(readContents)
    bValid = isValidMagicSquare(listSquare)
    if bValid:
        print("Writing valid square")
        writeFile(readContents, strFilename)
    else:
        print("Square is not valid")
    exit()
