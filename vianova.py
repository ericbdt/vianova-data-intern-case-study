import sqlite3
import csv

# First things first : let's create the database that we will fill thanks to the csv file
# This line will create the database the first time it is executed (if the database doesn't already exist) and afterwards it is used
# to connect to this data base

conn = sqlite3.connect('vianova.db')
curr = conn.cursor()


###### Starting from here, this whole section (until line 41 included) can be commented after the generation of the database


dropifexists = """ DROP TABLE IF EXISTS CITIES"""
curr.execute(dropifexists)

createTableCommand = """CREATE TABLE CITIES (
GeonameID INTEGER,
Name VARCHAR(50),
ASCIIName VARCHAR(50),
AlternateNames VARCHAR(256) NULL,
FeatureClass VARCHAR(1),
FeatureCode VARCHAR(5),
CountryCode VARCHAR(2),
CountryName_EN VARCHAR(38),
CountryCode2 VARCHAR(2) NULL,
Admin1Code VARCHAR(2),
Admin2Code VARCHAR(10) NULL,
Admin3Code VARCHAR(10) NULL,
Admin4Code VARCHAR(11) NULL,
Population INTEGER,
Elevation INTEGER NULL,
DigitalElevationModel INTEGER,
Timezone VARCHAR(30),
ModificationDate DATE,
LABEL_EN VARCHAR(50) NULL,
Coordinates VARCHAR(28)
);"""

curr.execute(createTableCommand)








# Now that the database is created let's fill it with the information stored in the csv file:
# I had to modify the csv for ambiguity reasons, as some alternative names of cities contained either ' or ". 
# I have decided to replace all the " by ' so that it is easier to deal with those alternative names


##### Starting from here, this whole section (until line 68 included) can be commented
##### until new csv files have to be integrated in the database

with open("geonames-all-cities-with-a-population-1000.csv") as file:
    cities = csv.reader(file, delimiter=';')

    i = 0
    for city in cities :
        if i > 0 :
            addData = f"""INSERT INTO CITIES VALUES ("{city[0]}", "{city[1]}", "{city[2]}","{city[3]}","{city[4]}","{city[5]}","{city[6]}","{city[7]}","{city[8]}","{city[9]}","{city[10]}","{city[11]}","{city[12]}","{city[13]}","{city[14]}","{city[15]}","{city[16]}","{city[17]}","{city[18]}","{city[19]}")"""
            curr.execute(addData)
        else :
            i+=1
conn.commit()









# Now that our database contains all the data from the csv file, we can query it
# Some information was missing from the csv file (for instance, there was no Country name for cities of Kosovo for instance, or independent/autonomous territories as Åland)
# So I had to insert them manually in the csv 

query = """SELECT CountryCode,CountryName_EN FROM CITIES 
WHERE CountryCode NOT IN
(SELECT CountryCode FROM CITIES WHERE Population >= 10000000 GROUP BY CountryCode)
GROUP BY CountryName_EN
ORDER BY CountryName_EN
"""

## This query search the countries that do not appear in the list of countries having at least one city of more than 10.000.000 inhabitants - or megapolis.

curr.execute(query)
answer = curr.fetchall()


##Now we want to export the results of this query into a tsv file :

exportfile = 'not_megapoliss_cities.tsv'

with open(exportfile, 'w', newline='') as exfile:
    writer = csv.writer(exfile, delimiter='\t')
    writer.writerows(answer)

print("Results exported as intended")