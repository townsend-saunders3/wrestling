import streamlit as st
import json
from utils.wrestleClasses import *
import pickle

def create_match():
    player1 = next((player for player in athletes if player.name == st.session_state.create_player1), None)
    player2 = next((player for player in athletes if player.name == st.session_state.create_player2), None)
    tournament = st.session_state.create_tournament
    date = st.session_state.create_match_date
    match_round = st.session_state.create_round
    match = Match(
            player1=player1, 
            player2=player2,
            tournament=tournament,
            date=date,
            match_round=match_round,
            )
    matches.append(match)
    with open('files/matches/match.pkl', 'wb') as f:
            pickle.dump(matches, f)
    st.toast("New match added successfully!")
try:
    with open('files/athletes/players.pkl', 'rb') as f:
        athletes = pickle.load(f)
except FileNotFoundError:
    athletes = []

try:
    with open('files/matches/match.pkl', 'rb') as f:
        matches = pickle.load(f)
except FileNotFoundError:
    matches = []
st.title('Matches')
matches_df = pd.concat([match.get_match_df() for match in matches]).reset_index(drop = True)
st.dataframe(matches_df)


# st.divider()
# st.subheader('Edit Matches')
# with st.expander('Edit'):
#     select_match = st.selectbox('Select Match to Edit', matches_df.index)
#     if select_match:
#         edit_player1_name = st.selectbox('Player 1', [athlete.name for athlete in athletes], index= key = 'create_player1')
#         edit_player2_name = st.selectbox('Player 2', [athlete.name for athlete in athletes],  key = 'create_player2')
#         edit_tournament = st.text_input('Tournament Name',  key = 'create_tournament')
#         edit_date = st.date_input('Match Date',  key = 'create_match_date')
#         edit_round = st.text_input('Round',  key = 'create_round')
#         edit_winner = st.selectbox('Winner', [player1_name, player2_name], key = 'create_winner')
#         edit_loser = st.selectbox('Loser', [player1_name, player2_name], key = 'create_loser')
#         edit_submit = st.button('Submit', on_click=create_match)


st.divider()
st.subheader('Create New Match')
with st.expander('Create New'):
    player1_name = st.selectbox('Player 1', [athlete.name for athlete in athletes], key = 'create_player1')
    player2_name = st.selectbox('Player 2', [athlete.name for athlete in athletes],  key = 'create_player2')
    tournament = st.text_input('Tournament Name',  key = 'create_tournament')
    date = st.date_input('Match Date',  key = 'create_match_date')
    round = st.text_input('Round',  key = 'create_round')
    submit = st.button('Submit', on_click=create_match)
