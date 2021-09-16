from flask import Blueprint, render_template, request, flash, jsonify
from .gb_functions import create_book
from .models import Book
import requests
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

def home():
    books = Book.query.all()
    return render_template("home.html", books = books, books_no = len(books))


@views.route('/googlebooks', methods = ['GET', 'POST'])

def googlebooks():
    si = 0
    books_list = []
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        title_search = request.form.get('title_search')
        author_search = request.form.get('author_search')
        publisher_search = request.form.get('publisher_search')
        subject_search = request.form.get('subject_search')
        isbn_search = request.form.get('isbn_search')
        lccn_search = request.form.get('lccn_search')
        oclc_search = request.form.get('oclc_search')
        search = ''
        if search_term:
            search += search_term
        if title_search:
            search += '+intitle:' + title_search
        if author_search:
            search += '+inauthor:' + author_search
        if publisher_search:
            search += '+inpublisher:' + publisher_search
        if subject_search:
            search += '+subject:' + subject_search
        if isbn_search:
            search += '+isbn:' + isbn_search
        if lccn_search:
            search += '+lccn:' + lccn_search
        if oclc_search:
            search += '+oclc:' + oclc_search

        r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=40&startIndex={si}')
        if r.status_code == 200:
            d = r.json()
            totalitems = d['totalItems']
            if totalitems:
                for item in d['items']:
                    books_list.append(create_book(item))
            si += 40
            while si < totalitems:
                r = requests.get(
                    f'https://www.googleapis.com/books/v1/volumes?q={search_term}&maxResults=40&startIndex={si}')
                d = r.json()
                if 'items' in d.keys():
                    for item in d['items']:
                        books_list.append(create_book(item))


                si += 40
        if not books_list:
            flash(f'No results for "{search}".', category='error')
        return render_template('googlebooks.html', books_list = books_list, results= len(books_list), search_term = search)
    else:
        return render_template('googlebooks.html', books_list=books_list)

@views.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method =='POST':
        title = request.form.get('title')
        authors = request.form.get('authors')
        published = request.form.get('published')
        isbn = request.form.get('isbn')
        pages = request.form.get('pages')
        thumbnail = request.form.get('thumbnail')
        language = request.form.get('language')
        print([i for i in request.form.values()])
        for item in request.form.items():
            if not item[1]:
                flash(f'Missing requied field "{item[0].capitalize()}"', category='error')
        if all(request.form.values()):
            new_book = Book(title=title,
                            authors=authors,
                            published=published,
                            isbn=isbn,
                            pages=pages,
                            thumbnail=thumbnail,
                            language=language)
            db.session.add(new_book)
            db.session.commit()
            flash(f'book added (ISBN:{new_book.isbn})')
            books = Book.query.all()
            return render_template("home.html", books=books, books_no=len(books))
    return render_template('add.html')

@views.route('/importbook', methods=['POST'])
def importbook():
    book = json.loads(request.data)
    new_book = Book(title = book['title'],
                    authors = book['authors'],
                    published = book['published'],
                    isbn = book['isbn'],
                    pages = book['pages'],
                    thumbnail = book['thumbnail'],
                    language = book['language'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({})

@views.route('/deletebook', methods=['POST'])
def deletebook():
    data = json.loads(request.data)
    isbn = data['isbn']
    book = Book.query.get(isbn)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash(f'book deleted (ISBN:{isbn})')
    return jsonify({})

@views.route('/edit', methods = ['GET', 'POST'])
def edit():
    if request.method == 'POST':  
        n_title = request.form.get('title')
        n_authors = request.form.get('authors')
        n_published = request.form.get('published')
        isbn = request.form.get('ISBN').strip()
        n_pages = request.form.get('pages')
        n_language = request.form.get('language')
        n_thumbnail = request.form.get('thumbnail')
        book = Book.query.get(isbn)
        if book:
            book = Book.query.get(isbn)
            book.title = n_title
            book.authors = n_authors
            book.published = n_published
            book.pages = n_pages
            book.language = n_language
            book.thumbnail = n_thumbnail
            db.session.commit()
            flash(f'book updated (ISBN:{isbn})')
        return home()
    else:
        book = None
        print(request.args)
        if request.args:
            book = Book.query.get(request.args["ISBN"])
        return render_template('edit.html', book = book)