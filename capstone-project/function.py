import googleapiclient.discovery
import pandas as pd
import re 
import datetime

api_service_name = "youtube"
api_version = "v3"
api_key='AIzaSyCCSBV9rVe2JzkkvMGBA0IZYfS5w3B4R3M'
youtube = googleapiclient.discovery.build(
api_service_name, api_version,developerKey=api_key)


def channel_data(channel_id):
    channel_data=[]
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    data={
        'channel_id' : channel_id,
        'channel_name':response['items'][0]['snippet'].get('title',None),
        'channel_description' :response['items'][0]['snippet']['description'],
        'channel_playlist_id':response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        'channel_view_count':response['items'][0]['statistics']['viewCount'],
        'channel_sub_count' :response['items'][0]['statistics']['subscriberCount'],
        'channel_video_count':response['items'][0]['statistics']['videoCount']
        }
    channel_data.append(data)

    return pd.DataFrame(channel_data)



#playlist id
def get_playlist_name(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id)
    response = request.execute()
    data=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return data




def to_seconds(duration): #eg P1W2DT6H21M32S
    week = 0
    day  = 0
    hour = 0
    min  = 0
    sec  = 0

    duration = duration.lower()

    value = ''
    for c in duration:
        if c.isdigit():
            value += c
            continue

        elif c == 'p':
            pass
        elif c == 't':
            pass
        elif c == 'w':
            week = int(value) * 604800
        elif c == 'd':
            day = int(value)  * 86400
        elif c == 'h':
            hour = int(value) * 3600
        elif c == 'm':
            min = int(value)  * 60
        elif c == 's':
            sec = int(value)

        value = ''

    return week + day + hour + min + sec


# get the play_list id through channel id #
def get_video_details(playlist_id):
        
    video_info=[]
    video_ids =[]
    next_page = None
    while True:
        playlist_request = youtube.playlistItems().list(
                                                part="snippet,contentDetails",
                                                maxResults=50,                      #max is the fuction for geting maximum results (50),default is 5#
                                                pageToken=next_page,                #pageToken is used for access more than 50results based on next page #
                                                playlistId=playlist_id )
        playlist_response = playlist_request.execute()
        for item in playlist_response['items']:
            video_ids.append(item['contentDetails']['videoId'])     
        next_page=playlist_response.get('nextPageToken')                            #The nextPageToken is a string value that is returned in the API response when the number of results exceeds the maxResults parameter value.#
        if next_page is None:                                                          # It can be used to request the next page of results by passing it in the pageToken parameter of the API request#
            break
    for video_id in video_ids:
        video_request = youtube.videos().list(
                                        part="contentDetails,snippet,statistics,status",
                                        id=video_id
                                        )
        video_response = video_request.execute()
        data={
        'channel_name':video_response['items'][0]['snippet']['channelTitle'],
        'video_id' : video_id,
        'video_tittle':video_response['items'][0]['snippet']['title'],
        'video_Description':video_response['items'][0]['snippet'].get('description'), 
        #'video_tag' :','.join(video_response['items'][0]['snippet'].get('tags',['NA])),                                  #'video_tags': video_response['items'][0]['snippet].get('tags', [])#
        'published_date':video_response['items'][0]['snippet'].get('publishedAt',None).replace('Z',''),                            # get results if the key is present in dict it gives otherwise it gives none --for avoiding key error#
        'view_count': int(video_response['items'][0]['statistics'].get('viewCount',0)),
        'likecount':int( video_response['items'][0]['statistics'].get('likeCount',0)),
        'dislike_count':int(video_response['items'][0]['statistics'].get('dislikeCount',0)),
        'comment_count':int(video_response['items'][0]['statistics'].get('commentCount',0)),
        'video_favourite_count':int(video_response['items'][0]['statistics'].get('favoriteCount',0)),
        'video_thumbnails':video_response['items'][0]['snippet']['thumbnails']['default']['url'],                   ## Convert thumbnails dict to JSON string
        'video_caption':video_response['items'][0]['contentDetails']['caption'],
        'video_duration': int(to_seconds(video_response['items'][0]['contentDetails'].get('duration', "PT0S"))),
        }
        video_info.append(data)
    return pd.DataFrame(video_info)




#get Video ids
def get_video_ids(playlist_id):
    video_ids =[]
    next_page = None
    while True:
        playlist_request = youtube.playlistItems().list(
                                                part="snippet,contentDetails",
                                                maxResults=50,                      #max is the fuction for geting maximum results (50),default is 5#
                                                pageToken=next_page,                #pageToken is used for access more than 50results based on next page #
                                                playlistId=playlist_id )
        playlist_response = playlist_request.execute()
        for item in playlist_response['items']:
            video_ids.append(item['contentDetails']['videoId'])     
        next_page=playlist_response.get('nextPageToken')                            #The nextPageToken is a string value that is returned in the API response when the number of results exceeds the maxResults parameter value.#
        if next_page is None:                                                          # It can be used to request the next page of results by passing it in the pageToken parameter of the API request#
            break
    return video_ids



def conversion(input_string):
    pattern = r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z'           # Define regular expression pattern
    match = re.match(pattern, input_string)                                 # Match the pattern
    if match:
        year, month, day, hour, minute, second = match.groups()             # Extract matched groups
        dt_obj = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))   # Convert to datetime object
        return dt_obj
    else:
        print("Invalid datetime string format.")
    return None 
    
#comment Details
def get_comment_detail(video_ids):
    all_comments=[]
    try:
        for video_id in video_ids:
            request = youtube.commentThreads().list(
                        part="snippet,replies",
                        videoId=video_id,
                        maxResults=50  # Maximum number of comments to retrieve per request
                        )
            response = request.execute()
            for i in range (len(response)):
                id=response['items'][i]['id']
                text=response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
                Auther=response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
                publish=conversion(response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'])
                data={"video_id":video_id,
                            "comment_id":id,
                            "comment_text":text,
                            "comment_Auther":Auther,
                            "comment_publish":publish}
                all_comments.append(data)
                        
    except:
        pass
    return pd.DataFrame(all_comments)
