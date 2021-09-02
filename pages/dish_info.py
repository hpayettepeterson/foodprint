import requests
import streamlit as st

import pandas as pd

import plotly.express as px


import ast
import numpy as np


def app():
    ############## LOADING SESSION #######################################
    complete_df = pd.read_csv("gs://foodprint-672/data/dishes_with_co2_nutrients_3.csv")
    #complete_df = complete_df.sort_values('dish_name')
    #cached_df = pickle.load(open("foodprint/cached_data/cached_im2recipe.pickle", "rb"))
    clustering_df = pd.read_csv('gs://foodprint-672/data/3D_recipe_clustering.csv')
    recipes_df = pd.read_csv('gs://foodprint-672/data/dishes_with_co2_nutrients_3.csv')

    ######################################################################

    st.markdown("""
        ## Check the estimated CO2 output* of your favorite dish
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
                st.table(recipe_temp_df.head(3))
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
            #st.markdown(f'This dish has about **{calories} calories** per 100 g serving.')
            # show link to recipe?

            # get other nutritional info per 100gr for dish with particular ID
            # fat
            fat = round(recipes_df.loc[recipes_df['id'] == temp_id]['fat_per_100gr'].values[0], 2)
            # protein
            protein = round(recipes_df.loc[recipes_df['id'] == temp_id]['protein_per_100gr'].values[0], 2)
            # salt
            salt = round(recipes_df.loc[recipes_df['id'] == temp_id]['salt_per_100gr'].values[0], 2)
            # sugar
            sugar = round(recipes_df.loc[recipes_df['id'] == temp_id]['sugar_per_100gr'].values[0], 2)
            st.write('Here is some nutritional info for a 100 g serving of this dish.')

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("calories", calories)
            col2.metric("fat (g)", fat)
            col3.metric("protein (g)", protein)
            col4.metric('salt (g)', salt)
            col5.metric('sugar (g)', sugar)


            #####  TALK TO THE API #############################
            st.markdown('## Similar Dishes:')

            url=f'https://foodprint-m7tvgzo76q-ew.a.run.app/predict_similarities?recipe_id={temp_id}&n_neighbors={dish_number}'

            response = requests.get(url)
            if response.status_code == 503:
                st.write("Try to load this dish again in a few moments to see similar dishes")
            else:
                j_response = response.json()

                #st.write(response.json())
                api_input_df=pd.DataFrame.from_dict(j_response["prediction"]).head()
                #api_input_df["distance"] = api_input_df["distance"].apply(lambda x: x)

                # add co2 scoring
                api_input_df['Dish'] = api_input_df['name']
                api_input_df['Calories (per 100 g)'] = np.round(api_input_df['calories_per_100g'], 2)
                api_input_df['Carbon Footprint'] = api_input_df['co2']

                api_input_df['CO2 Output (kg per kg)'] = np.round(api_input_df['co2'].apply(lambda x: x * 10), 2)
                api_input_df.loc[api_input_df['CO2 Output (kg per kg)'] <= (3), 'Carbon Footprint'] = 'moderate'
                api_input_df.loc[api_input_df['CO2 Output (kg per kg)'] <= (2), 'Carbon Footprint'] = 'low'
                api_input_df.loc[api_input_df['CO2 Output (kg per kg)'] > (3), 'Carbon Footprint'] = 'high'

                df_show = api_input_df.copy(deep=True)
                df_show.drop(columns=['name', 'percentage_of_similarity', 'co2', 'calories_per_100g'], inplace=True)
                st.write('Here is the searched dish and the top four most similar dishes, along with carbon footprint and calorie information. This information can help you find greener options.')
                st.table(df_show)

                st.write('Here is a plot of the searched dish along with the four most similar dishes. The dishes are shown along three axes: CO2 output, calories per 100gr serving, and similarity (lower = more similar to input dish).')
                fig_api = px.scatter_3d(api_input_df,
                    title="",
                    x='percentage_of_similarity',
                    y='calories_per_100g',
                    z='CO2 Output (kg per kg)',
                    labels={
                        "percentage_of_similarity": "Similarity",
                        "calories_per_100g": "Calories (per 100 g)",
                        "CO2 Output (kg per kg)": "CO2 Output (kg per kg)"
                    },
                    color_discrete_map={
                                "low": "green",
                                "moderate": "yellow",
                                "high": "red"},
                    template="plotly",
                    hover_name='name',
                    hover_data=["CO2 Output (kg per kg)", "Carbon Footprint"],
                    color='Carbon Footprint')
                fig_api.update(layout_coloraxis_showscale=False)
                st.plotly_chart(fig_api)
                #####  PLOT - Standart #############################
                # fig_api = px.scatter_3d(api_input_df,
                #                         title="",
                #                         x='distance',
                #                         y='nutritional_value',
                #                         z='co2',
                #                         labels={
                #                             "distance": " ",
                #                             "nutritional_value": " nutritional value ",
                #                             "co2": "co2 output per 100g"
                #                         },
                #                         size="marker_size",
                #                         hover_name='name',
                #                         color='co2',
                #                         color_continuous_scale=px.colors.diverging.RdYlGn[::-1])
                # #fig_api.update_layout(showlegend=True)
                # st.plotly_chart(fig_api)

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

                        ### See the recipe for this dish [here]({recipe_url}) (note that some links may no longer work)
                        ''')

            st.write('')

    st.write('--------')
    st.write(
        "\* Please note that the calculated carbon footprints are only estimates, to be used for educational purposes."
    )
    if st.button("Find out more"):

        st.markdown('''We collected carbon footprint data from [Reducing food’s environmental impacts through producers and consumers](https://science.sciencemag.org/content/360/6392/987) and [Healabel](https://healabel.com/carbon-footprint-of-foods). The CO2 emissions per ingredient are only estimates of average values and may not always be accurate.
                    We used food and recipe data from [pic2recipe](http://pic2recipe.csail.mit.edu/) and [Yummly](https://alioben.github.io/yummly/).
                    \nThis project was completed by Hannah Payette Peterson, Jean-Arnaud Ritouret, Martin Lechner, and Christopher Scott.''')
