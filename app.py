import streamlit as st
import openai
from datetime import datetime
from streamlit.components.v1 import html
import pandas as pd
import csv
st.set_page_config(page_title="Frisch Menu Meal Maker")


html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

# button = """
# <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="nainiayoub" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
# """


with st.sidebar:
    st.markdown("""
    # About 
    Frisch Menu Meal Maker is a helper tool built on GPT-3 to give you menu suggestions based on your needs. 
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work
    Choose your dietary and monetary restrictions and we'll give you some meal suggestions
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)


# input_text = None
# if 'output' not in st.session_state:
#     st.session_state['output'] = 0

# if st.session_state['output'] <=2:
#     st.markdown("""
#     # Frisch Menu Meal Maker
#     """)
#     input_text = st.text_input("Brainstorm ideas for", disabled=False, placeholder="What's on your mind?")
#     st.session_state['output'] = st.session_state['output'] + 1

#     ##make a check box form for dietary restrictions
#     st.markdown("""
#     # Dietary Restrictions
#     """)
#     st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
#     st.markdown("""
#     ## Select all that apply
#     """)


# else:
#     # input_text = st.text_input("Brainstorm ideas for", disabled=True)
#     st.info("Thank you! Refresh for more brainstorming💡")

# hide="""
# <style>
# footer{
# 	visibility: hidden;
#     position: relative;
# }
# .viewerBadge_container__1QSob{
#     visibility: hidden;
# }
# #MainMenu{
# 	visibility: hidden;
# }
# <style>
# """
# st.markdown(hide, unsafe_allow_html=True)

st.title("Dietary and Financial Restrictions")

st.header("Menu")
menu = st.text_area("Enter the menu items here:")


st.header("Dietary Restrictions")
gluten_free = st.checkbox("Gluten-Free")
dairy_free = st.checkbox("Dairy-Free")
nut_free = st.checkbox("Nut-Free")

st.header("Financial Restrictions")
price_range = st.radio("Choose your budget:", ("< $5", "$5-$10", "$10-$15"))

if st.button("Submit"):
    dietary_restrictions = {
        "gluten_free": gluten_free,
        "dairy_free": dairy_free,
        "nut_free": nut_free
    }

    st.write("Your dietary restrictions:")
    st.write(dietary_restrictions)

    st.write("Your financial restrictions:")
    st.write(price_range)


if menu:
    prompt = "I am going to provide you a food menu and list of dietary and monetary restrictions, can you help me decide on a meal. Dietary restrictions: "+str(dietary_restrictions)+", financial restrictions: "+str(price_range)+"\n Menu: " +str(menu)
    if prompt:
        openai.api_key = st.secrets["openaiKey"]
        response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=150)
        meal_output = response['choices'][0]['text']
        today = datetime.today().strftime('%Y-%m-%d')
        meal = response
        
        st.info(meal_output)
        filename = "brainstorming_"+str(today)+".txt"
        btn = st.download_button(
            label="Download txt",
            data=meal,
            file_name=filename
        )
        fields = [prompt, meal_output, str(today)]
        # read local csv file
        r = pd.read_csv('./data/prompts.csv')
        if len(fields)!=0:
            with open('./data/prompts.csv', 'a', encoding='utf-8', newline='') as f:
                # write to csv file (append mode)
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(fields)

        
        

        
