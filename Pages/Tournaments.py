import streamlit as st
import json
from utils.wrestleClasses import *

import pickle
try:
    with open('files/athletes/players.pkl', 'rb') as f:
        athletes = pickle.load(f)
except FileNotFoundError:
    athletes = []