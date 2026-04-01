from types import NoneType

from django.core.management import BaseCommand
from bookshelf.models import Publisher, Copyrighter, Rightholder, Genre, Rating
from bookshelf.models import Book, Contributor, BookContributor

import os
import random
import json
from bs4 import BeautifulSoup
from pathlib import Path
from django.conf import settings

destination_directory = "{}/.ai_log/db/".format(settings.BASE_DIR)


def parse(library_id):
    current_directory_name = f"{destination_directory}{library_id}"
    file_path = f'{current_directory_name}/{library_id}.html'

    # parse 'html'

    try:
        with open(file_path, 'r', encoding='utf-8') as fp:
            html_content = fp.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        # extract info
        dom_script_json = soup.find('script', attrs={'id': '__NEXT_DATA__', 'type': 'application/json'})
        dom_script = json.loads(dom_script_json.text)
        dom_initial_state = dom_script["props"]["pageProps"]["initialState"]
        initial_state = json.loads(dom_initial_state)
        # key = f'getArtFiles({{"artId":{library_id}}})'
        # files = initial_state['rtkqApi']['queries'][key]['data']

        key = f'getArtData({{"artIdOrSlug":{library_id}}})'
        bookdata = initial_state['rtkqApi']['queries'][key]['data']
        return bookdata

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def getdata(library_id):
    Dirs = os.popen(f'find {destination_directory} -mindepth 1 -maxdepth 1 -type d').read().split()
    for Dir in Dirs:
        library_id = Dir.split('/')[-1]
        data = parse(library_id)



class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        запуск отдельной функции
        """
        self.clear_databases()
        self.handle_bulk_create(*args, **options)
        print("Success!!!")

    def clear_databases(self):
        Publisher.objects.all().delete()
        Genre.objects.all().delete()
        Copyrighter.objects.all().delete()
        Rightholder.objects.all().delete()
        Book.objects.all().delete()
        BookContributor.objects.all().delete()
        Contributor.objects.all().delete()
        Rating.objects.all().delete()

    def handle_bulk_create_publisher(self, *args, **options):
        """
        заполнение с одним обращением в базу данных с
        записью множества строк одновременно
        """
        object_list = [
            {'id': 85198, 'name': 'Фантом Пресс', 'url': 'publisher/fantom-press/'}
        ]
        objects_for_creation = []
        for object_item in object_list:
            objects_for_creation.append(Publisher(**object_item))
        Publisher.objects.bulk_create(objects_for_creation)

    def handle_bulk_create(self, *args, **options):
        """
        заполнение с одним обращением в базу данных с
        записью множества строк одновременно
        """
        Dirs = os.popen(f'find {destination_directory} -mindepth 1 -maxdepth 1 -type d').read().split()
        for Dir in Dirs:
            library_id = Dir.split('/')[-1]
            library_data = parse(library_id)
            print(library_id)

            if library_data is not NoneType and library_data is not None:
                print(library_data)
                rating_item = {k: library_data['rating'][k]
                               for k in
                               ['user_rating', 'rated_1_count', 'rated_2_count', 'rated_3_count', 'rated_4_count',
                                'rated_5_count', 'rated_avg', 'rated_total_count']}

                rating, created = Rating.objects.get_or_create(**rating_item)

                publisher = None
                copyrighter = None
                if library_data["publisher"] is not None:
                    if library_data["publisher"]["id"] is not None:
                        publisher, created = Publisher.objects.get_or_create( ** library_data["publisher"] )
                if library_data["copyrighter"]["id"] is not None:
                    copyrighter, created = Copyrighter.objects.get_or_create( ** library_data["copyrighter"] )



                book_item = {
                    'id': library_data['id'],
                    'uuid': library_data['uuid'],
                    'title': library_data['title'],
                    'subtitle': library_data['subtitle'],
                    'cover_url': library_data['cover_url'].replace("/pub/c/cover/","media/book_covers/"),
                    'url': library_data['url'],
                    'is_draft': library_data['is_draft'],
                    'art_type': library_data['art_type'],
                    'prices': library_data['prices']['full_price'],
                    'is_auto_speech_gift': library_data['is_auto_speech_gift'],
                    'min_age': library_data['min_age'],
                    'language_code': library_data['language_code'],
                    'last_updated_at': library_data['last_updated_at'],
                    'last_released_at': library_data['last_released_at'],
                    'availability': library_data.get('availability', False),
                    'available_from': library_data['available_from'],
                    'html_annotation': library_data['html_annotation'],
                    'html_annotation_litres': library_data['html_annotation_litres'],
                    'livelib_rated_count': library_data['livelib_rated_count'],
                    'livelib_rated_avg': library_data['livelib_rated_avg'],
                    'isbn': library_data.get('isbn',''),
                    'publication_date': library_data['publication_date'],
                    'contents_url': library_data['contents_url'],

                    'rating': rating,
                    'publisher': publisher,
                    'copyrighter':copyrighter,


                }

                book, created = Book.objects.get_or_create(**book_item)

                genres_id=[]
                for item in library_data['genres']:
                    genre_item = {k: item[k]
                                               for k in ['id', 'uuid', 'name', 'url'] }
                    genre, created = Genre.objects.get_or_create(**genre_item)
                    genres_id.append( genre.id )
                book.genres.set( genres_id )

                rightholder_id = []
                for item in library_data["rightholders"]:
                    if item["id"] is not None:
                        rightholder, created = Rightholder.objects.get_or_create( ** item )
                        rightholder_id.append( rightholder.id )
                book.rightholder.set(rightholder_id)

                for person in library_data['persons']:
                    contributor_data = {k: person[k] for k in ['id', 'uuid', 'full_name', 'full_rodit', 'url']}
                    contributor, created = Contributor.objects.get_or_create(**contributor_data)
                    BookContributor.objects.create( book=book, contributor=contributor, role=person['role'] )


