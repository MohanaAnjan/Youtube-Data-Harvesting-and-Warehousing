
import os
import googleapiclient.discovery
import pandas as pd
import json
import datetime
import isodate 
import re
import streamlit as st
from streamlit import set_option
from datetime import datetime
from sqlalchemy import create_engine
import plotly.express as px
import pymysql

from function import *
from table import *

st.set_page_config(page_title="youtube",layout='wide',initial_sidebar_state='expanded')
#option menu
with st.sidebar:
    import streamlit as st

with st.sidebar:
    selected = st.selectbox("Select a Zone", ["Home", "Data Zone", "Analysis Zone", "Query Zone"], index=0)


#Home PAge
if selected=="Home":
    st.title(':blue[YOUTUBE DATA HARVESTING and WAREHOUSING using SQL and STREAMLIT]')
    st.markdown("## :red[Domain] : Social Media")
    st.markdown("## :red[Skills take away From This Project] : Python scripting, Data Collection, Streamlit, API integration, Data Management using SQL")
    st.markdown("## :red[Overall view] : Building a simple UI with Streamlit, retrieving data from YouTube API, storing the date SQL as a WH, querying the data warehouse with SQL, and displaying the data in the Streamlit app.")
    st.markdown("## :red[Developed by] : Mohana Anjan A V")




    
# Data Zone
elif selected == "Data Zone":
    tab1,tab2 = st.tabs(["$\huge COLLECT $", "$\huge MIGRATE $"])

    with tab1:
        st.markdown('## :red[Data collection zone]')
        st.write(
            '(**collects data** by using channel id and **stores it in the :orange[SQL] database**.)')
        channel_id = st.text_input('**Enter the channel_id**')
        st.write('''click below to retrieve and store data.''')
        Get_data = st.button('**Retrieve and store data**')

        # Define Session state to Get data button
        if "Get_state" not in st.session_state:
            st.session_state.Get_state = False
        if Get_data or st.session_state.Get_state:
            st.session_state.Get_state = True
            
            channel_df=channel_data(channel_id)
          
            p_id=get_playlist_name(channel_id)
            video_df=get_video_details(p_id)
           
            v_id=get_video_ids(p_id)
            comment_df=get_comment_detail(v_id)
        


    with tab2:
        
        st.markdown('## :blue[Data Migration zone]')
        st.write('''( **Migrates channel data to :green[MYSQL] database**)''')
        st.write('''Click below for **Data migration**.''')
        Migrate = st.button('**Migrate to MySQL**')
        if 'migrate_sql' not in st.session_state:
            st.session_state_migrate_sql = False
        if Migrate or st.session_state_migrate_sql:
            st.session_state_migrate_sql = True
            
            channel=channel_table(channel_df)
           
            video=videos_table(video_df)
           
            comments=comments_table(comment_df)
          
    
            Migrate=st.button('**Success**')

                
                    
   

#Analysis Zone                
if selected == "Analysis Zone":
    st.header(':blue[Channel Data Analysis zone]')
    st.write(
        '''(Checks for available channels by clicking this checkbox)''')
    # Check available channel data
    Check_channel = st.checkbox('**Check available channel data for analysis**')
    if Check_channel:
        # Create database connection
        engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/youtube")
                    # Execute SQL query to retrieve channel names
        query = "SELECT channel_name FROM channels;"
        results = pd.read_sql(query,engine)
            # Get channel names as a list
        channel_names_fromsql = list(results['channel_name'])
            # Create a DataFrame from the list and reset the index to start from 1
        sql_df = pd.DataFrame(channel_names_fromsql,columns=['Available channel data']).reset_index(drop=True)
            # Reset index to start from 1 instead of 0
        sql_df.drop_duplicates(inplace=True)
        sql_df.index += 1
            # Show dataframe
        st.dataframe(sql_df)

# QUERY ZONE
if selected == "Query Zone":
    st.subheader(':blue[Queries and Results ]')
    st.write('''(Queries were answered based on :orange[**Channel Data analysis**] )''')
    
    # Selectbox creation
    question_tosql = st.selectbox('Select your Question]',
                                  ('1. What are the names of all the videos and their corresponding channels?',
                                   '2. Which channels have the most number of videos, and how many videos do they have?',
                                   '3. What are the top 10 most viewed videos and their respective channels?',
                                   '4. How many comments were made on each video, and what are their corresponding video names?',
                                   '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                                   '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                                   '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                                   '8. What are the names of all the channels that have published videos in the year 2022?',
                                   '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                   '10. Which videos have the highest number of comments, and what are their corresponding channel names?'),
                                  key='collection_question')
    
       # Create a connection to SQL
    connect_for_question = pymysql.connect(host="127.0.0.1", user="root", passwd="1234", port=3306, db="youtube")
    cursor = connect_for_question.cursor()
    engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/youtube")

    # Q1
    if question_tosql == '1. What are the names of all the videos and their corresponding channels?':
        cursor.execute(''' SELECT video.channel_name,video.video_tittle FROM video ''')
        result_1 = cursor.fetchall()
        df1 = pd.DataFrame(result_1, columns=['Channel Name', 'Video Name']).reset_index(drop=True)
        df1.index += 1
        st.dataframe(df1)

    # Q2
    elif question_tosql == '2. Which channels have the most number of videos, and how many videos do they have?':

        col1, col2 = st.columns(2)
        with col1:
            cursor.execute("SELECT channels.channel_name, channels.channel_video_count FROM channels ORDER BY channel_video_count DESC;")
            result_2 = cursor.fetchall()
            df2 = pd.DataFrame(result_2, columns=['Channel Name', 'Video Count']).reset_index(drop=True)
            df2.index += 1
            st.dataframe(df2)

        with col2:
            fig_vc = px.bar(df2, y='Video Count', x='Channel Name', text_auto='.2s', title="Most number of videos", )
            fig_vc.update_traces(textfont_size=16, marker_color='#E6064A')
            fig_vc.update_layout(title_font_color='#1308C2 ', title_font=dict(size=25))
            st.plotly_chart(fig_vc, use_container_width=True)
       # Q3
    elif question_tosql == '3. What are the top 10 most viewed videos and their respective channels?':

        col1, col2 = st.columns(2)
        with col1:
            cursor.execute(
                "SELECT video.video_tittle, video.view_count, video.channel_name FROM video ORDER BY video.view_count DESC LIMIT 10;")
            result_3 = cursor.fetchall()
            df3 = pd.DataFrame(result_3, columns= ['Video Name', 'View count','Channel Name']).reset_index(drop=True)
            df3.index += 1
            st.dataframe(df3)

        with col2:
            fig_topvc = px.bar(df3, y='View count', x='Video Name', text_auto='.2s', title="Top 10 most viewed videos")
            fig_topvc.update_traces(textfont_size=16, marker_color='#E6064A')
            fig_topvc.update_layout(title_font_color='#1308C2 ', title_font=dict(size=25))
            st.plotly_chart(fig_topvc, use_container_width=True)

    # Q4
    elif question_tosql == '4. How many comments were made on each video, and what are their corresponding video names?':
        cursor.execute(
            "SELECT video.video_tittle, video.comment_count FROM video;")
        result_4 = cursor.fetchall()
        df4 = pd.DataFrame(result_4, columns=['Video Name', 'Comment count']).reset_index(drop=True)
        df4.index += 1
        st.dataframe(df4)

    # Q5
    elif question_tosql == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        cursor.execute(
            "SELECT video.channel_name, video.video_tittle, video.likecount FROM video ORDER BY video.likecount DESC;")
        result_5 = cursor.fetchall()
        df5 = pd.DataFrame(result_5, columns=['Channel Name', 'Video Name', 'Like count']).reset_index(drop=True)
        df5.index += 1
        st.dataframe(df5)

    # Q6
    elif question_tosql == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        st.write('**Note:- In November 2021, YouTube removed the public dislike count from all of its videos.**')
        cursor.execute(
            "SELECT video.channel_name, video.video_tittle, video.likecount ,video.dislike_count FROM video ORDER BY video.likecount DESC,video.dislike_count;")
        result_6 = cursor.fetchall()
        df6 = pd.DataFrame(result_6, columns=['Channel Name', 'Video Name', 'Like count','Dislike count' ]).reset_index(drop=True)
        df6.index += 1
        st.dataframe(df6)

    # Q7
    elif question_tosql == '7. What is the total number of views for each channel, and what are their corresponding channel names?':

        col1, col2 = st.columns(2)
        with col1:
            cursor.execute("SELECT channel_name,channel_views FROM channels ORDER BY channel_views DESC;")
            result_7 = cursor.fetchall()
            df7 = pd.DataFrame(result_7, columns=['Channel Name', 'Total number of views']).reset_index(drop=True)
            df7.index += 1
            st.dataframe(df7)

        with col2:
            fig_topview = px.bar(df7, y='Total number of views', x='Channel Name', text_auto='.2s',
                                 title="Total number of views", )
            fig_topview.update_traces(textfont_size=16, marker_color='#E6064A')
            fig_topview.update_layout(title_font_color='#1308C2 ', title_font=dict(size=25))
            st.plotly_chart(fig_topview, use_container_width=True)

    # Q8
    elif question_tosql == '8. What are the names of all the channels that have published videos in the year 2022?':
        cursor.execute('''
            SELECT video.channel_name, video.published_date 
                       FROM video WHERE EXTRACT(YEAR FROM published_date) = 2022''')
        result_8 = cursor.fetchall()
        df8 = pd.DataFrame(result_8, columns=['Channel Name', 'Year 2022 only']).reset_index(drop=True)
        df8.index += 1
        st.dataframe(df8)

     # Q9
    elif question_tosql == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        cursor.execute('''
              SELECT video.channel_name, AVG(video.video_duration) FROM video GROUP BY video.channel_name, video.video_duration
              ORDER BY AVG(video.video_duration) DESC ''')
        result_9 = cursor.fetchall()
        df9 = pd.DataFrame(result_9, columns=['Channel Name', 'Average duration of videos (HH:MM:SS)']).reset_index(drop=True)
        df9.index += 1
        st.dataframe(df9)

    # # Q10
    elif question_tosql == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        cursor.execute(
            "SELECT video.channel_name, video.video_tittle, video.comment_count FROM video ORDER BY video.comment_count DESC;")
        result_10 = cursor.fetchall()
        df10 = pd.DataFrame(result_10, columns=['Channel Name', 'Video Name', 'Number of comments']).reset_index(drop=True)
        df10.index += 1
        st.dataframe(df10)

    # SQL DB connection close
    connect_for_question.close()
    




                        
                        
                            
                    
                                        




    


















