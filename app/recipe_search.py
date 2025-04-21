# recipe_search.py
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from tqdm import tqdm
import pickle

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


df = pd.read_csv("data/recipes.csv")


def preprocess_ingredients(text):
    if isinstance(text, str) and text.startswith('['):
        text = ' '.join(eval(text))
    words = word_tokenize(str(text).lower())
    filtered = [word for word in words 
               if word.isalpha() 
               and word not in stop_words
               and len(word) > 2]
    return " ".join(filtered)


tqdm.pandas()
df['processed'] = df['ingredients'].progress_apply(preprocess_ingredients)


vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.8
)
X = vectorizer.fit_transform(df['processed'])


df.to_pickle("data/processed_recipes.pkl")
with open("data/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)


def search_recipes(query, diet=None, max_calories=None, top_n=5):
    try:
        processed_query = preprocess_ingredients(query)
        query_vec = vectorizer.transform([processed_query])
        
        mask = pd.Series(True, index=df.index)
        if diet:
            mask &= df['diet_type'].str.lower().str.contains(diet.lower(), na=False)
        if max_calories:
            mask &= df['calories'] <= max_calories
        
        #  to check if any recipes match the filters
        if not mask.any():
            return pd.DataFrame(columns=df.columns.tolist() + ['similarity'])
        
        essential_cols = [
        'name', 
        'ingredients',
        'directions',
        'prep',
        'cook',
        'servings',
        'calories',
        'diet_type',
        'url' 
        ]
        # Compute similarity scores for filtered recipes
        sim_scores = cosine_similarity(query_vec, X[mask]).flatten()
        top_indices = sim_scores.argsort()[-top_n:][::-1]  # Get top N indices
        
        results = df[mask].iloc[top_indices][essential_cols].copy()
        results['similarity'] = sim_scores[top_indices]
        return results
        
    except Exception as e:
        print(f"Search error: {e}")
        return pd.DataFrame(columns=df.columns.tolist() + ['similarity'])