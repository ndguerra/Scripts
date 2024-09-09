# copied from internet
def function(file):
    lines = []
    for line in f:
        lines.append(line)
    return lines


with open('xc7z020clg484pkg.txt', 'r') as f: # open the file
    contents = function(f) # put the lines to a variable
    n = len(contents)
    Pin2Name = []
    for i in range(3,n-2): # only important lines
        line = contents[i].split()
        temp = [line[0], line[1]]
        Pin2Name.append(temp)
# Pin2Name is a 2xn array of the pin and pin name
# example [A19, IO_L10N_T1_AD11N_35]

with open('PacManV5_Trenz_Signals_Flat.csv', 'r') as f: #open the file
    contents = function(f) #put the lines to a variable.
    ThreeCols = []
    for i in range(len(contents)-1):
        line = contents[i+1].strip("\n")
        splitline = line.split(",")
        if len(splitline) >= 3:
            ThreeCols.append([splitline[0], splitline[2], splitline[1]])
# takes the file and puts only the important data in the order we need
# [Pin#, PacMan Signal, Trenz signal]
# example [JB1.35, TILE7_POSI0, B35_L10_N]


''' testing our example case
for i in range(len(ThreeCols)):
    if ThreeCols[i][0] == 'JB1.35':
        print(i) #17

test3 = ThreeCols[17]

for i in range(len(Pin2Name)):
    if Pin2Name[i][0] == 'A19':
        print(i) #191

test2 = Pin2Name[191]

print(test3)
print(test2)
print(Pin2Name)
'''



""" Making Checked.txt """

missing = []
FiveCols = [] # all important pins
NewThreeCols = [] # all not important pins
for i in range(len(ThreeCols)):
    name = ThreeCols[i][2] # gets the name e.g. B35_L10_N
    if name[0] != 'B': # if it doesn't start with B it is not important to us
        NewThreeCols.append(ThreeCols[i])
        continue
    name = name[1:] #removes the B
    splitname = name.split("_") # splits name up into 3 parts e.g. '35' 'L10' 'N'
    if len(splitname) == 3: # four have length 2
        splitname = [splitname[0],splitname[1]+splitname[2]] # this is how it appears in Pin2Name
    else:
        missing.append(ThreeCols[i]) # put them in new list we dont care about
        continue
    for j in range(len(Pin2Name)):
        bool1 = "_"+splitname[0] in Pin2Name[j][1] # true if bank number matches
        bool2 = splitname[1] in Pin2Name[j][1] # true if L number and N/P matches
        if bool1 and bool2: # if they both match put it in important list
            FiveCols.append([ThreeCols[i][0],ThreeCols[i][1],ThreeCols[i][2], Pin2Name[j][1], Pin2Name[j][0]])









'''
sum = 0
for j in range(len(ThreeCols)):
    Bool = False
    for i in range(len(FourCols)):
        if ThreeCols[j][0] == FourCols[i][0]:
            sum += 1
            Bool = True
    for i in range(len(NewThreeCols)):
        if ThreeCols[j][0] == NewThreeCols[i][0]:
            sum += 1
            Bool = True
    if not Bool:
        print(ThreeCols[j])
# ^checks to see if it is in important list or doesnt start with B

for i in range(len(ThreeCols)):
    Bool = False
    for j in range(len(FourCols)):
        if ThreeCols[i][0] == FourCols[i][0]:
            Bool = True
            break
    for j in range(len(NewThreeCols)):
        if ThreeCols[i][0] == NewThreeCols[i][0]:
            Bool = True
            break
    if not Bool:
        print(ThreeCols[i])
# ^same thing?



FILENAME = Output1 # whatever you want the filename to be
LIST = FourCols # whatever list you want to make into a file
list1 = []
for i in range(len(FourCols)):
    list1.append(' & '.join(FourCols[i]))

string1 = '\n'.join(list1)
string1 = string1.replace('_', '\_')

text_file = open(FILENAME, "w")
text_file.write(string1)
text_file.close()
# ^ outputs the list as a file

'''


""" Making Constraints File """

# vectorizes the Names
NAMES = []
for i in range(len(FiveCols)):
    PinNumber = FiveCols[i][4] # grabs pin e.g. A19
    TempName = FiveCols[i][1] # grabs PacMan singal e.g.  TILE7_POSI0
    # the following goes through every possible name that has to be changed
    if "PISO" in TempName:
        Tile = int(TempName[4:-6])-1 # gets Tile number (starting from 0) e.g. 7 goes to 6
        PSNumber = Tile * 4 + int(TempName[-1]) # gets the vectorization #
        Name = 'PISO[' + str(PSNumber) + ']'
    elif "POSI" in TempName: # same as above
        Tile = int(TempName[4:-6])-1
        PSNumber = Tile * 4 + int(TempName[-1])
        Name = 'POSI[' + str(PSNumber) + ']'
    elif "_SYNC" in TempName: # same as above
        number = int(TempName[4:-5]) - 1
        Name = "SYNC[" + str(number) + ']'
    elif "ENABLE" in TempName: # you get the idea
        number = int(TempName[4:-7])-1
        Name = "TILE_EN[" + str(number) + ']'
    elif "_TRIG" in TempName: # blah
        number = int(TempName[4:-5]) - 1
        Name = "TRIG[" + str(number) + ']'
    elif "ADC_D" in TempName: # blah
        number = int(TempName[5:])
        Name = "ADC_D["+str(number)+']'
    elif "TEST" in TempName: # blah
        number = int(TempName[-1])-1
        Name = "TEST_OUT["+str(number)+']'
    elif "(not used)" == TempName: # we ignore this one
        continue
    else: # for the ones we don't have to change
        Name = TempName
    NAMES.append([Name, PinNumber])
Names = sorted(NAMES)
# Now we have the vectorized name and Pin

SortingNames = [] # When in doubt make a new list
for i in range(len(Names)):
    Words = Names[i][0] # Takes the name e.g. 'PO'
    Letters = Words[:2] + Words[-3:] # Take the first 2 letters and last 3 numbers e.g.[0]
    x = Letters.replace('[','*') # * comes before 0 in the sort function
    SortingNames.append([x,Words,Names[i][1]]) # add element to list



SortedNames = sorted(SortingNames) # sort list


NewNames = [] # NEWLIST
for i in range(len(SortedNames)):
    NewNames.append([SortedNames[i][1], SortedNames[i][2]]) # just take the important stuff




# o
Constraints = []
for i in range(len(NewNames)):
    MAIN = f"set_property PACKAGE_PIN {NewNames[i][1]} [get_ports {NewNames[i][0]}]\n"
    Constraints.append(MAIN)
# ^puts Name and pin into properly formatted conts=raint file


string1 = ''.join(Constraints)
text_file = open("Output2.txt", "w")
text_file.write(string1)
text_file.close()
# turns it into a file