# Project #3: Association Rule Mining

### Description
Implementation of a simplified version of the A-Priori **a**ssociation **r**ule **min**ing algorithm.

### USAGE
`python armin.py input_filename output_filename min_support_percentage min_confidence`

where:
* `input_filename` is the name of the file that contains market basket data that is the input to the program.
* `output_filename` is the name of the file that will store the required output of the program. The file contains the frequent item sets and the association rules that it discovered after processing the submitted input data.
* `min_support_percentage` is the minimum support percentage for an itemset / association rule to be considered frequent, e.g., 5%. This should be provided as a floating point number (out of 1), e.g., 0.05, 0.4, 0.5 are used to denote 5%, 40%, and 50% respectively. Percent symbol is not included.
* `min_confidence` is the minimum confidence for an association rule to be significant, e.g., 50%. This should be provided as a floating point number (out of 1), e.g., 0.05, 0.4, 0.5 are used to denote 5%, 40%, and 50% respectively. Percent symbol is not included.  

An example call to the program:
`python3 armin.py input.csv output.csv 0.5 0.7`

---
