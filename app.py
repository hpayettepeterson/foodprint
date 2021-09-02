import requests
import streamlit as st
# import datetime
# import pandas as pd
# import plotly as plt
# import plotly.express as px
# import plotly.graph_objects as go
# import pickle
# ############## LOADING SESSION #######################################
# complete_df = pd.read_csv("data/dishes_with_co2_nutrients_3.csv")
# cached_df = pickle.load(open("foodprint/cached_data/cached_im2recipe.pickle", "rb"))
# clustering_df = pd.read_csv('data/3D_recipe_clustering.csv')
# recipes_df = pd.read_csv('data/dishes_with_co2_nutrients_3.csv')

# ######################################################################

# Custom imports
from multipage import MultiPage
from pages import dish_info, food_stats

# Create an instance of the app
app = MultiPage()

# Title of the main page
st.title("foodprint.ai")
st.write('A project at Le Wagon Data Science Bootcamp')
st.write('How can you make more informed choices about your food? foodprint.ai provides you with carbon footprint and nutritional information about your favorite dishes, and can help you find greener alternatives.')
st.write('-----------------------------')
# Add all your applications (pages) here
app.add_page("Food Statistics", food_stats.app)
app.add_page("Dish Search", dish_info.app)

# The main app
app.run()



# # add sidebar
# st.sidebar.markdown(f"""
#     # Navigation
#     \n
#     """)



# if st.sidebar.button('Food Statistics'):
#     # print is visible in the server output, not in the page
#     print('button clicked!')

# if st.sidebar.button('Test a Dish'):
#     # print is visible in the server output, not in the page
#     print('button clicked!')
#     st.write('I was clicked 🎉')
#     st.write('Further clicks are not visible but are executed')
# else:
#     st.write('I was not clicked 😞')


# st.markdown("""
#     # Welcome to **Foodprint.ai**! (Project@  **LE WAGON**)
#     ## Check the CO2 ouput* of your favorite dish:
# """)
# dish_selection = ["nothing"]
# dish_selection = st.multiselect( ' ',  complete_df["dish_name"])
# dish_number = st.slider('How many dish recommendations do you want to see?', 1, 10, 5)


# ############starts the magic! ####################################################
# if st.button('PRESS ME - DAMN IT - I CANNOT WAIT!'):
#     ##### variables #############################
#     temp_df = complete_df.loc[complete_df['dish_name'].isin(dish_selection)]
#     temp_id = temp_df["id"].values[0]
#     temp_ingredients = temp_df["ingredients"].values[0]
#     temp_weight_per_ingr = temp_df["weight_per_ingr"].values[0]
#     temp_total_dish_weight = temp_df["total_dish_weight"].values[0]
#     temp_total_footprint = temp_df["total_footprint"].values[0]
#     temp_dish_footprint_per_100gr = temp_df["dish_footprint_per_100gr"].values[0]
#     temp_confidence_score = temp_df["confidence_score"].values[0]
#     temp_dish_footprint_per_kilo = temp_df["dish_footprint_per_kilo"].values[0]
#     temp_co2_score = temp_df["co2_score"].values[0]
#     temp_km_driven_per_100gr = temp_df["km_driven_per_100gr"].values[0]

#     ##### text ##################################
#     #st.write("You have select: "+ dish_selection[0]+ "(ID: "+ temp_id+")")
#     #st.write(" Total dish weight is " + str(temp_total_dish_weight.round(2)) + "g")
#     #st.write(" total CO2 footprint is: " + str(temp_total_footprint.round(2)))
#     #st.write("We calculated that the  CO2 footprint per 100g is:  " + str(temp_dish_footprint_per_100gr.round(2)) + "g or per 1kg: " + str(temp_dish_footprint_per_kilo.round(2))+"kg")
#     if temp_co2_score == "low":
#         st.success(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a low  CO2-Score (below 2kg of CO2 output per 1kg)')
#     if temp_co2_score == "moderate":
#         st.warning(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a moderate CO2-Score (between 2kg and 3kg per 1kg)')
#     if temp_co2_score == "high":
#         st.error(dish_selection[0]+ ' has a CO2 output per Kg of '+str(temp_dish_footprint_per_kilo.round(2))+  ' and therefore a high CO2-Score (higher than 3kg per 1kg)')
#     st.write("We are " + str((temp_confidence_score*100).round(2))+"%"  + " sure that this score is accurate!")
#     #st.write("The ingredients are: " + str(temp_ingredients)[1:-1])
#     st.write("Eating 100g of this dish equals "+ str(temp_km_driven_per_100gr.round(2))  + "km driving a car.")

#     #####  TALK TO THE API #############################
#     url=f'https://foodprint-m7tvgzo76q-ew.a.run.app/predict?recipe_id={temp_id}&n_neighbors={dish_number}'

#     response = requests.get(url)
#     if response.status_code == 503:
#         st.write("try again in a few moments!")
#     else:
#         j_response = response.json()

#         #st.write(response.json())
#         api_input_df=pd.DataFrame.from_dict(j_response["prediction"])
#         #api_input_df["distance"] = api_input_df["distance"].apply(lambda x: x)
#         api_input_df["marker_size"] = api_input_df["nutritional_value"]*2

#         #####  PLOT - Standart #############################
#         fig_api = px.scatter_3d(api_input_df,
#                                 title="Here you can find better choices",
#                                 x='distance',
#                                 y='nutritional_value',
#                                 z='co2',
#                                 labels={
#                                     "distance": " ",
#                                     "nutritional_value": " nutritional value ",
#                                     "co2": "co2 output per 100g"
#                                 },
#                                 size="marker_size",
#                                 hover_name='name',
#                                 color='co2')
#         #fig_api.update_layout(showlegend=True)
#         st.plotly_chart(fig_api)

# else:
#     st.write('')



# direction = st.radio('Select a diet-type',
#                      ('all', 'vegetarian', 'non-vegetarian'))

# # add new column to df
# # transform high scores
# mask = clustering_df['co2_score'].str.contains(r'high', na=True)
# clustering_df.loc[mask, 'co2_score_num'] = 3
# # transform med scores
# mask = clustering_df['co2_score'].str.contains(r'moderate', na=True)
# clustering_df.loc[mask, 'co2_score_num'] = 2
# # transform low scores
# mask = clustering_df['co2_score'].str.contains(r'low', na=True)
# clustering_df.loc[mask, 'co2_score_num'] = 1

# # make dfs of veg and nonveg
# clustering_df['dietary_info'] = recipes_df['dietary_info']
# mask = clustering_df['dietary_info'].str.contains(r'non-veg', na=True)
# clustering_df_nonveg = clustering_df.loc[mask]
# mask = clustering_df['dietary_info'].str.contains(r'vegetarian', na=True)
# clustering_df_veg = clustering_df.loc[mask]

# if direction == 'all':
#     df = clustering_df
# elif direction == 'non-vegetarian':
#     df = clustering_df_nonveg
# elif direction == 'vegetarian':
#     df = clustering_df_veg


# if st.button("Load the big cloud of recipes!"):

#     # get data
#     #recipe_id = temp_id
#     # recipe_id = "000095fc1d"
#     # row = clustering_df.loc[clustering_df['id'] == recipe_id]
#     # a = float(row['PCA1'])
#     # b = float(row['PCA2'])
#     # c = float(row['PCA3'])
#     # transform high scores

#     # replace plot code with this
#     # change this variable based on if you want to show all recipes, just veg, or just non-veg
#     #df = clustering_df
#     x, y, z = df['PCA1'], df['PCA2'], df['PCA3']
#     recipe = df['recipeName']
#     co2 = df['co2']
#     fig = go.Figure(data=[go.Scatter3d(
#         x=x,
#         y=y,
#         z=z,
#         mode='markers',
#         hovertext= recipe,
#         text=co2,
#         hovertemplate = '%{hovertext}<br>CO2: {text}', # can't get text to properly substitute
#         marker=dict(
#             size=4,
#             color=df['co2_score_num'],                # set color to an array/list of desired values
#             colorscale='RdYlGn',   # choose a colorscale
#             opacity=0.8,
#             reversescale= True
#         )
#     )])
#     # camera = dict(
#     #     center=dict(x=a, y=b, z=c),
#     #     eye=dict(x=0.0001, y=0.0001, z=0.0001)
#     # )
#     #fig.update_layout(scene_camera=camera, title="name")
#     fig.update_layout(width=800, height=800, showlegend=False)
#     st.plotly_chart(fig)
# else:
#     st.write("")

# st.write(
#     "1* Please note that all the values are relativ and you can imagine them between plusminus 30 percent. Homegrown veggies and fruits surely produces less CO2 then imported or transported products. Still, the score can help you to make better decisions! Especially meat is high in CO2 output - choose vegan food more often. Besides: the data stems from healable. This is just a project, not company or something"
# )
