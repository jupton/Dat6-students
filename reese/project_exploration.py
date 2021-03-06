# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:43:10 2015

Adoption has had a significant impact on my life. When I was around 10 years old,
my mother adopted two 18 month old toddlers from Romania: Ileana and Traian. 

Traian came from an orphanage where the matron did not have time to change all 
the babies' diapers. Instead, she would paint them with disinfectant.

Ileana was marginally lucky; she came from a foster home. However, she was so
malnourished that she had developed rickets and spent the first few months in
her new home in a cast.

They are now both 16. Traian is studying to be a pilot. Ileana just broke up
with her first boyfriend, and she's pretty inconsolable, but she'll bounce back.
She wants to move to L.A. and be an actress.

I want to mine through international adoption statistics and find if there are
any telling correlations: high cost and high volume, number of adoptions per
thousand residents, ec.

@author: reesem
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from math import e
from sklearn.neighbors import KNeighborsClassifier

#Country adoption numbers
data = pd.read_csv('../../dat6-students/reese/adoption_countries.csv')

#State census information
states = pd.read_csv('https://www.census.gov/popest/data/state/totals/2011/tables/NST-EST2011-01.csv')

#Number of international adoptions by state
statesadopt = pd.read_csv('../../dat6-students/reese/state_international_adoptions.csv')

#Get a sense of the data
data.head()
'''

Issues to clean:
1) Eliminate empty spaces in column headers
2) Eliminate asterices in country names/define what they mean
3) Deal with NaN values in columns 3-5

'''

#Replace empty spaces with _
for strings in data:
    data.rename(columns = {strings : strings.replace(' ','_')}, inplace = True)

data.average_days_to_completion.mean()
data.head(10)
data.number_of_convention_cases.isnull()

#Get a general graph of the data

#Is there a correlation between adoptions finalized abroad vs. in the US?
data.plot(x = ['adoptions_finalized_abroad'], y = ['adoptions_to_be_finalized_in_the_u.s.'], kind = 'scatter', xlim = (0,2500))
#Looks very L shaped. Slope looks undefined. Let's look closer
data.plot(x = ['adoptions_finalized_abroad'], y = ['adoptions_to_be_finalized_in_the_u.s.'], kind = 'scatter', xlim = (0,500))
#Still L shaped. Let's look closer again:
data.plot(x = ['adoptions_finalized_abroad'], y = ['adoptions_to_be_finalized_in_the_u.s.'], kind = 'scatter', xlim = (0,50),ylim=(0,50))
#Still L shaped. Looks like, generally, one precludes the other.

#Some of the country names have a * preceding them. According to the key with
#the original PDF, this means they do not participate in the Hague convention.
#Does this have any effect on where the adoption is completed?

#First make a numerical column. If a country has an asterisk, it gets 0.
#Otherwise, 1

def is_hague(row):
    if '*' not in row['country']:
        return 1
    else:
        return 0
        
data['is_hague'] = data.apply(lambda row: is_hague(row), axis = 1)

#We now have 2 dataframes: one for is_hague, one for isnt
data_is_hague = data[data['is_hague'] == 1]
data_not_hague = data[data['is_hague'] == 0]

#Let's plot the same graphs
plt.scatter(data_is_hague['adoptions_finalized_abroad'],data_is_hague['adoptions_to_be_finalized_in_the_u.s.'],color='red',alpha=.75)
plt.scatter(data_not_hague['adoptions_finalized_abroad'],data_not_hague['adoptions_to_be_finalized_in_the_u.s.'],color='blue',alpha=.75)
plt.xlim(0,500)
plt.ylim(0,350)
#There doesn't seem to be a substantial difference.

#What about size?
data_is_hague.shape
data_not_hague.shape

#Moving on to State data
statesadopt.head()