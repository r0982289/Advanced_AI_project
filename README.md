🧑‍🍳 Chefmate – Your AI-Powered Cooking Assistant
Chefmate is a smart recipe explorer that lets you search for delicious meals based on ingredients and dietary preferences. It uses AI to enhance your cooking journey with features like recipe translation, intelligent filtering, ingredient substitution suggestions, and beautiful recipe visualization.

🚀 Features
🔍 Ingredient-Based Recipe Search
Enter ingredients like chicken, tomatoes and get instant recipe recommendations.
🥦 Dietary Filters
Choose from preferences like Vegan, Vegetarian, or Low-Carb.
🌍 Multilingual Translation
Translate recipes into French, Spanish, or German using an LLM-based translator.
📷 Image Scraper
Automatically fetches high-quality images of the recipes from the web.
📊 Nutritional Info
View essential nutritional details: calories, carbs, fat, and protein.

🛠️ Tech Stack
Frontend: Streamlit

Backend/Logic: - pandas – for recipe data handling - BeautifulSoup – for scraping recipe images - requests – for API and web requests - nltk – for optional NLP tasks

AI Services:

- LLM (OpenAI or local) for text translation

Project structure:
Advanced_AI_project/
│
├── app/
│ └── app.py # Main Streamlit app
│
├── llm_services.py # Functions for translation (LLM)
├── recipe_search.py # Recipe filtering/search logic(NLP)
├── ingredientsub.ipynb
├── requirements.txt # Python dependencies
└── README.md

▶️ How to Run
Install dependencies - pip install -r requirements.txt

Launch the app - streamlit run app/app.py

Use the Interface

- Enter ingredients
- Select diet preference
- Browse recipes
- Translate selected recipe in the sidebar
- Incase of a need for a substitute ingredient, you can consult the substitue ingredients section in the sidebar

🧪 Example Use Case
Input: chicken, garlic, rice
Diet: Low-Carb
Action: Click "Find Recipes"
Bonus: Translate to Spanish in the sidebar
✅ You'll see cards with nutrition + translated steps!

👩‍💻 Authors - Rahmet Bahiru Kedir - Princess Blessing Darling
