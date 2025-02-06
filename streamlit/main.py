import streamlit as st
import pandas as pd
import joblib

#get the model
model = joblib.load('model.joblib')


st.write('# Predict Oil prices in china')
st.image('2024-08-02_dqevqgf3r0.webp')

#upload the file
file = st.file_uploader("You can Upload a File ")
if file :
    df = pd.read_excel(file)
    st.session_state['disabled'] = True
else:
    st.session_state['disabled'] = False

date = st.date_input("Date :", disabled=st.session_state['disabled'])
pch = st.number_input('Indice des actions : ', disabled=st.session_state['disabled'])
tch = st.number_input('Température : ', disabled=st.session_state['disabled'])
co2ch = st.number_input('CO2CH exprimés en Millions : ', disabled=st.session_state['disabled'])
chus = st.number_input('Chinese Yuan to US $ : ', disabled=st.session_state['disabled'])
ich = st.number_input("Taux d'intérêt : ", disabled=st.session_state['disabled'])

#split the date to year-month-day
date = str(date)
year = int(date[:date.find('-')])
date = date[date.find('-')+1:]
month = int(date[:date.find('-')])
day = int(date[date.find('-')+1:])

#create the dataframe
columns = ['Indice des actions', 'Température', 'Emission CO2','Chinese Yuan to US $', "Taux d'intérêt", 'month','year', 'day']
cdf = pd.DataFrame([pch, tch, co2ch,chus,ich, month, year, day], columns=columns)

def clicked():
    if st.session_state['disabled'] == True:
        st.session_state['error'] = False
        # predict the result for the given file
        st.session_state['res'] = 6
    elif pch == 0 or tch == 0 or co2ch == 0 or chus == 0 or ich == 0:
        st.session_state['error'] = True
    else:
        st.session_state['error'] = False
        #predict the result from the given inputs
        model.fit()
        st.session_state['res'] = 7
    

st.button('predict', on_click=clicked)

#check if the button is clicked or not
if 'res' in st.session_state:
    res = st.session_state['res']
    st.write(res) 


#errors Handlers
if 'error' in st.session_state and st.session_state['error'] == True:
    st.warning('fileds are required')