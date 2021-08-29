import streamlit as st
import requests
import datetime
import pandas as pd
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle
import numpy as np

def app():
    st.markdown('## Food Statistics')

    st.write('Average carbon footprint (in kilos of CO2) per kilo of food:')

    # get data
    clustering_df = pd.read_csv('data/3D_recipe_clustering.csv')
    recipes_df = pd.read_csv('data/dishes_with_co2_nutrients_3.csv')

    # average footprints
    mean_co2_100gr_all = round((10 * np.mean(recipes_df['dish_footprint_per_100gr'])), 3)

    mask1 = recipes_df['dietary_info'].str.contains(r'vegetarian', na=True)
    mean_co2_100gr_veg = round((10 * np.mean(recipes_df[mask1]['dish_footprint_per_100gr'])), 3)

    mask2 = recipes_df['dietary_info'].str.contains(r'non-veg', na=True)
    mean_co2_100gr_nonveg = round((10 * np.mean(recipes_df[mask2]['dish_footprint_per_100gr'])), 3)

    col1, col2, col3 = st.columns(3)
    col1.metric("All dishes", mean_co2_100gr_all)
    col2.metric("Vegetarian dishes", mean_co2_100gr_veg)
    col3.metric("Non-vegetarian dishes", mean_co2_100gr_nonveg)

    st.write('-------------')
    st.markdown('## Dish Clustering')
    st.markdown('### Below is a clustering of different dishes, each represented by a point in the embedding space.')
    st.write('Similar dishes are nearby each other. Each dish is colored according to its carbon footprint (green: low, yellow: moderate, red: high). Feel free to explore the clustering and check out the differences between vegetarian and non-vegetarian foods.')

    direction = st.radio('Select a dish type:',
                        ('all', 'vegetarian', 'non-vegetarian'))
    # add new column to df
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
    x, y, z = df['PCA1'], df['PCA2'], df['PCA3']
    recipe = df['recipeName']
    co2 = round((df['co2'] * 10), 4)
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        hovertext= recipe,
        text=co2,
        hovertemplate = '%{hovertext}<br>CO2/Kilo:%{text}', # can't get text to properly substitute
        marker=dict(
            size=4,
            color=df['co2_score_num'],                # set color to an array/list of desired values
            colorscale='RdYlGn',   # choose a colorscale
            opacity=0.8,
            reversescale= True
        )
    )])
    # camera = dict(
    #     center=dict(x=a, y=b, z=c),
    #     eye=dict(x=0.0001, y=0.0001, z=0.0001)
    # )
    #fig.update_layout(scene_camera=camera, title="name")
    fig.update_layout(width=800, height=800, showlegend=False)
    st.plotly_chart(fig)

    st.write(
            "\* Please note that the calculated carbon footprints are only estimates, to be used for educational purposes."
        )
    if st.button("Find out more"):
        st.write('Write about how we got the data, from which sources etc (healabel, scientific paper etc')
