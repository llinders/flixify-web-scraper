from flixify.dataaccess.db_connection import cursor


def insert_movie(movie_id, movie_title, movie_description, movie_year, movie_language, movie_genres, movie_media, movie_subtitles):
    if movie_year is None:
        movie_year = 0
    insert_movie_statement = "INSERT INTO MOVIE VALUES ('{0}', '{1}', '{2}', {3}, '{4}')".format(movie_id, movie_title.replace("'", "''"), movie_description.replace("'", "''"), movie_year, movie_language)
    cursor.execute(insert_movie_statement)
    for movie_genre in movie_genres:
        insert_movie_genre_statement = "INSERT INTO GENRE_FOR_MOVIE VALUES ('{0}', '{1}')".format(movie_id, movie_genre)
        print(insert_movie_genre_statement)
        cursor.execute(insert_movie_genre_statement)

    for media in movie_media:
        resolution = media
        url = movie_media[media]
        insert_movie_media_statement = "INSERT INTO MOVIE_MEDIA VALUES ('{0}', {1}, '{2}')".format(movie_id, resolution, url)
        print(insert_movie_media_statement)
        cursor.execute(insert_movie_media_statement)
    for movie_subtitle_language in movie_subtitles:
        for movie_subtitle_properties in movie_subtitles[movie_subtitle_language]:
            id = movie_subtitle_properties['id']
            filename = movie_subtitle_properties['filename']
            src = movie_subtitle_properties['src']
            url = movie_subtitle_properties['url']
            insert_movie_subtitle_statement = "INSERT INTO MOVIE_SUBTITLE VALUES ('{0}', '{1}', '{2}', '{3}')".format(id,
                                                                                                     movie_id,
                                                                                                     url,
                                                                                                     movie_subtitle_language)
            cursor.execute(insert_movie_subtitle_statement)
    cursor.commit()


# import json
# a = json.dumps({"Name": "Robert",
#    "Date" : "January 17th, 2017",
#    "Address" : "Jakarta"})
# for key in json.loads(a):
#     print(key)