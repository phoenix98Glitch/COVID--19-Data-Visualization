#!/usr/bin/env python
# coding: utf-8

# # COVID-19 DATA VISUALIZATION 

# ### Importing modules

# ### Task 1

# In[2]:


import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt 
print('modules are imported')


# ### Task 1.1: 
# #### Loading the Dataset

# In[3]:


dataset_url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv(dataset_url)   


# ### Task 1.2:
# #### let's check the dataframe 

# In[4]:


df.head()


# In[5]:


df.tail()


# #### let's check the shape of the dataframe 

# In[6]:


df.shape


# ### Task 2.1 :
# #### let's do some preprocessing 

# In[7]:


df = df[df.Confirmed > 0]


# In[8]:


df.head()


# #### let's see data related to a country for example India 
# 

# In[9]:


df[df.Country == 'India']


# #### let's see Global spread of Covid19

# In[12]:


fig = px.choropleth(df , locations = 'Country' , locationmode='country names',color='Confirmed'
                   ,animation_frame='Date')
fig.update_layout(title_text = 'Global Spread of COVID-19')
fig.show()


# ### Task 2.2 : Exercise 
# #### Let's see Global deaths of Covid19

# In[13]:


fig = px.choropleth(df , locations = 'Country' , locationmode='country names',color='Deaths'
                   ,animation_frame='Date')
fig.update_layout(title_text = 'Global Deaths of COVID-19')
fig.show()


# ### Task 3.1:
# #### Let's Visualize how intensive the Covid19 Transmission has been in each of the country
# let's start with an example:

# In[14]:


df_china = df[df.Country == 'China']
df_china.head()


# let's select the columns that we need

# In[15]:


df_china = df_china[['Date','Confirmed']]


# In[16]:


df_china.head()


# calculating the first derivation of confrimed column

# In[17]:


df_china['Infection Rate'] = df_china['Confirmed'].diff()


# In[18]:


df_china.head()


# In[19]:


px.line(df_china , x = 'Date' , y = ['Confirmed','Infection Rate'])


# In[20]:


df_china['Infection Rate'].max()


# ### Task 3.2:
# #### Let's Calculate Maximum infection rate for all of the countries

# In[21]:


df.head()


# In[22]:


countries = list(df['Country'].unique())
max_infection_rates = []
for c in countries :
    MIR = df[df.Country == c].Confirmed.diff().max()
    max_infection_rates.append(MIR)


# ### Task 3.3:
# #### let's create a new Dataframe 

# In[23]:


df_MIR = pd.DataFrame()
df_MIR['Country'] = countries
df_MIR['Max Infection Rate'] = max_infection_rates
df_MIR.head()


# #### Let's plot the barchart : maximum infection rate of each country

# In[24]:


px.bar(df_MIR, x='Country' , y='Max Infection Rate', color = 'Country' , title ='Global Maximum infection rate', log_y=True)


# ### Task 4: Let's See how National Lockdowns Impacts Covid19 transmission in India

# ### COVID19 pandemic lockdown in India 
# On 24 March 2020, the Government of India under Prime Minister Narendra Modi ordered a nationwide lockdown for 21 days, limiting movement of the entire 1.3 billion population of India as a preventive measure against the COVID-19 pandemic in India.It was ordered after a 14-hour voluntary public curfew on 22 March, followed by enforcement of a series of regulations in the country's COVID-19 affected regions.The lockdown was placed when the number of confirmed positive coronavirus cases in India was approximately 500. <a href="https://en.wikipedia.org/wiki/COVID-19_pandemic_lockdown_in_India#:~:text=On%209%20March%202020%2C%20the,COVID%2D19%20in%20the%20country.">source</a>

# In[18]:


india_lockdown_start_date = '2020-03-25'
india_lockdown_a_month_later = '2020-04-25'


# In[19]:


df.head()


# let's get data related to india

# In[20]:


df_india = df[df.Country == 'India']


# lets check the dataframe

# In[21]:


df_india.head()


# let's calculate the infection rate in Italy

# In[22]:


df_india['Infection Rate'] = df_india.Confirmed.diff()
df_india.head()


# ok! now let's do the visualization

# In[23]:


fig = px.line(df_india , x = 'Date' , y = 'Infection Rate' , title = "Before and After Lockdown in India")
fig.add_shape(
    dict(
    type="line",
    x0=india_lockdown_start_date,
    y0=0,
    x1=india_lockdown_start_date,
    y1= df_india['Infection Rate'].max(),
    line = dict(color='red' , width=2)

    )

)
fig.add_annotation(
     dict(
     x = india_lockdown_start_date,
     y = df_india['Infection Rate'].max(),
     text = 'starting date of the lockdown'  
     )
)
fig.add_shape(
    dict(
    type="line",
    x0=india_lockdown_a_month_later,
    y0=0,
    x1=india_lockdown_a_month_later,
    y1= df_india['Infection Rate'].max(),
    line = dict(color='orange' , width=2)

    )

)
fig.add_annotation(
     dict(
     x = india_lockdown_a_month_later,
     y = 0,
     text = 'a month later'  
     )
)


# ### Task 5: Let's See how National Lockdowns Impacts Covid19 Deaths rate in India

# In[48]:


df_india.head()


# let's calculate the deaths rate

# In[24]:


df_india['Deaths Rate'] = df_india.Deaths.diff()


# let's check the dataframe again

# In[25]:


df_india.head()


# now let's plot a line chart to compare COVID19 national lockdowns impacts on spread of the virus and deaths rate

# In[26]:


fig = px.line(df_india,x='Date',y=['Infection Rate','Deaths Rate'])
fig.show()


# let's normalize the columns

# In[27]:


df_india['Infection Rate'] = df_india['Infection Rate']/df_india['Infection Rate'].max()
df_india['Deaths Rate'] = df_india['Deaths Rate']/df_india['Deaths Rate'].max()


# let's plot the line chart again

# In[34]:


fig = px.line(df_india , x='Date', y=['Infection Rate','Deaths Rate'])
fig.add_shape(
    dict(
    type="line",
    x0=india_lockdown_start_date,
    y0=0,
    x1=india_lockdown_start_date,
    y1= df_india['Infection Rate'].max(),
    line = dict(color='black' , width=2)

    )

)
fig.add_annotation(
     dict(
     x = india_lockdown_start_date,
     y = df_india['Infection Rate'].max(),
     text = 'starting date of the lockdown'  
     )
)
fig.add_shape(
    dict(
    type="line",
    x0=india_lockdown_a_month_later,
    y0=0,
    x1=india_lockdown_a_month_later,
    y1= df_india['Infection Rate'].max(),
    line = dict(color='orange' , width=2)

    )

)
fig.add_annotation(
     dict(
     x = india_lockdown_a_month_later,
     y = 0,
     text = 'a month later'  
     )
)


# ### COVID19 pandemic lockdown in Germany 
# Lockdown was started in Freiburg, Baden-Württemberg and Bavaria on 20 March 2020. Three days later, it was expanded to the whole of Germany

# In[37]:


Germany_lockdown_start_date = '2020-03-23' 
Germany_lockdown_a_month_later = '2020-04-23'


# let's select the data related to Germany

# In[38]:


df_germany= df[df.Country =='Germany']


# let's check the dataframe 

# In[39]:


df_germany.head()


# let's calculate the infection rate and deaths rate in Germany

# In[40]:


df_germany['Infection Rate'] = df_germany.Confirmed.diff()
df_germany['Deaths Rate'] = df_germany.Deaths.diff()


# let's check the dataframe

# In[41]:


df_germany.head()


# let's do some scaling and plot the line chart 

# In[42]:


df_germany['Infection Rate'] = df_germany['Infection Rate']/df_germany['Infection Rate'].max()
df_germany['Deaths Rate'] = df_germany['Deaths Rate']/df_germany['Deaths Rate'].max()


# In[43]:


fig = px.line(df_germany, x='Date', y=['Infection Rate','Deaths Rate'])
fig.add_shape(
    dict(
    type="line",
    x0=Germany_lockdown_start_date,
    y0=0,
    x1=Germany_lockdown_start_date,
    y1= df_germany['Infection Rate'].max(),
    line = dict(color='black' , width=2)

    )

)
fig.add_annotation(
     dict(
     x = Germany_lockdown_start_date,
     y = df_germany['Infection Rate'].max(),
     text = 'starting date of the lockdown'  
     )
)
fig.add_shape(
    dict(
    type="line",
    x0=Germany_lockdown_a_month_later,
    y0=0,
    x1=Germany_lockdown_a_month_later,
    y1= df_germany['Infection Rate'].max(),
    line = dict(color='yellow' , width=2)

    )

)
fig.add_annotation(
     dict(
     x = Germany_lockdown_a_month_later,
     y = 0,
     text = 'a month later'  
     )
)

