import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from wrestle_utils import *
df = pd.read_csv('wrestleStats.csv')
header_cols = st.columns(3)
st.header('Dominique Parrish')
# with st.expander('Key Stats'):

#     st.dataframe(df)
df['Offense_Defense'] = ['Defense' if 'Defense' in x else 'Offense' for x in df.Player_Move]
df['Opponent_Countered'] = (df['Match_ID'].shift(-1) == df['Match_ID']) & (df.Type.shift(-1) == 'Reattack') & (df.Opponent_Points.shift(-1) > 0)
df.Player_Success = df.Player_Success.astype(bool)
df.Win_Loss = df.Win_Loss.astype(bool)
df = df.sort_values(by = ['Date', 'Match_Day_Order', 'Period', 'Clock'], ascending=[True, True, True, False])


select_boxes = {}
use_filter = {}
sidebar_containers = {}
with st.sidebar:
    st.title('Filters')
    for column in df.columns:
        sidebar_cols = st.columns(2, gap = 'small')
        with sidebar_cols[0]:
            use_filter[column] = st.toggle(column, key = column + '_filter')
        with sidebar_cols[1]:
            select_boxes[column] = st.selectbox(column, df[column].unique(), label_visibility='collapsed')



for column in select_boxes.keys():
    if use_filter[column]:
        selection = select_boxes[column]
        df = df[df[column] == selection]
        if column == 'URL':
            if selection != 'Unknown':
                with st.expander('Video'):
                    st.video(selection)
"Key Statistics"
"Shot Accuracy: "
df[(df.Offense_Defense == 'Offense') & (df.Player_Success == True)].shape[0]/df[df.Offense_Defense == 'Offense'].shape[0]
"Total Shots Taken"
df[df.Offense_Defense == 'Offense'].shape[0]
"Total Shots Landed"
df[(df.Offense_Defense == 'Offense') & (df.Player_Success == True)].shape[0]
"Opponents Shots Taken"
df[df.Offense_Defense == 'Defense'].shape[0]
"Opponents Shots Defended"
df[(df.Offense_Defense == 'Defense') & (df.Player_Success == True)].shape[0]
"Opponents Shots Landed"
df[(df.Offense_Defense == 'Defense') & (df.Player_Success == False)].shape[0]
'Aggressiveness Rating'
df[df.Offense_Defense == 'Offense'].shape[0]/df[df.Offense_Defense == 'Defense'].shape[0]
'Offensive Effectiveness Rating'
(df[(df.Offense_Defense == 'Offense') & (df.Player_Success == True)].shape[0]+1)/(df[(df.Offense_Defense == 'Defense') & (df.Player_Success == False)].shape[0]+1)
tab1, tab2 = st.tabs(['Summary Stats', 'Data Table'])
with tab2:
    st.dataframe(df)
with tab1:
    summary_stats = get_summary_stats(df, 'Player_Move', ['Player_Success', 'Player_Points'])
    st.dataframe(summary_stats)
    # for move in df.Player_Move.unique:


dfGraphs = pd.DataFrame(df.groupby('Player_Move').agg({
    'Player_Success': lambda x: list(x),
    'Player_Points' : lambda x: list(x),
    }))
dfGraphs['Player_Success_Chart'] = dfGraphs['Player_Success']
dfGraphs['Player_Points_Chart'] = dfGraphs['Player_Points']
st.dataframe(dfGraphs, column_config={
    "Player_Success_Chart": st.column_config.LineChartColumn(
            "Player Move Succcess Chart",
            width="medium",
         ),
    "Player_Points_Chart": st.column_config.LineChartColumn(
            "Player Points Chart",
            width="medium",
         )
})
# best_move = st.button('Best Move')


# if best_move:
#     for move in df.Player_Move

# st.dataframe(df)

