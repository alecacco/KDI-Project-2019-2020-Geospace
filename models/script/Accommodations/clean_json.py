import os

path = os.path.join(os.path.expanduser('~'), 'hotels.json')
readFile = open(path, "r")
content = readFile.read().replace('\n][', ',')

writeFile = open(path, "w")
writeFile.write(content)
