import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl

# Load tweet data
data = pd.read_excel('Book1.xlsx')

# Initialize session state for index and log
if "index" not in st.session_state:
    st.session_state.data_shuffled = data.sample(frac=1).reset_index(drop=True)
    st.session_state.index = 0

# Define the log file
log_file = 'swipe_log.xlsx'

# Function to log user's swipe action in a new sheet
def log_swipe_to_excel(tweet, is_cyberbullying):
    log_entry = pd.DataFrame({
        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'Tweet': [tweet],
        'Cyberbullying': [is_cyberbullying]
    })
    try:
        with pd.ExcelWriter(log_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            log_entry.to_excel(writer, sheet_name="Log", index=False, header=False, startrow=writer.sheets["Log"].max_row)
    except FileNotFoundError:
        with pd.ExcelWriter(log_file, engine="openpyxl") as writer:
            log_entry.to_excel(writer, sheet_name="Log", index=False)

# Responsive CSS styling
st.markdown("""
    <style>
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .tweet-card {
            background-color: #f9f9f9;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            font-size: 18px;
            text-align: center;
            font-family: Arial, sans-serif;
            width: 100%;
            max-width: 400px;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 400px;
            margin-top: 20px;
        }
        .swipe-button {
            flex: 1;
            margin: 5px;
            padding: 10px;
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

st.markdown("<div class='container'>", unsafe_allow_html=True)

# Display the current tweet
if st.session_state.index < len(st.session_state.data_shuffled):
    tweet = st.session_state.data_shuffled.iloc[st.session_state.index]["Tweet"]
    st.markdown(f"<div class='tweet-card'>{tweet}</div>", unsafe_allow_html=True)

    # Button container
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Swipe Left (Not Cyberbullying)", key="left", help="Mark as not cyberbullying"):
            log_swipe_to_excel(tweet, False)
            st.session_state.index += 1

    with col2:
        if st.button("Swipe Right (Cyberbullying)", key="right", help="Mark as cyberbullying"):
            log_swipe_to_excel(tweet, True)
            st.session_state.index += 1

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.write("End of Tweets! Thanks for participating.")

st.markdown("</div>", unsafe_allow_html=True)
