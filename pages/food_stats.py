import streamlit as st


import pandas as pd

import plotly.graph_objects as go

import numpy as np

def app():
    st.markdown('## Food Statistics')

    st.markdown('### Average carbon footprint (in kilos of CO2) per kilo of food:')

    # get data
    clustering_df = pd.read_csv('gs://foodprint-672/data/3D_recipe_clustering.csv')
    recipes_df = pd.read_csv('gs://foodprint-672/data/dishes_with_co2_nutrients_3.csv')

    # average footprints
    # random comment
    mean_co2_100gr_all = round((10 * np.mean(recipes_df['dish_footprint_per_100gr'])), 2)

    mask1 = recipes_df['dietary_info'].str.contains(r'vegetarian', na=True)
    mean_co2_100gr_veg = round((10 * np.mean(recipes_df[mask1]['dish_footprint_per_100gr'])), 2)

    mask2 = recipes_df['dietary_info'].str.contains(r'non-veg', na=True)
    mean_co2_100gr_nonveg = round((10 * np.mean(recipes_df[mask2]['dish_footprint_per_100gr'])), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("All dishes", mean_co2_100gr_all)
    col2.metric("Vegetarian dishes", mean_co2_100gr_veg)
    col3.metric("Non-vegetarian dishes", mean_co2_100gr_nonveg)

    # show co2 data of meats
    st.markdown('### The average carbon footprint per kilo of some common ingredients:')
    co2_df = pd.read_csv('gs://foodprint-672/data/co2.csv')

    st.markdown('#### Meats')
    meats_lst = ['beef', 'pork', 'lamb', 'duck', 'chicken', 'salmon']

    carbon_output_meats = []
    scores_lst = []
    for meat in meats_lst:
        carbon_output = co2_df.loc[co2_df['ingredients'] == meat]['CO2_per_kilo'].values[0]
        carbon_output_meats.append(carbon_output)
        scores_lst.append('high')


    meats_df = pd.DataFrame(
        {'Food': meats_lst,
        'CO2 Output (kg per kg)': carbon_output_meats,
        'Carbon Footprint': scores_lst
        })
    meats_df.sort_values('CO2 Output (kg per kg)', ascending=False, inplace=True)
    st.table(meats_df)

    st.markdown('#### Non-meats')
    nonmeats_df = pd.read_csv('gs://foodprint-672/data/nonmeats.csv')
    st.table(nonmeats_df)

    st.write('A carbon footprint is considered low if it is below 2 kg of CO2 output per 1 kg of food, moderate if it is between 2 and 3 kg of CO2 per kg, and high if it is greater than 3 kg of CO2 per kg.')

    st.write('-------------')
    st.markdown('## Dish Clustering')
    st.markdown('### Below is a clustering of different dishes, each represented by a point in the embedding space.')
    st.write('Similar dishes are nearby each other. Each dish is colored according to its carbon footprint (green: low, yellow: moderate, red: high). Explore the clustering and check out the differences between vegetarian and non-vegetarian foods.')

    direction = st.radio('Select a dish type:',
                        ('all', 'vegetarian', 'non-vegetarian'))

    # add co2 per kilo column
    clustering_df['dish_footprint_per_kilo'] = clustering_df['dish_footprint_per_100gr'].apply(lambda x: x * 10)

    clustering_df['co2_score_num'] = clustering_df['dish_footprint_per_kilo']

    # transform high scores
    mask = clustering_df['co2_score'].str.contains(r'high', na=True)
    clustering_df.loc[mask, 'co2_score_num'] = 3
    # transform med scores
    mask = clustering_df['co2_score'].str.contains(r'moderate', na=True)
    clustering_df.loc[mask, 'co2_score_num'] = 2
    # transform low scores
    mask = clustering_df['co2_score'].str.contains(r'low', na=True)
    clustering_df.loc[mask, 'co2_score_num'] = 1

    # make dfs of veg and nonveg
    clustering_df['dietary_info'] = recipes_df['dietary_info']
    mask = clustering_df['dietary_info'].str.contains(r'non-veg', na=True)
    clustering_df_nonveg = clustering_df.loc[mask]
    mask = clustering_df['dietary_info'].str.contains(r'vegetarian', na=True)
    clustering_df_veg = clustering_df.loc[mask]

    if direction == 'all':
        df = clustering_df
    elif direction == 'non-vegetarian':
        df = clustering_df_nonveg
    elif direction == 'vegetarian':
        df = clustering_df_veg




    # get data
    #recipe_id = temp_id
    # recipe_id = "000095fc1d"
    # row = clustering_df.loc[clustering_df['id'] == recipe_id]
    # a = float(row['PCA1'])
    # b = float(row['PCA2'])
    # c = float(row['PCA3'])
    # transform high scores

    # replace plot code with this
    # change this variable based on if you want to show all recipes, just veg, or just non-veg
    #df = clustering_df
    x, y, z = df['Dim1'], df['Dim2'], df['Dim3']
    recipe = df['dish_name']
    co2 = round((df['dish_footprint_per_kilo']), 4)
    fig = go.Figure(data=[
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            hovertext=recipe,
            text=co2,
            hovertemplate='%{hovertext}<br>CO2/kg:%{text}',
            marker=dict(
                size=4,
                color=
                df['co2_score_num'],  # set color to an array/list of desired values
                colorscale='RdYlGn',  # choose a colorscale
                opacity=0.8,
                reversescale=True))
    ])
    # camera = dict(
    #     center=dict(x=a, y=b, z=c),
    #     eye=dict(x=0.0001, y=0.0001, z=0.0001)
    # )
    #fig.update_layout(scene_camera=camera, title="name")
    fig.update_layout(width=800, height=800, showlegend=False)
    st.plotly_chart(fig)






    st.write('--------------')
    st.markdown('## More facts about our data')
    st.markdown('''The total number of recipes in our dataset is **51235**.
            Among them **44820** are vegetarian and **6415** are meat-based.''')

    st.markdown('''**32054** of the vegetarian recipes have a low carbon footprint, **9169** have a moderate one and **3597** have a high one.''')

    st.markdown('''**1614** of the non-vegetarian recipes have a low carbon footprint, **1074** have a moderate one and **3727** have a high one.''')

    st.markdown('''Per 100 g serving, **508** out of **6415** total non-vegetarian recipes exceed **2 kg** of CO2 output.''')

    st.markdown('''In contrast, the vegetarian recipe with the highest carbon footprint outputs **1.1 kg** of CO2 per 100 g serving.
                ''')

    # expander = st.expander("More information about our data")

    # expander.markdown('''We collected carbon footprint data from [Reducing food’s environmental impacts through producers and consumers](https://science.sciencemag.org/content/360/6392/987) and [Healabel](https://healabel.com/carbon-footprint-of-foods). The CO2 emissions per ingredient are only estimates of average values and may not always be accurate.
    #             We used food and recipe data from [pic2recipe](http://pic2recipe.csail.mit.edu/) and [Yummly](https://alioben.github.io/yummly/).

    #             Total amount of recipes: 51235
    #             Among them 44820 are vegetarian and 6415 are meat-based.
    #             Vegis score:
    #             low        32054
    #             moderate    9169
    #             high        3597
    #             Meat score:
    #             low        1614
    #             moderate   1074
    #             high       3727
    #             Even on 100g basis, 508 out of 6415 total meat-based recipes exceed the 2kg CO2 output. Among those 357 recipes even count as “high” on a 100g basis! On 1kg base, this even increases to 3717, making almost half of the recipes.
    #             The highest CO2 recipe found in vegetarian recipes per 100g is 1.1kg that still count as “low”. On 1kg level, 3524 out 44820 would be rated as “high”.
    #             ''')
    st.write('---------')
    st.write(
            "\* Please note that the calculated carbon footprints are only estimates, to be used for educational purposes."
        )
    if st.button("Find out more"):

        st.markdown('''We collected carbon footprint data from [Reducing food’s environmental impacts through producers and consumers](https://science.sciencemag.org/content/360/6392/987) and [Healabel](https://healabel.com/carbon-footprint-of-foods). The CO2 emissions per ingredient are only estimates of average values and may not always be accurate.
                We used food and recipe data from [pic2recipe](http://pic2recipe.csail.mit.edu/) and [Yummly](https://alioben.github.io/yummly/).
                \nThis project was completed by Hannah Payette Peterson, Jean-Arnaud Ritouret, Martin Lechner, and Christopher Scott.\nYou can contact us at hpayettepeterson@gmail.com''')
