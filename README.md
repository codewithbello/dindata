# The DINData Software

DINData - DIDBase Numerica Iongram dataset. 
The software is to take care of missing days and filter data based on CS value on the DIDBase digisonde numerical ionogram dataset.

# DINData GUI Setup Download

Download the Dindata exe GUI Setup for Windows machine from Zendo
10.5281/zenodo.17937258


### DINData GUI Software User’s Brief Guide

A test numerical ionogram data `DIDBGetValuesAll.txt` for the year `2020` is included in the setup folder.

1. Intsall the DINDATA software
2. Open the software after installation and click on the Browse button to load the test dataset.
3. Enter `2010-01-01` for the start date and `2010-12-13` for the end date
4. Enter any value between `0-100` for CS or leave empty. The default value is `0`.
5. Click the Run button

If the process is successful, the output file is in the created DINDATA folder in the Windows PC Document folder.


# Running the source code

You will need to have git install on your machine

### Step 1:

Run the command 

`https://github.com/bioyesaeed/dindata.git`

### Step 2:

Run the command below on your terminal

`cd dindata` or the folder conatining the dindata code, and then run

 `pip install -r requirements.txt`

### Step 3:

Run the dindata on your terminal

`python main.py'

