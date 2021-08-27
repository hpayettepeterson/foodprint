import pandas as pd
import plotly.graph_objects as go

# get data
clustering_df = pd.read_csv('data/3D_recipe_clustering.csv')

# transform high scores
mask = clustering_df['co2_score'].str.contains(r'high', na=True)
clustering_df.loc[mask, 'co2_score_num'] = 3
# transform med scores
mask = clustering_df['co2_score'].str.contains(r'moderate', na=True)
clustering_df.loc[mask, 'co2_score_num'] = 2
# transform low scores
mask = clustering_df['co2_score'].str.contains(r'low', na=True)
clustering_df.loc[mask, 'co2_score_num'] = 1


# make plotly

x, y, z = clustering_df['PCA1'], clustering_df['PCA2'], clustering_df['PCA3']
recipe = clustering_df['recipeName']
co2 = clustering_df['co2']

fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    hovertext= recipe,
    hovertemplate = '%{hovertext}<br>CO2: {text}', # can't get text to properly substitute for
    text=[clustering_df['co2']],
    marker=dict(
        size=3,
        color=clustering_df['co2_score_num'],                # set color to an array/list of desired values
        colorscale='RdYlGn',   # choose a colorscale
        opacity=0.8,
        reversescale= True
    )
)])

fig.show()
