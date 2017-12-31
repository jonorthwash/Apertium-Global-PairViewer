"""
Python script used to filter out the pairs in pairs.json.txt that do not contain
languages with coordinates in the tsv file
"""

def filterPairs(filename, languages):
    pairFile = open(filename, "r")
    filtered = []
    count = 1
    for line in pairFile:
        line = line.strip().split()
        lang1 = line[3][1:4]
        lang2 = line[1][1:4]
        if lang1 in languages and lang2 in languages:
            #getting rid of last comma
            line[-1] = line[-1][:-1]
            joined = " ".join(line)
            filtered.append(joined)

    pairFile.close()
    return filtered

def getLanguagesWithCoords(filename):

    langFile = open(filename, "r")
    langDict = {}
    for line in langFile:
        line = line.strip().split(",")
        lat, lon = float(line[1]), float(line[2])
        langDict[line[0]] = [lon, lat]
    langFile.close()
    return langDict

if __name__ == "__main__":
    langDict = getLanguagesWithCoords("apertium-languages.tsv")
    filtered = filterPairs("pairs.json.txt", langDict)
    apertiumFile = open("apertiumPairs.json", "w")

    apertiumFile.write("{\n")
    apertiumFile.write('"type": "FeatureCollection",\n')
    apertiumFile.write('"pairs": [\n')
    for line in filtered:
        apertiumFile.write("\t"+line+"\n")
        apertiumFile.write(",\n")

    apertiumFile.write("]\n")
    apertiumFile.write("}")

    apertiumFile.close()

    apertiumFile2 = open("apertiumPoints.json", "w")
    apertiumFile2.write("{\n")
    apertiumFile2.write('"type": "FeatureCollection",\n')

    #writing point coordinates
    apertiumFile2.write('"point_data": [\n')
    for code, coords in langDict.items():
        string = '{"type": "Feature", "tag": "' + code + '", ' + '"geometry": { "type": "Point", ' + '"coordinates": ' + str(coords) + "} } \n"
        apertiumFile2.write("\t"+string)
        apertiumFile2.write(",\n")

    apertiumFile2.write("]\n")
    apertiumFile2.write("}")

    apertiumFile2.close()
