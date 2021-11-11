# CAHD_Anonimization
Implementation of CAHD algorithm for transaction data anonymization

Starting from the paper _"On the Anonymization of Sparse High-Dimensional Data"_ this code wants to show a possible implementation using **Python** programming language.

## Main
#### Input params:

* -p *param* 
* -QID_subset *for KL-Divergence computation*
* -SD_subset *for KL-Divergence computation*
* -dataset *path*

After parsing the input file, and checking the validity of other inputs the anonymization takes place. Finally the *KL-Divergence* and *computed time* values are printed and the two matrices shown.

### Output:

The result of the anonymization is written in the appropriate *AnonymizedDataset* file.


## Reverse_Cuthil_McKee

**RCM** class returns *band matrix* and keeps correspondence between the two matrices for each SD.

## Anonymizer
 
**CAHD** class apply the algorithm and create *groups*.

## KLDivergenceCalculator

**Calculator** class computes *ACT*,*EST* and finally *KL-Divergence*.



## Sources
[On the Anonymization of Sparse High-Dimensional Data](https://github.com/Elpinzeiro/CAHD_Anonimization/blob/main/On%20the%20Anonymization%20of%20Sparse%20High-Dimensional%20Data.pdf)
