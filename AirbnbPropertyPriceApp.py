#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import pickle
import zipfile
import os

# In[2]:


# Separando os inputs do modelo
x_numeric = {'latitude': 0, 'longitude': 0, 'accomodates': 0, 'bathrooms': 0, 
             'bedrooms': 0, 'beds': 0, 'extra_people': 0, 'minimum_nights': 0,
             'year': 0, 'month': 0, 'n_amenities': 0, 'host_listings_count': 0
             }

x_boolean = {'host_is_superhost': 0, 'instant_bookable': 0}

x_lists = {'property_type': ['Apartment', 'Condominium', 'House', 'Loft',
          'Serviced apartment', 'others'],
           'room_type': ['Entire home/apt', 'Others'],
           'cancellation_policy': ['flexible', 'moderate', 'strict',
                                   'strict_14_with_grace_period']
           }

# Separando o modelo
zp = zipfile.ZipFile(os.path.join('Airbnb_Project/AppFiles/model.zip'), mode='r')
model = zp.extractall()


# In[3]:


# Criando os botões
for item in x_numeric:
  if (item == 'latitude') or (item == 'longitude'):
    valor = st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f')
  elif item == 'extra_people':
    valor = st.number_input(f'{item}', step=0.01, value=0.0)
  else:
    valor = st.number_input(f'{item}', step=1, value=0)
  x_numeric[item] = valor

for item in x_boolean:
  valor = st.selectbox(f'{item}', ('Yes', 'No'))
  if valor == 'Yes':
    x_boolean[item] = 1
  else:
    x_boolean[item] = 0

dict_ = {}
for item in x_lists:
  valor = st.selectbox(f'{item}', x_lists[item])
  for value in x_lists[item]:    
    if value == valor:
      dict_[f'{item}_{valor}'] = 1
    else:
      dict_[f'{item}_{value}'] = 0


botao = st.button('Predict property price')

if botao:
  dict_.update(x_numeric)
  dict_.update(x_boolean)
  x_values = pd.DataFrame(dict_, index=[0])
  modelo = pickle.load(open(model,mode='rb'))
  preco = modelo.predict(x_values)
  st.write(preco[0])

