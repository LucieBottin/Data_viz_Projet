import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.express as px


def create_map(sub_df):
    sub_df['latitude']=pd.to_numeric(sub_df['latitude'])
    sub_df['longitude']=pd.to_numeric(sub_df['longitude'])
    sub_df.dropna(subset = ['latitude', 'longitude'], inplace = True)
    st.map(sub_df[['latitude', 'longitude']])

#def count_rows(rows) :
    #return len(rows)
    

def pie(df) :

    local_count = df['type_local'].value_counts()
    local_count = pd.DataFrame({'Names' :local_count.index, 'Values' :local_count.values})
    fig = px.pie(local_count, values='Values', names='Names')
    st.plotly_chart(fig)




def sidebar(df) :

    data_set = df[['type_local', 'nombre_pieces_principales', 'code_postal', 'valeur_fonciere', 'surface_terrain','latitude', 'longitude']]

    option = st.sidebar.selectbox('Quel type de local vous intéresse ?', ('Choisir', 'Maison', 'Appartement', 'Dépendance','Local industriel. commercial ou assimilé'))
    option2 = st.sidebar.selectbox('Combien de pieces ?', ['Choisir']+[0,1,2,3,4,5])
    option3 = st.sidebar.selectbox('Dans quel département ?', ['Choisir']+[cp for cp in range(1000, 6000)])
    check = st.sidebar.checkbox("Terrain extérieur")

    if check :
        option4 = st.sidebar.slider('Surface terrain en m2 ?',20,2000)
        
        if option4  :
            mask3 = (data_set['surface_terrain'] > option4)
            data_set = data_set[mask3]


    if option  :
        mask = (data_set['type_local'] == option)
        data_set = data_set[mask]

    if option2  :
        mask1 = (data_set['nombre_pieces_principales'] == option2)
        data_set = data_set[mask1]

    if option3  :
        mask2 = (data_set['code_postal'] == option3)
        data_set = data_set[mask2]

    
    st.write(data_set)

    reset = st.sidebar.button(label="Reset")

    if reset :   
        data_set = df[['type_local', 'nombre_pieces_principales', 'code_postal', "valeur_fonciere", 'surface_terrain','latitude', 'longitude']]

    return data_set


if __name__ == "__main__":

    #file_path = "full_2020.csv"
    #df_full = pd.read_csv(file_path, delimiter = ',')
    #csv_sample = df_full.head(100000).to_csv('sample_2020.csv')
    df = pd.read_csv('sample_2020.csv')
    pie(df)
    a = sidebar(df)
    fig, ax = plt.subplots(figsize=(10, 7))
    create_map(a)
    st.title("Valeurs foncières des biens qui correspondent à vos choix :")
    st.bar_chart(data=a["valeur_fonciere"])
    st.title("Surface extérieur des biens qui correspondent à vos choix :")
    st.bar_chart(data=a['surface_terrain'])
