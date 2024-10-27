import streamlit as st
import pandas as pd
from PIL import Image

# Load tweet data
data = pd.read_excel('Book1.xlsx')

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.cyberbullying_count = 0
    st.session_state.non_cyberbullying_count = 0

# Set custom CSS for a Tinder-like look
st.markdown("""
    <style>
        .tweet-card {
            background-color: #f9f9f9;
            padding: 20px;
            margin-top: 50px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            font-size: 20px;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .button-container {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .swipe-button {
            width: 130px;
            height: 40px;
            font-size: 16px;
            color: #fff;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .swipe-left {
            background-color: #ff5c5c;
        }
        .swipe-left:hover {
            background-color: #ff1e1e;
        }
        .swipe-right {
            background-color: #4CAF50;
        }
        .swipe-right:hover {
            background-color: #388e3c;
        }
    </style>
""", unsafe_allow_html=True)

# Display the current tweet
if st.session_state.index < len(data):
    tweet = data.iloc[st.session_state.index]["Tweet"]

    # Tweet card style
    st.markdown(f"<div class='tweet-card'>{tweet}</div>", unsafe_allow_html=True)

    # Buttons styled like Tinder swipe buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Swipe Left (Not Cyberbullying)", key="left", help="Mark as not cyberbullying"):
            if data.iloc[st.session_state.index]["Cyberbullying"] == False:
                st.session_state.non_cyberbullying_count += 1
            st.session_state.index += 1

    with col2:
        if st.button("Swipe Right (Cyberbullying)", key="right", help="Mark as cyberbullying"):
            if data.iloc[st.session_state.index]["Cyberbullying"] == True:
                st.session_state.cyberbullying_count += 1
            st.session_state.index += 1
else:
    # End of tweets
    st.write("End of Tweets! Thanks for participating.")
    st.write(f"Cyberbullying tweets identified: {st.session_state.cyberbullying_count}")
    st.write(f"Non-cyberbullying tweets identified: {st.session_state.non_cyberbullying_count}")
