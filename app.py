import requests
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

############## LOADING SESSION #######################################
complete_df = pd.read_csv("raw_data/temp_dishes_with_co2.csv")

######################################################################

st.markdown("""
    # Welcome to **Foodprint.ai**! (Project@  **LE WAGON**)
    ## Check the CO2 ouput* of your favorite dish:
""")
dish_selection = ["nothing"]
dish_selection = st.multiselect( ' ',  complete_df["dish_name"])
dish_number = st.slider('How many dish recommendations do you want to see?', 1, 10, 5)


############starts the magic! ####################################################
if st.button('PRESS ME - DAMN IT - I CANNOT WAIT!'):
    ##### variables #############################
    temp_df = complete_df.loc[complete_df['dish_name'].isin(dish_selection)]
    temp_id = temp_df["id"].values[0]
    temp_ingredients = temp_df["ingredients"].values[0]
    temp_weight_per_ingr = temp_df["weight_per_ingr"].values[0]
    temp_total_dish_weight = temp_df["total_dish_weight"].values[0]
    temp_total_footprint = temp_df["total_footprint"].values[0]
    temp_dish_footprint_per_100gr = temp_df["dish_footprint_per_100gr"].values[0]
    temp_confidence_score = temp_df["confidence_score"].values[0]
    temp_dish_footprint_per_kilo = temp_df["dish_footprint_per_kilo"].values[0]
    temp_co2_score = temp_df["co2_score"].values[0]
    temp_km_driven_per_100gr = temp_df["km_driven_per_100gr"].values[0]

    ##### text ##################################
    #st.write("You have select: "+ dish_selection[0]+ "(ID: "+ temp_id+")")
    #st.write(" Total dish weight is " + str(temp_total_dish_weight.round(2)) + "g")
    #st.write(" total CO2 footprint is: " + str(temp_total_footprint.round(2)))
    #st.write("We calculated that the  CO2 footprint per 100g is:  " + str(temp_dish_footprint_per_100gr.round(2)) + "g or per 1kg: " + str(temp_dish_footprint_per_kilo.round(2))+"kg")
    if temp_co2_score == "low":
        st.success(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a low  CO2-Score (below 2kg of CO2 output per 1kg)')
    if temp_co2_score == "moderate":
        st.warning(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a moderate CO2-Score (between 2kg and 3kg per 1kg)')
    if temp_co2_score == "high":
        st.error(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a high CO2-Score (higher than 3kg per 1kg)')
    st.write("We are " + str((temp_confidence_score*100).round(2))+"%"  + " sure that this score is accurate!")
    #st.write("The ingredients are: " + str(temp_ingredients)[1:-1])
    st.write("Eating 100g of this dish equals "+ str(temp_km_driven_per_100gr.round(2))  + "km driving a car.")

    #####  TALK TO THE API #############################
    url=f'https://foodprint-m7tvgzo76q-ew.a.run.app/predict?recipe_id={temp_id}&n_neighbors={dish_number}'
    response = requests.get(url)
    j_response = response.json()
    #st.write(response)
    #st.write(response.json())
    api_input_df=pd.DataFrame.from_dict(j_response["prediction"])
    #api_input_df["distance"] = api_input_df["distance"].apply(lambda x: x)

    #####  PLOT - Standart #############################
    fig = px.scatter_3d(api_input_df, title="Here you can find better choices", x='distance',y='marker_size',z='co2',
                     labels={
                     "distance": " ",
                     "marker_size": " ",
                     "co2": "co2 output per 100g"
                 }, size_max=18,hover_name='name', color='co2')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)


    #####  PLOT - ZOOM #############################
    #fig2 = go.Figure(data=api_input_df (x='distance', y='marker_size', z='co2'))
    #fig2.update_layout(
    #    titel="hi",
    #    width=400, height=400,
    #    margin=dict(t=30,r=0,l=20,b=10)
    #)
    #fig.update_layout(
    #title='Mt Bruno Elevation',
    #width=400, height=400,
    #margin=dict(t=30, r=0, l=20, b=10)
    #name = 'eye = (x:0.1, y:0.1, z:1.5)'
    #camera = dict(
    #    eye=dict(x=0.1, y=0.1, z=1.5)
    #)

    #fig.update_layout(scene_camera=camera, title=name)
    #fig.show()


    #st.write(j_response[0])
    #import plotly.express as px
    #fig = px.scatter_3d(response[""], x='sepal_length', y='sepal_width', z='petal_width',
    #          color='species')
    #fig.show()
else:
    st.write('')


st.write("* Please note that all the values are relativ and you can imagine them between plusminus 30 percent. Homegrown veggies and fruits surely produces less CO2 then imported or transported product. Still, the score can help you to make better decisions! Especially meat is high in CO2 output - choose vegan food more often")