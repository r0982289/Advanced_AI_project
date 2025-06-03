import streamlit as st
from recipe_search import search_recipes
import requests
from PIL import Image
from io import BytesIO
import re
from bs4 import BeautifulSoup
from llm_services import translate_text


# css
st.markdown("""
<style>
.recipe-card {
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    background-color: #f9f9f9;
}
.recipe-title {
    font-size: 1.5rem;
    color: #2e7d32;
}
.nutrition-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 12px;
    background-color: #e8f5e9;
    margin-right: 5px;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)


def get_allrecipes_image(url):
    """Fetch the high-quality recipe image by scraping the page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple image sources
        img_src = (
            soup.find('meta', property='og:image') or
            soup.find('meta', attrs={'name': 'twitter:image'}) or
            soup.find('img', class_=re.compile('image.*img.*recipe', re.I))
        )

        if img_src:
            img_url = img_src.get('content') or img_src.get('src')
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            return img_url
    except Exception as e:
        print(f"Image fetch error: {e}")
    return None


def display_recipe(recipe):
    """Display a recipe card with image and selection button"""
    with st.container():
        st.markdown(f"<div class='recipe-card'>", unsafe_allow_html=True)


        img_url = get_allrecipes_image(recipe['url'])
        if img_url:
            try:
                response = requests.get(img_url, stream=True, timeout=10)
                if response.status_code == 200:
                    st.markdown(
                        f'<img src="{img_url}" class="recipe-image" width="100%">',
                        unsafe_allow_html=True
                    )
            except:
                pass

        st.subheader(recipe['name'])

        
        cols = st.columns(4)
        cols[0].metric("Prep", recipe['prep'] or "N/A")
        cols[1].metric("Cook", recipe['cook'] or "N/A")
        cols[2].metric("Servings", recipe['servings'] or "N/A")
        cols[3].metric("Calories", recipe['calories'] or "N/A")

        with st.expander("Nutrition Info"):
            st.markdown(f"""
            **Calories:** {recipe['calories']}  
            **Protein:** {recipe.get('protein_g', 'N/A')}g  
            **Carbs:** {recipe.get('carbohydrates_g', 'N/A')}g  
            **Fat:** {recipe.get('fat_g', 'N/A')}g
            """)

      
        tab1, tab2 = st.tabs(["Ingredients", "Directions"])
        with tab1:
            st.write(recipe['ingredients'])
        with tab2:
            st.write(recipe['directions'])

        if st.button(f"Select: {recipe['name']}"):
            st.session_state.selected_recipe = recipe
            st.success("Recipe selected!")
            return True

        st.markdown("</div>", unsafe_allow_html=True)

    return False

# Measurement Conversion Functions
def metric_to_us_cups(metric_ml):
    return metric_ml / 240  # 1 US cup = 240ml

def us_to_metric_cups(us_cups):
    return us_cups * 240  # 1 US cup = 240ml

# UI for Measurement Converter
def measurement_converter_ui():
    st.sidebar.markdown("### 🧪 Measurement Converter")
    conversion_direction = st.sidebar.radio("Convert from:", ["Belgian (Metric) to U.S.", "U.S. to Belgian (Metric)"])
    cups_input = st.sidebar.number_input("Enter number of cups:", min_value=0.0, step=0.1, format="%.2f")

    if conversion_direction == "Belgian (Metric) to U.S.":
        converted = metric_to_us_cups(cups_input * 250)  # Belgian cup = 250 ml
        st.sidebar.write(f"≈ **{converted:.2f} U.S. cups**")
    else:
        converted = us_to_metric_cups(cups_input)
        st.sidebar.write(f"≈ **{converted / 250:.2f} Belgian cups** (or {converted:.0f} ml)")


# Main 
st.title("🍳 Chefmate")
query = st.text_input(
    "Search recipes by ingredients (e.g., chicken, potatoes):")
diet = st.selectbox("Dietary Preference", [
                    "Any", "Vegetarian", "Vegan", "Low-Carb"])


# Initialize session state to store selected recipe
if 'selected_recipe' not in st.session_state:
    st.session_state.selected_recipe = None

# Initialize storage for results
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

if st.button("Find Recipes"):
    if query:
        with st.spinner("Searching recipes..."):
            results = search_recipes(
                query,
                diet=diet if diet != "Any" else None
            )
            if results.empty:
                st.warning("No recipes found. Try different ingredients!")
                st.session_state.search_results = None
            else:
                st.session_state.search_results = results
    else:
        st.warning("Please enter some ingredients")

# Display search results after button press (persisted)
if st.session_state.search_results is not None:
    st.success(f"Found {len(st.session_state.search_results)} recipes")
    for _, recipe in st.session_state.search_results.iterrows():
        display_recipe(recipe) 

    else:
        st.warning("Please enter some ingredients")

if st.sidebar.checkbox("Translate Recipe"):
    if st.session_state.get("selected_recipe") is not None:
        language = st.sidebar.selectbox(
            "Select Language", ["French", "German"])

        with st.spinner("Translating..."):
            recipe = st.session_state.selected_recipe
            title_translated = translate_text(recipe['name'], language)
            ingredients_translated = translate_text(
                recipe['ingredients'], language)
            directions_translated = translate_text(
                recipe['directions'], language)

        st.sidebar.markdown("### 🔤 Translated Recipe")
        st.sidebar.write(f"**Title**: {title_translated}")
        st.sidebar.write(f"**Ingredients**: {ingredients_translated}")
        st.sidebar.write(f"**Directions**: {directions_translated}")
    else:
        st.sidebar.warning("Please select a recipe first.")

# Measurement Converter UI
measurement_converter_ui()
