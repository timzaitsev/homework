from dicttoxml import dicttoxml
import json


def transform(filename):
    with open(filename) as file:
        data = file.read()
        name = filename.split('.')
        xml = open(name[0] + ".xml", "w")
        xml.write(str(dicttoxml(json.loads(data))))
        xml.close()


if __name__ == '__main__':

    transform(filename="books.json")

