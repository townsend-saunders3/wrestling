import streamlit as st
import json
from utils.wrestleClasses import *
import pickle

try:
    with open('files/athletes/players.pkl', 'rb') as f:
        athletes = pickle.load(f)
except FileNotFoundError:
    athletes = []

athletes_df = pd.concat([player.get_player_df() for player in athletes])

def update_player():
    selected_player = next((player for player in athletes if player.name == st.session_state.edit_player), None)
    selected_player.name = st.session_state.edit_name
    selected_player.weight = st.session_state.edit_weight
    selected_player.club = st.session_state.edit_club
    selected_player.country = st.session_state.edit_country

    # Update the pickle file
    with open('files/athletes/players.pkl', 'wb') as f:
        pickle.dump(athletes, f)
    st.toast("Player information updated successfully!")

def add_player():
    athlete_name = st.session_state['add_name']
    athlete_weight = st.session_state['add_weight']
    athlete_club = st.session_state['add_club']
    athlete_country = st.session_state['add_country']
    athlete = Player(athlete_name, athlete_weight, athlete_club, athlete_country)
    try:
        with open('files/athletes/players.pkl', 'rb') as f:
            athletes = pickle.load(f)
    except FileNotFoundError:
        athletes = []

    if any(player.name == athlete_name for player in athletes):
            st.toast("A player with this name already exists.")
    else:
        athletes.append(athlete)
        # Update the pickle file
        with open('files/athletes/players.pkl', 'wb') as f:
            pickle.dump(athletes, f)
        st.toast("New player added successfully!")


st.title('Athletes')
st.dataframe(athletes_df.reset_index(drop = True))
country_list = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

player_names = [player.name for player in athletes]
st.divider()
st.subheader('Edit Athlete')
with st.expander('Edit'):
    selected_player_name = st.selectbox("Select Athlete", player_names, key = 'edit_player')
    selected_player = next((player for player in athletes if player.name == selected_player_name), None)
    if selected_player:
        with st.form("Edit Player Form"):
            edit_player_name = st.text_input("Edit player's name", selected_player.name, key = 'edit_name')
            edit_player_weight = st.text_input("Edit player's weight",selected_player.weight, key = 'edit_weight')
            edit_player_club = st.text_input("Edit player's club", selected_player.club, key = 'edit_club')
            edit_player_country = st.selectbox("Edit player's country",country_list,  country_list.index(selected_player.country), key = 'edit_country')
            edit_submitted = st.form_submit_button(on_click=update_player)

st.divider()
st.subheader('Create New Athlete')
with st.expander('Create New'):
    with st.form('New Player Form'):
        athlete_name = st.text_input('Name', key = 'add_name')
        athlete_weight = st.text_input('Weight Kg', key = 'add_weight')
        athlete_club = st.text_input('Club', key = 'add_club')
        athlete_country = st.selectbox('Country', country_list, key = 'add_country')
        submit = st.form_submit_button(on_click = add_player)





