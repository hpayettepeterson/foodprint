import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from foodprint.params import MODEL_NAME, BUCKET_NAME, PATH_TO_LOCAL_MODEL
import pickle
import joblib
from google.cloud import storage


def load_recipe_similarities(path_to_recipe_similarities ='./foodprint/cached_data/cached_recipe_similarities.pickle'):
    # Load dataframe  from pickle file
    X_recipe_similarities = pickle.load(open(path_to_recipe_similarities,"rb"))
    return -X_recipe_similarities

def load_similar_recipes(path_to_similar_recipes ='./foodprint/cached_data/cached_similar_recipes.pickle'):
    # Load dataframe  from pickle file
    X_similar_recipes = pickle.load(open(path_to_similar_recipes,"rb"))
    return X_similar_recipes

def load_informational_data(path_to_recipes_data ='./foodprint/cached_data/cached_informational_data.pickle'):
    # Load dataframe from pickle file
    df_recipes_info = pickle.load(open(path_to_recipes_data,"rb"))
    return df_recipes_info

def get_similar_recipes(recipe_id, df_recipes_info, X_similar_recipes, X_recipe_similarities, n_similar):
    # Find the n most similar recipes with their distance, including the recipe input
    recipe_index = df_recipes_info.index[df_recipes_info['id']==recipe_id][0]

    # Create the dataframe of the neighbors including their name, distance to inpu, co2 footprint
    # and marker size (power function of co2 fooprint)
    dict_to_plot = {'name':[],'percentage_of_similarity':[], 'co2':[],'calories_per_100g':[]}

    for rec in zip(X_similar_recipes[recipe_index], X_recipe_similarities[recipe_index]):
        rec_index = int(rec[0])
        print('rec_index')
        print(rec_index)
        dict_to_plot['name'].append(df_recipes_info.iloc[rec_index]['recipeName'])
        dict_to_plot['percentage_of_similarity'].append(rec[1])
        dict_to_plot['co2'].append(df_recipes_info.iloc[rec_index]['co2'])
        dict_to_plot['calories_per_100g'].append(df_recipes_info.iloc[rec_index]['calories_per_100g'])

    df_similar = pd.DataFrame(dict_to_plot)

    return df_similar

if __name__ == '__main__':
    recipe_id = '006ab0aafd'

    X_recipe_similarities = load_recipe_similarities()
    print('X_recipe_similarities : ')
    print(X_recipe_similarities)
    print('\n')

    X_similar_recipes = load_similar_recipes()
    print('X_similar_recipes : ')
    print(X_similar_recipes)
    print('\n')

    df_recipes_info = load_informational_data()
    print('df_recipes_info : ')
    print(df_recipes_info)
    print('\n')

    df_similar = get_similar_recipes(recipe_id, df_recipes_info, X_similar_recipes, X_recipe_similarities, 10)
    print('df_similar : ')
    print(df_similar)
    print('\n')


