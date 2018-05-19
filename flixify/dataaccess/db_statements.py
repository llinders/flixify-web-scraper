from flixify.dataaccess.db_connection import cursor


def insert_movie(movie_id, movie_title, movie_description, movie_year, movie_language, movie_genres, movie_media, movie_subtitles):
    """

    :type movie_id: int
    :type movie_title: str
    :type movie_description: str
    :type movie_year: int
    :type movie_language: str
    :type movie_genres: list
    :type movie_media: list
    :type movie_subtitles: list
    """
    if movie_year is None:
        movie_year = 0
    insert_movie_statement = "INSERT INTO MOVIE VALUES ('{0}', '{1}', '{2}', {3}, '{4}')".format(movie_id, movie_title.replace("'", "''"), movie_description.replace("'", "''"), movie_year, movie_language)
    cursor.execute(insert_movie_statement)
    insert_genres_for_movie(movie_id, movie_genres)

    insert_movie_media(movie_id, movie_media)
    insert_movie_subtitles(movie_id, movie_subtitles)
    cursor.commit()


def insert_movie_subtitles(movie_id, movie_subtitles):
    """

    :type movie_id: int
    :type movie_subtitles: list
    """
    for movie_subtitle_language in movie_subtitles:
        for movie_subtitle_properties in movie_subtitles[movie_subtitle_language]:
            id = movie_subtitle_properties['id']
            filename = movie_subtitle_properties['filename']
            src = movie_subtitle_properties['src']
            url = movie_subtitle_properties['url']
            insert_movie_subtitle_statement = "INSERT INTO MOVIE_SUBTITLE VALUES ('{0}', '{1}', '{2}', '{3}')".format(
                id,
                movie_id,
                url,
                movie_subtitle_language)
            cursor.execute(insert_movie_subtitle_statement)


def insert_movie_media(movie_id, movie_media):
    """

    :type movie_id: int
    :type movie_media: list
    """
    for media in movie_media:
        resolution = media
        url = movie_media[media]
        insert_movie_media_statement = "INSERT INTO MOVIE_MEDIA VALUES ('{0}', {1}, '{2}')".format(movie_id, resolution,
                                                                                                   url)
        print(insert_movie_media_statement)
        cursor.execute(insert_movie_media_statement)


def insert_genres_for_movie(movie_id, movie_genres):
    """

    :type movie_id: int
    :type movie_genres: list
    """
    for movie_genre in movie_genres:
        insert_movie_genre_statement = "INSERT INTO GENRE_FOR_MOVIE VALUES ('{0}', '{1}')".format(movie_id, movie_genre)
        print(insert_movie_genre_statement)
        cursor.execute(insert_movie_genre_statement)


def search_movie_by_title(title):
    """

    :type title: str
    """
    stmt = "SELECT TOP(10) Title FROM movie WHERE Title LIKE '%{0}%'".format(title.replace("'", "''"))
    return cursor.execute(stmt)


def movie_info(title):
    """

    :type title: str
    """
    stmt = "SELECT * FROM movie WHERE Title = '{0}'".format(title.replace("'", "''"))
    return cursor.execute(stmt)
