# Make quotes

This scripts creates quotes using GPT4ALL python integration. </br>
This script also supports translation in french </br>

This is aimed to be used to generate autoamtic videos.

---

The requirements are as follow :

    conda create -n makevideos
    conda activate makevideos
    conda install python
    pip install gpt4all
    pip install deep-translator

## Arguments
The script supports arguments such as :

    python create_quotes.py 10 -fr

This creates 10 quotes in english then translateds them to english using google traduction

    python create_quotes.py -o

This creates a single paragraph in english and saves it to default location

    python create_quote.py -on filename.csv

This will save the quotes on the specified file

