import requests
import streamlit as st
import datetime
import pandas as pd
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle
import ast


def app():
    ############## LOADING SESSION #######################################
    complete_df = pd.read_csv("data/dishes_with_co2_nutrients_3.csv")
    cached_df = pickle.load(open("foodprint/cached_data/cached_im2recipe.pickle", "rb"))
    clustering_df = pd.read_csv('data/3D_recipe_clustering.csv')
    recipes_df = pd.read_csv('data/dishes_with_co2_nutrients_3.csv')

    ######################################################################

    st.markdown("""
        ## Check the estimated CO2 ouput* of your favorite dish
    """)
    st.write('Select a dish to see its estimated carbon footprint, nutritional info, suggestions of similar dishes, and more')
    dish_selection = ["nothing"]
    dish_selection = st.multiselect( ' ',  complete_df["dish_name"])
    dish_number = st.slider('How many dish recommendations do you want to see?', 1, 10, 5)


    ############starts the magic! ####################################################
    if st.button('Tell me about my dish!'):
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

        ## CO2 info
        st.markdown('## CO2 Info:')
        if temp_co2_score == "low":
            st.success(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a low  CO2-Score (below 2kg of CO2 output per 1kg)')
        if temp_co2_score == "moderate":
            st.warning(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a moderate CO2-Score (between 2kg and 3kg per 1kg)')
        if temp_co2_score == "high":
            st.error(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a high CO2-Score (higher than 3kg per 1kg)')
        st.write("We are " + str((temp_confidence_score*100).round(2))+"%"  + " sure that this score is accurate!")
        #st.write("The ingredients are: " + str(temp_ingredients)[1:-1])
        st.write("Eating 100g of this dish equals "+ str(temp_km_driven_per_100gr.round(2))  + "km driving a car.")

        ## Nutritional info
        st.markdown('## Nutritional Info:')

        # get calorie info
        mask3 = recipes_df['id'].str.contains(f'{id}', na=True)
        #calories = recipes_df[mask3]['calories_per_100gr'].values[0] # NEED HELP TROUBLESHOOTING THIS LINE, how to get calorie info
        #st.write(f'This dish has about {calories} per 100g serving.')
        st.write(temp_ingredients) # process these so they appear nicely
        # show link to recipe?
        if st.button('See ingredients'): # get this working
            st.write(temp_ingredients)

        #####  TALK TO THE API #############################
        url=f'https://foodprint-m7tvgzo76q-ew.a.run.app/predict?recipe_id={temp_id}&n_neighbors={dish_number}'

        response = requests.get(url)
        if response.status_code == 503:
            st.write("try again in a few moments!")
        else:
            j_response = response.json()

            #st.write(response.json())
            api_input_df=pd.DataFrame.from_dict(j_response["prediction"])
            #api_input_df["distance"] = api_input_df["distance"].apply(lambda x: x)
            api_input_df["marker_size"] = api_input_df["nutritional_value"]*2

            #####  PLOT - Standart #############################
            fig_api = px.scatter_3d(api_input_df,
                                    title="Here you can find better choices",
                                    x='distance',
                                    y='nutritional_value',
                                    z='co2',
                                    labels={
                                        "distance": " ",
                                        "nutritional_value": " nutritional value ",
                                        "co2": "co2 output per 100g"
                                    },
                                    size="marker_size",
                                    hover_name='name',
                                    color='co2')
            #fig_api.update_layout(showlegend=True)
            st.plotly_chart(fig_api)

    else:
        st.write('')


    st.write(
        "\* Please note that the calculated carbon footprints are only estimates, to be used for educational purposes."
    )
    if st.button("Find out more"):
        st.write('Write about how we got the data, from which sources etc (healabel, scientific paper etc')
