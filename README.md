# HiveCSVParser
A simple CSV parser written in Python used to convert files to a format that can be used by Apache Hive.

## Command line options

| Option        | Description           | Mandatory |
| ------------- |-------------- | ------------- |
| -f \<file-path\> <br> --file \<file-path\> | Path to input file  | Yes |
| -d \<datatype,datatype\> <br> --datatypes \<datatype,datatype\> | Comma separated list of data types to be applied to the columns  | Yes |
| -o \<file-path\> <br> --outputlocation \<file-path\> | Output location for generated file | Yes |
| -s  <br> --skip header | Skip the first line of the CSV file | No | 

## Example Usage
```
python CSVParser.py -f 2018-Q1.csv -d STRING,STRING,INT,INT,INT,INT,DECIMAL -o output/ -s
```
### Example Input
City,Suburb,"Sales 1Q 2017","Median 1Q 2017","Sales 1Q 2018","Median 1Q 2018","Median Change"
ADELAIDE,ADELAIDE,6,"673,750",5,"861,000",27.79% <br>
ADELAIDE,NORTH ADELAIDE,7,"1,100,000",2,"2,195,500",99.59%

### Example Output
ADELAIDE,ADELAIDE,6,673750,5,861000,27.79 <br>
ADELAIDE,NORTH ADELAIDE,7,1100000,2,2195500,99.59
