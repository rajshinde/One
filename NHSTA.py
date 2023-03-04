import pandas as pd;
import requests;
import math;

#Initialize the url and the post data and output receiving variables
# The output will be taken from string in csv format to file. Blank records would be deleted later on

url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/';
post_fields = {'format': 'csv', 'data':''};
output_data = '' 

#Read the input data which consists of VIN 10 numbers.
#Remove the duplicates to save unnecessary API calls. Lastly, convert the data to list form

data = pd.read_csv('/Manheim_VIN_Data.csv')
data.drop(data[data[['VIN 10']].duplicated()].index,axis=0,inplace=True)
data_list = data['VIN 10'].tolist()

# Batch size is 50. So we can call 50 records at a time. Call 50 records at a time in for loop and concatenate the output string

total_api_calls = math.ceil(len(data)/50)

#Write output in a csv file. This file will contain blank records and multiplie header columns

for x in range(0,total_api_calls):
    post_fields['data'] = ';'.join(data_list[50 * x : 50 * (x+1)])
    r = requests.post(url, data=post_fields);
    with open("/Output.csv","a") as text_File:
        text_File.write(r.text)

    

# This block of code removes the header column present throughtout per 50 records and then removes the blank records also.
df = pd.read_csv('/Output.csv', encoding= 'unicode_escape')
df = df[df.makeid != 'makeid']
df.to_csv('/Output.csv', index=False)
