# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input('Name of Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME')).to_pandas()

# Convert the Snowpark DataFrame to a list for the multiselect widget
fruit_options = my_dataframe['FRUIT_NAME'].tolist()

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

if ingredient_list:
    # Concatenate selected ingredients into a string
    ingredients_string = ' '.join(ingredient_list)

    # Build a SQL Insert Statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered!', icon='✅')
