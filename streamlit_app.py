import streamlit
import pandas as pd
import requests as req
import snowflake.connector # will tell your app to bring in codes from snowflake library you added (snowflake-connector-python)

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

# add a text entry box
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
# send the input above to Fruityvice as API call
streamlit.write('The user entered', fruit_choice)

fruityvice_response = req.get('https://fruityvice.com/api/fruit/' + fruit_choice) # separate url base vs. variable (fruit name)
# streamlit.text(fruityvice_response.json()) # writes the data to the screen
fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) # take the json version of the response and normalize it

# Display the table on page
streamlit.dataframe(fruityvice_normalized) 

# query snowflake account metadata
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# query some other data instead
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
