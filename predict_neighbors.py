import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from foodprint.params import MODEL_NAME, BUCKET_NAME, PATH_TO_LOCAL_MODEL
import pickle
import joblib
from google.cloud import storage


def load_vectorized_data(path_to_recipes_data ='./foodprint/cached_data/cached_vectorized_data.pickle'):
    # Load dataframe  from pickle file
    df_recipes_vect = pickle.load(open(path_to_recipes_data,"rb"))
    return df_recipes_vect

def load_informational_data(path_to_recipes_data ='./foodprint/cached_data/cached_informational_data.pickle'):
    # Load dataframe from pickle file
    df_recipes_info = pickle.load(open(path_to_recipes_data,"rb"))
    return df_recipes_info

def get_recipe_input(recipe_id, df_recipes):
    # Get the recipe in the right input shape for our model
    recipe = np.array(df_recipes.loc[recipe_id]).reshape(-1,1).T
    return recipe


def download_model(model_directory="PipelineTest",
                   bucket=BUCKET_NAME,
                   rm=False):
    client = storage.Client().bucket(bucket)

    storage_location = 'models/{}/versions/{}/{}'.format(
        MODEL_NAME, model_directory, PATH_TO_LOCAL_MODEL)
    blob = client.blob(storage_location)
    blob.download_to_filename(PATH_TO_LOCAL_MODEL)
    print("=> pipeline downloaded from storage")
    model = joblib.load(PATH_TO_LOCAL_MODEL)
    if rm:
        os.remove(PATH_TO_LOCAL_MODEL)

    return model


def load_model(path_to_model="./models/nneighbors_model.pkl"):
    # Load model from pickle file
    # nneighbors_model = pickle.load(open(path_to_model,"rb"))
    nneighbors_model = joblib.load(open(path_to_model,"rb"))
    return nneighbors_model




def get_neighbors(recipe_input, df_recipes_info, nneighbors_model, n_neighbors):
    # Find the n closest neighbors with their distance, including the recipe input
    neighbors = nneighbors_model.kneighbors(X=recipe_input, n_neighbors=n_neighbors, return_distance=True)

    # Create the dataframe of the neighbors including their name, distance to inpu, co2 footprint
    # and marker size (power function of co2 fooprint)
    dict_to_plot = {'name':[],'distance':[], 'co2':[],'nutritional_value':[]}

    for rec in zip(neighbors[0][0], neighbors[1][0]):
        dict_to_plot['name'].append(df_recipes_info.iloc[rec[1]]['recipeName'])
        dict_to_plot['distance'].append(rec[0])
        dict_to_plot['co2'].append(df_recipes_info.iloc[rec[1]]['co2'])
        dict_to_plot['nutritional_value'].append(df_recipes_info.iloc[rec[1]]['nutritional_value'])

    df_neighbors = pd.DataFrame(dict_to_plot)

    return df_neighbors

def plot_neighbors(df_neighbors):
    # Scatter plot of the input and closest neighbors
    # size of the points and colors depend on marker size
    plt.scatter(df_neighbors['distance'], # this is X
            df_neighbors['co2'], # this is Y
            s=df_neighbors['nutritional_value'], # this is the size of points
            c=df_neighbors['co2'], #this is the color
            cmap="Blues",
            alpha=0.6,
            edgecolors="grey",
            linewidth=1)

    # Add the names of recipes as label of the points
    for x,y,z in zip(df_neighbors['distance'],df_neighbors['co2'],df_neighbors['name']):
        label = f"{z}"
        plt.annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.show()

if __name__ == '__main__':
    recipe_id = '006ab0aafd'

    df_recipes_vect = load_vectorized_data()
    print('df_recipes_vect : ')
    print(df_recipes_vect)
    print('\n')

    df_recipes_info = load_informational_data()
    print('df_recipes_info : ')
    print(df_recipes_info)
    print('\n')

    recipe_input = get_recipe_input(recipe_id, df_recipes_vect)
    print('recipe_input : ')
    print(recipe_input)
    print('\n')

    nneighbors_model = load_model()
    df_neighbors = get_neighbors(recipe_input, df_recipes_info, nneighbors_model, n_neighbors=5)
    print('df_neighbors : ')
    print(df_neighbors)
    print('\n')

    plot_neighbors(df_neighbors)
