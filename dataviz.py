import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px


st.title("Trouve ta nouvelle maison 🏡😊")

def create_map(sub_df):
    sub_df['latitude']=pd.to_numeric(sub_df['latitude'])
    sub_df['longitude']=pd.to_numeric(sub_df['longitude'])
    sub_df.dropna(subset = ['latitude', 'longitude'], inplace = True)
    st.header("Lieux des biens :")
    st.map(sub_df[['latitude', 'longitude']])

#def count_rows(rows) :
    #return len(rows)
    

def pie(df) :

    local_count = df['type_local'].value_counts()
    local_count = pd.DataFrame({'Names' :local_count.index, 'Values' :local_count.values})
    fig = px.pie(local_count, values='Values', names='Names')
    st.header("Types de biens disponibles")
    st.plotly_chart(fig)




def sidebar(df) :

    data_set = df[['type_local', 'nombre_pieces_principales', 'code_postal', 'valeur_fonciere', 'surface_terrain','latitude', 'longitude']]

    option = st.sidebar.selectbox('Quel type de local vous intéresse ?', ('Choisir', 'Maison', 'Appartement', 'Dépendance','Local industriel. commercial ou assimilé'))
    option2 = st.sidebar.selectbox('Combien de pieces ?', ['Choisir']+[0,1,2,3,4,5])
    option3 = st.sidebar.selectbox('Dans quel département ?', ['Choisir']+[cp for cp in range(1000, 6000)])
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

if __name__ == "__main__":

    #file_path = "full_2020.csv"
    #df_full = pd.read_csv(file_path, delimiter = ',')
    #csv_sample = df_full.head(100000).to_csv('sample_2020.csv')
    df = pd.read_csv('sample_2020.csv')
    fig, ax = plt.subplots(figsize=(10, 7))
    pie(df)
    a = sidebar(df)
    if not (a.empty):
        st.header("Liste des biens selon vos choix")
        st.write(a)
        create_map(a)
        bar_chart(a)
    reset = st.sidebar.button(label="Reset")
    if reset :   
        a = df
