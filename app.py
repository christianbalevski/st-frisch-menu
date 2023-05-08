import streamlit as st
import openai
from datetime import datetime
from streamlit.components.v1 import html
# import pandas as pd
# import csv
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

# Set up the OpenAI API
openai.api_key = st.secrets["openaiKey"]

def generate_messages(menu, dietary_restrictions, price_range):
    messages = [
        {"role": "system", "content": "You are a helpful meal planning assistant. Make sure you follow the instructions carefully including gluten restrictions."},
        {"role": "user", "content": f"Given a menu with the following items:\n{menu}\n Other menu options to include pizza - $2.50 \n gluten free pizza - $6.00 \n salad bar - price varies \n sushi gluten free, $8.50 \n\n. Find suitable options for someone with these dietary restrictions: {', '.join([k for k, v in dietary_restrictions.items() if v])} and within this total budget: {price_range}. Do not apologise, do not refrence past responses. Just give the meal suggestions."},
        {"role": "assistant", "content": "The output should be in table format with the following columns: item, price, dietary restrictions, with total price for the meal at the bottom. Items not gluten free include: pasta, mac & cheese, couscous, toast, impossible burger, salmon burger, cheese quesadilla."},
    ]
    return messages

def call_openai_api(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message['content']

def format_response(response):
    # Replace unwanted characters and split the response into lines
    lines = response.replace("−", "-").split("\n")

    # Clean up the lines by removing any extra spaces and empty lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Join the cleaned lines with line breaks and return the formatted response as a Markdown string
    return "    \n".join(cleaned_lines)

def main():
    st.title("Dietary and Financial Restrictions")

    st.header("Menu")
    menu = st.text_area("Enter the menu items here:")

    st.header("Dietary Restrictions")
    gluten_free = st.checkbox("Gluten-Free")
    dairy_free = st.checkbox("Dairy-Free")
    nut_free = st.checkbox("Nut-Free")
    vegan = st.checkbox("Vegan")

    st.header("Financial Restrictions")
    price_range = st.radio("Choose your budget:", ("< $5", "$5-$10", "$10-$15"))

    if st.button("Submit"):
        dietary_restrictions = {
            "gluten_free": gluten_free,
            "dairy_free": dairy_free,
            "nut_free": nut_free,
            "vegan": vegan
        }

        prompt = generate_messages(menu, dietary_restrictions, price_range)
        st.write("Generated prompt for GPT-3.5:")
        # st.write(prompt)

        st.write("Calling GPT-3.5 Turbo...")
        response = call_openai_api(prompt)

        # formatted_response = format_response(response)
        st.markdown("Formatted GPT-3.5 Turbo response:")
        st.markdown(response)

if __name__ == "__main__":
    main()