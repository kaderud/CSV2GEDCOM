# CSV2GEDCOM

_Create a GEDCOM file with data from **Geneaology ON DISPLAY** CSV file_

This project is based upon [xlsToGedcom](https://github.com/BodonFerenc/xlsToGedcom) by _**Ferenc Bodon**_

The purpose of this project is to convert the _**LISTPER**_ output (_PRINTPER.csv_ file) from [Geneaology ON DISPLAY](https://github.com/kaderud/Genealogy-ON-DISPLAY) into a GEDCOM file.


## CSV Format

The program _CSV2GEDCOM_ expects the CSV file adhere to the following header names (on one line, from left to right):
```
ID
Surname
Given Names
Sex
Father ID
Father Name
Mother ID
Mother Name
Birth Date
Birth City
Birth County
Birth State
Death Date
Death City
Death County
Death State
Burial Date
Burial City
Burial County
Burial State
```


## Configuration & Usage

Some small changes are needed before running the conversion program, edit ```CsvParser2Gedcom.py``` and make the following changes:

Edit the ```HEADER``` string and change ```DEST, LANG, SUBM1``` to reflect your destination program. The **SUBM1** is the Submitter person of the file to the destination geneaology program.
The ```convertDate(datum)``` function translates some Swedish month names to English, if the CSV file contains non-english month names, add them to this function.

Usage:

In the _**tools**_ directory, the program _**FormatCSV.py**_ (shell-script _**FormatPersons.sh**_) is used to clean up the CSV-file _PRINTPER.csv_ by removing leading and trailing whitespace and DOS's Ctrl-Z (EOF) marker.

```
ck@ws:~$ ./CSV2GEDCOM.sh persons.csv
```
or:
```
ck@ws:~$ python CSV2GEDCOM.py persons.csv > myfamily.ged
```
