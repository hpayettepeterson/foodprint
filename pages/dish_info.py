import requests
import streamlit as st
import datetime
import pandas as pd
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle
import ast
import numpy as np


def app():
    ############## LOADING SESSION #######################################
    complete_df = pd.read_csv("data/dishes_with_co2_nutrients_3.csv")
    #complete_df = complete_df.sort_values('dish_name')
    cached_df = pickle.load(open("foodprint/cached_data/cached_im2recipe.pickle", "rb"))
    clustering_df = pd.read_csv('data/3D_recipe_clustering.csv')
    recipes_df = pd.read_csv('data/dishes_with_co2_nutrients_3.csv')

    ######################################################################

    st.markdown("""
        ## Check the estimated CO2 ouput* of your favorite dish
    """)
    st.write('Select a dish to see its estimated carbon footprint, nutritional info, suggestions of similar dishes, and more')
    dish_selection = ["nothing"]
    dish_selection = st.multiselect( 'Select a dish or start typing one in...',  complete_df["dish_name"])
    dish_number = 5 #st.slider('How many dish recommendations do you want to see?', 1, 10, 5)


    ############starts the magic! ####################################################
    if st.button('Tell me about my dish!'):
         ##### variables #############################
        temp_df = complete_df.loc[complete_df['dish_name'].isin(dish_selection)]
        if len(temp_df) == 0:
            st.write('Please select a dish')
        else:
            temp_id = temp_df["id"].values[0]
            temp_ingredients = ast.literal_eval(temp_df["ingredients"].values[0])
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
                st.markdown(f'{dish_selection[0]} has an output of **{str(temp_dish_footprint_per_kilo.round(2))} kg** of CO2 per Kg of food')
                st.success('This is a relatively LOW carbon footprint (below 2 kg of CO2 output per 1 kg)')
            if temp_co2_score == "moderate":
                st.markdown(f'{dish_selection[0]} has an output of **{str(temp_dish_footprint_per_kilo.round(2))} kg** of CO2 per Kg of food')
                st.warning('This is a relatively MODERATE carbon footprint (between 2 and 3 kg of CO2 output per 1 kg)')
            if temp_co2_score == "high":
                st.markdown(f'{dish_selection[0]} has an output of **{str(temp_dish_footprint_per_kilo.round(2))} kg** of CO2 per Kg of food')
                st.error('This is a relatively HIGH carbon footprint (over 3 kg of CO2 output per 1 kg)')
            st.markdown(f"We have CO2 data for **{str((temp_confidence_score*100).round(2))}%** of the ingredients in this dish.")
            #st.write("The ingredients are: " + str(temp_ingredients)[1:-1])
            st.markdown(f"Eating 100 g of this dish outputs the same CO2 as driving **{str(temp_km_driven_per_100gr.round(2))} km** in a car.")

            # get ingredient footprints, make temp df
            st.write('The following three ingredients account for the highest percentages of the dish\'s carbon footprint:')

            ingr_footprints = ast.literal_eval(recipes_df.loc[recipes_df['id'] == temp_id]['footprint_per_ingr_100gr'].values[0])
            ingr_names = ast.literal_eval(recipes_df.loc[recipes_df['id'] == temp_id]['ingredients'].values[0])

            # get percentages that each ingredient accounts for of total footprint
            percentage_of_total_footprint = []
            for ingredient_number, ingredient in enumerate(ingr_footprints):
                if ingredient != False:
                    ingr_percent = np.round(((ingr_footprints[ingredient_number] / temp_dish_footprint_per_100gr) * 100), 1)
                    percentage_of_total_footprint.append(ingr_percent)
                else:
                    percentage_of_total_footprint.append(None)


            # make temp df for displaying top 3 ingredients

            if len(ingr_names) == len(ingr_footprints):
                recipe_temp_df = pd.DataFrame({'Ingredient': ingr_names, 'Carbon Footprint': ingr_footprints})
                recipe_temp_df['Percentage of dish CO2 Footprint'] = percentage_of_total_footprint
                recipe_temp_df.sort_values('Carbon Footprint', ascending=False, inplace=True)
                recipe_temp_df.reset_index(inplace=True)
                recipe_temp_df.drop(columns=['Carbon Footprint', 'index'], inplace=True)
                st.write(recipe_temp_df.head(3))
                st.write('You can use this information to make informed choices about which ingredients you could substitute to reduce your carbon footprint.')
            else:
                message = 'Sorry, we don\'t have ingredient information available for this dish'
                st.write(message)



            ## Nutritional info
            st.markdown('## Nutritional Info:')

            # get calorie info
            calories = int(round(recipes_df.loc[recipes_df['id'] == temp_id]['calories_per_100gr'].values[0], 0))
            #mask3 = recipes_df['id'].str.contains(f'{id}', na=True)
            #calories = recipes_df[mask3]['calories_per_100gr'].values[0] # NEED HELP TROUBLESHOOTING THIS LINE, how to get calorie info
            st.markdown(f'This dish has about **{calories} calories** per 100g serving.')
                  # show link to recipe?

            st.write('ADD MORE NUTRITIONAL INFO')


            st.write('GET BUTTON WORKING FOR INGREDIENTS')


            #####  TALK TO THE API #############################
            st.markdown('## Similar Dishes:')
            st.write('HERE ADD A LIST OF MOST SIMILAR DISHES')
            url=f'https://foodprint-m7tvgzo76q-ew.a.run.app/predict?recipe_id={temp_id}&n_neighbors={dish_number}'

            response = requests.get(url)
            if response.status_code == 503:
                st.write("Try to load this dish again in a few moments to see similar dishes")
            else:
                j_response = response.json()

                #st.write(response.json())
                api_input_df=pd.DataFrame.from_dict(j_response["prediction"])
                #api_input_df["distance"] = api_input_df["distance"].apply(lambda x: x)
                api_input_df["marker_size"] = api_input_df["nutritional_value"]*2

                #####  PLOT - Standart #############################
                st.write('Here are some similar dishes and their carbon footprints. Here you can find greener options. (Output list of similar dishes and their footprints or calories)')
                fig_api = px.scatter_3d(api_input_df,
                                        title="",
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

            ### Other dish info
            st.markdown("## Other info about this dish:")
            st.markdown('''

                        ### Ingredients:''')
            for ingredient in temp_ingredients:
                    st.markdown(f'- {ingredient}')
            #if st.button('See all ingredients'): # get this working
            #     for ingredient in temp_ingredients:
            #         st.write(ingredient)
            recipe_url = recipes_df.loc[recipes_df['id'] == temp_id]['url'].values[0]
            st.markdown(f'''

                        ### See the recipe for this dish [here]({recipe_url})
                        ''')

            st.write('')

    st.write('--------')
    st.write(
        "\* Please note that the calculated carbon footprints are only estimates, to be used for educational purposes."
    )
    if st.button("Find out more"):
        st.write('Write about how we got the data, from which sources etc (healabel, scientific paper etc')
