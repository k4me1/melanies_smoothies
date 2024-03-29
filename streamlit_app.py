# Import python packages
import streamlit as st

cnx=st.connexion("snowflake")
session=cnx.session()

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:");
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)
from snowflake.snowpark.functions import col
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
NAME_ON_ORDER =st.text_input('Name on Smoothie')

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5 )

sub_but=st.button('Submit Order')
if sub_but:
    ingredients_string=''
    for i in ingredients_list:
        ingredients_string += i +' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
                values ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""

    
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+NAME_ON_ORDER+'!', icon="✅")
