import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import time
import datetime
import os
import streamlit.components.v1 as components

st.caption("Lucie Bottin - M1-APP-BDIA - Streamlit projet, 2020 csv\n")
st.title("Trouve ta nouvelle maison 🏡😊")

#D E C O R A T O R S
#log execution time
@st.cache(suppress_st_warning=True) 
def log(func):
    def wrapper(*args,**kwargs):
        with open("logs.txt","a") as f:
            f.write("Called function with " + " ".join([str(arg) for arg in args]) + " at " + str(datetime.datetime.now()) + "\n")
        val = func(*args,**kwargs)
        return val
    return wrapper

@log
def run(a,b,c=9):
    print(a+b+c)

run(1,3,c=9)

def create_map(df):
    df['latitude']=pd.to_numeric(df['latitude'])
    df['longitude']=pd.to_numeric(df['longitude'])
    df.dropna(subset = ['latitude', 'longitude'], inplace = True)
    st.header("Lieux des biens :")
    st.map(df[['latitude', 'longitude']])

def pie(df) :

    local_count = df['type_local'].value_counts()
    local_count = pd.DataFrame({'Names' :local_count.index, 'Values' :local_count.values})
    fig = px.pie(local_count, values='Values', names='Names')
    st.header("Types de biens disponibles")
    st.plotly_chart(fig)
    
def sidebar(df) :

    data_set = df[['type_local', 'nombre_pieces_principales', 'code_postal', 'valeur_fonciere', 'surface_terrain','latitude', 'longitude']]
    liste_departements = df['code_postal'].dropna().astype(int).to_list()
    
    st.sidebar.header("Mes critères :")
    option = st.sidebar.selectbox('Quel type de local vous intéresse ?', ('Choisir', 'Maison', 'Appartement', 'Dépendance','Local industriel. commercial ou assimilé'))
    option2 = st.sidebar.selectbox('Combien de pieces ?', ['Choisir']+[0,1,2,3,4,5])
    option3 = st.sidebar.selectbox('Dans quel département ?', ['Choisir']+liste_departements)
    check = st.sidebar.checkbox("Terrain extérieur")

    if option  :
        mask = (data_set['type_local'] == option)
        data_set = data_set[mask]

    if option2  :
        mask1 = (data_set['nombre_pieces_principales'] == option2)
        data_set = data_set[mask1]

    if option3  :
        mask2 = (data_set['code_postal'] == option3)
        data_set = data_set[mask2]

    if check :
        option4 = st.sidebar.slider('Surface terrain en m2 ?',20,2000)
        
        if option4  :
            mask3 = (data_set['surface_terrain'] > option4)
            data_set = data_set[mask3]
            
   
    return data_set

def bar_chart(a) :

    st.header("Valeurs foncières des biens qui correspondent à vos choix :")
    st.bar_chart(data=a["valeur_fonciere"])
    st.header("Surface extérieur des biens qui correspondent à vos choix :")
    st.bar_chart(data=a['surface_terrain'])
    
@st.cache(suppress_st_warning=True)    
def convert_df(df):
     return df.to_csv().encode('utf-8')

if __name__ == "__main__":

    df = pd.read_csv('sample_2020.csv')
    fig, ax = plt.subplots(figsize=(10, 7))
    pie(df)
    a = sidebar(df)
    if not (a.empty):
        st.header("Liste des biens selon vos choix")
        st.write(a)
        csv = convert_df(a)
        st.download_button(
            label="Télécharger la liste",
            data=csv,
            file_name='liste_biens.csv',
            mime='text/csv',
        )
        create_map(a)
        bar_chart(a)
