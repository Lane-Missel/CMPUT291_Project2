import sys
import json
import os
from pymongo import MongoClient
# get file

# mongo db with port number

def main():
    args = sys.argv[1:]
    path = args[0]
    port = None
    client = None
    collection = None
    DATABASENAME = "291db"
    COLLECTIONNAME = "dblp"
    datafile = None
    IMPORTSTRING = 'mongoimport --drop --quiet --db={} --collection={} --uri="mongodb://localhost:{}" --file="{}"'
    
    try:
        port = int(args[1])
        client = MongoClient(host="localhost", port=port)
    except ValueError:
        print("Invalid argument entered for port number. Exiting...")
        exit()

    except Exception:
        print("Error connecting to database. Exiting...")
        exit()

    # check if file exists...

    try:
        os.system(IMPORTSTRING.format(DATABASENAME, COLLECTIONNAME, port, path))
    except Exception:
        print("Fatal error while trying to import data. Exiting...")
        exit()

    print("Data from {} loaded into database located at port {}.".format(path, port))

if __name__ == "__main__":
    main()