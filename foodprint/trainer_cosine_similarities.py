import pandas as pd
import numpy as np
import json
import os
from helper import load_data, load_data_im2recipe
from trainer_neighbors import add_random_co2_data, convert_to_dict, save_processed_data
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from food_extractor.food_model import FoodModel
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def get_data(cache_data=True, add_random_co2=False):
    if cache_data:
        df_im2recipe = pickle.load(open('../foodprint/cached_data/cached_im2recipe.pickle','rb'))
        df_yummly = pd.DataFrame()
    else:
        df_yummly = load_data_yummly(recipes_folder='./data/sample_recipes/')
        df_im2recipe = load_data_im2recipe(recipes_folder='./data/sample_im2recipes/')
    
    df = pd.concat([df_yummly, df_im2recipe]).reset_index(drop=True)
    
    if add_random_co2:
        df = add_random_co2_data(df)
    
    return df

def pipeline():
    pipe = Pipeline([
        ('dict_vectorizer', DictVectorizer(sparse=False))
    ])
    return pipe

def get_processed_data():
    df = get_data()
    df['bow'] = df.ingredients.apply(convert_to_dict)
    pipe = pipeline()
    X_recipes = pipe.fit_transform(df.bow.tolist())
    return (df, X_recipes)

def get_recipe_similarities(X_recipes):
    X_recipes_float32 = np.float32(X_recipes)
    similarities = cosine_similarity(X_recipes_float32)
    return similarities

def sort_similarities(similarities):
    index_start = 0
    index_end = similarities.shape[0]
    n_similar = 11

    X_recipe_similarities = np.zeros((index_end,11))
    X_similar_recipes = np.zeros((index_end,11))
    
    for i in range(index_start, index_end):
        X_similar = similarities[:,i]
        X_recipe_similarities[i] = np.sort(-X_similar)[:n_similar]
        X_similar_recipes[i] = np.argsort(-X_similar)[:n_similar]
    return (X_recipe_similarities, X_similar_recipes)


def save_recipe_similarities(X_recipe_similarities):
    with open("../foodprint/cached_data/cached_recipe_similarities.pickle", "wb") as file:
        pickle.dump(X_recipe_similarities, file)

def save_similar_recipes(X_similar_recipes):
    with open("../foodprint/cached_data/cached_similar_recipes.pickle", "wb") as file:
        pickle.dump(X_similar_recipes, file)


if __name__ == '__main__':
    (df_cleaned, X_recipes) = get_processed_data()
    print('df_cleaned : ')
    print(df_cleaned)
    print('\n')
    print('\n')

    print('X_recipes : ')
    print(X_recipes)
    print('\n')

    print('X_recipes.shape : ')
    print(X_recipes.shape)
    print('\n')

    save_processed_data(df_cleaned, X_recipes)
    recipe_similarities = get_recipe_similarities(X_recipes)
    print('recipe_similarities : ')
    print(recipe_similarities)
    print('\n')

    print('recipe_similarities[:,1] : ')
    print(recipe_similarities[:,1])
    print('\n')

    X_recipe_similarities, X_similar_recipes = sort_similarities(similarities)
    
    save_recipe_similarities(X_recipe_similarities)
    
    save_similar_recipes(X_similar_recipes)
