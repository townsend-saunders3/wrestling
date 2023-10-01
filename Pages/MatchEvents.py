import streamlit as st
import json
from utils.wrestleClasses import *
import pickle

try:
    with open('files/matches/match.pkl', 'rb') as f:
        matches = pickle.load(f)
except FileNotFoundError:
    matches = []

select_match_id = st.selectbox('Select Match', [match.match_id for match in matches])
select_match: Match = next((match for match in matches if match.match_id == select_match_id), None)

events = select_match.events
events

st.divider()
with st.expander('Add Attack'):
    st.
