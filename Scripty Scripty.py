def function(file):
    lines = []
    for line in file:
        lines.append(line)
    return lines


with open('', 'r') as f: #open the file
    contents = function(f) #put the lines to a variable.
    NameAndDigits = []
    for i in range(len(contents)):
        line = contents[i].strip(" \t\n")
        splitline = line.split()
        if splitline[0] == 'constant':
            NameAndDigits.append([splitline[1], line [-4:-2]])


FILENAME = "Output" # whatever you want the filename to be
LIST = NameAndDigits # whatever list you want to make into a file
list1 = []
for element in LIST:
    list1.append('#define '+element[0]+'0x'+element[1])

string1 = '\n'.join(list1)

text_file = open(FILENAME, "w")
text_file.write(string1)
text_file.close()
# ^ outputs the list as a file


























