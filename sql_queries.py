import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE staging_events(
    artist_name VARCHAR,
    auth VARCHAR,
    user_first_name VARCHAR,
    user_gender  VARCHAR,
    item_in_session	INTEGER,
    user_last_name VARCHAR,
    song_length	DECIMAL , 
    user_level VARCHAR,
    location VARCHAR,	
    method VARCHAR,
    page VARCHAR,	
    registration VARCHAR,	
    session_id	INT,
    song_title VARCHAR,
    status INTEGER,
    ts VARCHAR,
    user_agent VARCHAR,	
    user_id VARCHAR)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
    song_id VARCHAR,
    title VARCHAR,
    artist_id VARCHAR NOT NULL,
    year INT,
    duration FLOAT,
    artist_latitude DECIMAL,
    artist_location VARCHAR ,
    artist_longitude DECIMAL,
    artist_name VARCHAR,
    num_songs INT 
)""")
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(
    songplay_id INT CONSTRAINT songplay_pk PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INT NOT NULL,
    level VARCHAR NOT NULL,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT NOT NULL,
    location VARCHAR,
    user_agent VARCHAR
)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
    user_id VARCHAR CONSTRAINT users_pk PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR NOT NULL
)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
    song_id VARCHAR CONSTRAINT songs_pk PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR NOT NULL,
    year INT,
    duration FLOAT
)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(
    artist_id VARCHAR CONSTRAINT artist_pk PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude DECIMAL,
    longitude DECIMAL
)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
    start_time TIMESTAMP CONSTRAINT time_pk PRIMARY KEY,
    hour INT,
    day INT ,
    week INT,
    month INT,
    year INT ,
    weekday VARCHAR
)""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {}
 credentials 'aws_iam_role={}'
 region 'us-west-2' 
 JSON {} """).format(config.get('S3', 'LOG_DATA'),
                     config.get('IAM_ROLE', 'ARN'),
                     config.get('S3', 'LOG_JSONPATH'))



staging_songs_copy = ("""copy staging_songs from {}
    credentials 'aws_iam_role={}'
    region 'us-east-2' 
    JSON 'auto'""").format(config.get('S3', 'SONG_DATA'),
                           str(config.get('IAM_ROLE', 'ARN')))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET
                        level = EXCLUDED.level
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s) 
                        ON CONFLICT (start_time) DO NOTHING                       
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]