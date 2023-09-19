import streamlit
import pandas as pd
import requests as req

# First part of the new menu
streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Import txt file
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on page
streamlit.dataframe(fruits_to_show)

# New section to display Fruity Vice API response
streamlit.header('Fruityvice Fruit Advice!')

fruityvice_response = req.get('https://fruityvice.com/api/fruit/' + 'kiwi') # separate url base vs. variable (fruit name)
# streamlit.text(fruityvice_response.json()) # writes the data to the screen
fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) # take the json version of the response and normalize it

# Display the table on page
streamlit.dataframe(fruityvice_normalized) 
