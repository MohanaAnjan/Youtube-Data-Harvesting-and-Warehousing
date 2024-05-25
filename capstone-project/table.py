import pymysql
mydb = pymysql.connect(host="127.0.0.1", user="root", passwd="1234", port=3306,database="youtube")

mycursor = mydb.cursor()


mycursor.execute("create database if not exists youtube")
mycursor.execute("use youtube")
#creating channel table#
mycursor.execute("""create table if not exists channels(
                    channel_id VARCHAR(255) PRIMARY KEY,
                    channel_name VARCHAR(255),
                    channel_description TEXT,
                    channel_playlist_id VARCHAR(255),
                    channel_views INT,
                    channel_subscribers INT,
                    channel_video_count INT)
                """)
def channel_table(channel_df):
    # df=channel_detail
    for index,row in channel_df.iterrows():
        sql='''insert into channels( channel_id,
                    channel_name,
                    channel_description,
                    channel_playlist_id,
                    channel_views,
                    channel_subscribers,
                    channel_video_count) values(%s,%s,%s,%s,%s,%s,%s)'''
        values=tuple(row)
        # Execute the SQL query
        mycursor.execute(sql,values)
        mydb.commit()
    
    return "SUCCESSFULLY INSERTED"

 #creating videos table#
mycursor.execute("""create table if not exists video(channel_name VARCHAR(255), 
                video_id VARCHAR(255) PRIMARY KEY,
                video_tittle TEXT, 
                video_Description TEXT,
                published_date DATETIME,
                view_count INT, 
                likecount INT,
                dislike_count INT,
                comment_count INT,
                video_favourite_count INT,
                video_thumbnails TEXT,
                video_caption VARCHAR(255),
                video_duration INT )""")



def videos_table(video_df):    
    for index, row in video_df.iterrows():
        sql='''insert into video(channel_name,
        video_id,
        video_tittle,
        video_Description,
        published_date,
        view_count,
        likecount,
        dislike_count,
        comment_count,
        video_favourite_count,
        video_thumbnails,
        video_caption,
        video_duration) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        values = (
                row['channel_name'],
                row['video_id'],
                row['video_tittle'],
                row['video_Description'],
                row['published_date'],
                row['view_count'],
                row['likecount'],
                row['dislike_count'],
                row['comment_count'],
                row['video_favourite_count'],
                row['video_thumbnails'],
                row['video_caption'],
                row['video_duration'])
        mycursor.execute(sql, values)
        mydb.commit()
    return "SUCCESSFULLY INSERTED"




mycursor.execute("""create table if not exists comments( video_id VARCHAR(255),
                comment_id VARCHAR(255) PRIMARY KEY,
                comment_text TEXT,
                comment_Auther TEXT,
                comment_publish TEXT
                )""")

def comments_table(comment_df):
    for index,row in comment_df.iterrows():
        sql="""insert  into comments(video_id,comment_id,comment_text,comment_Auther,comment_publish)
        values(%s,%s,%s,%s,%s)"""
        values=(row['video_id'],
                row['comment_id'],
                row['comment_text'],
                row['comment_Auther'],
                row['comment_publish'])
        mycursor.execute(sql, values)
        mydb.commit()
    return "SUCCESSFULLY INSERTED"

         
            
