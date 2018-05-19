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

    cursor.execute("INSERT INTO MOVIE VALUES (?, ?, ?, ?, ?)", [movie_id, movie_title, movie_description, movie_year, movie_language])
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
            cursor.execute("INSERT INTO MOVIE_SUBTITLE VALUES (?, ?, ?, ?)", [id, movie_id, url, movie_subtitle_language])


def insert_movie_media(movie_id, movie_media):
    """

    :type movie_id: int
    :type movie_media: list
    """
    for media in movie_media:
        resolution = media
        url = movie_media[media]
        cursor.execute("INSERT INTO MOVIE_MEDIA VALUES (?, ?, ?)", [movie_id, resolution, url])


def insert_genres_for_movie(movie_id, movie_genres):
    """

    :type movie_id: int
    :type movie_genres: list
    """
    for movie_genre in movie_genres:
        cursor.execute("INSERT INTO GENRE_FOR_MOVIE VALUES (?, ?)", [movie_id, movie_genre])


def search_movie_by_title(title):
    """

    :type title: str
    """
    return cursor.execute("SELECT TOP(10) Title FROM movie WHERE Title LIKE ?", ["%{0}%".format(title)])


def movie_info(title):
    """

    :type title: str
    """
    return cursor.execute("SELECT * FROM movie WHERE Title = ?", [title])
