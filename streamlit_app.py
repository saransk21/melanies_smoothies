# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want to include in your custom smoothie!
    """
)


# option = st.selectbox(
#     'What Is Your Favorite Fruit?',
#     ('Banana', 'Straberries', 'Peaches'))

# st.write('Your favorite fruit is:', option)
# --------------select----------------
name_on_order = st.text_input('Name on Smoothie')
st.write('The Name on Smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 integredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list);
    # st.text(ingredients_list);
    
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string +=each_fruit+' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                values ('""" + ingredients_string + """','""" + name_on_order  + """')"""
    
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
