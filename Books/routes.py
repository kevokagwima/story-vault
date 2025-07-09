from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Book, Post, Users
from .form import BookForm

books = Blueprint("books", __name__)

@books.route("/")
@books.route("/home")
@books.route("/books")
@login_required
def home():
  books = Book.query.all()

  context = {
    "books": books,
    "posts": Post.query.all(),
    "readers": Users.query.filter(Users.unique_id != current_user.unique_id).all(),
  }

  return render_template("Books/index.html", **context)

@books.route("/books/<int:book_id>")
def book_detail(book_id):
  book = Book.query.get_or_404(book_id)
  return render_template("Books/detail.html", book=book)

@books.route("/books/add", methods=["GET", "POST"])
# @login_required
def add_book():
  form = BookForm()
  if form.validate_on_submit():
    title = form.title.data
    author = form.author.data
    cover_url = form.cover_url.data
    description = form.description.data
    isbn = form.isbn.data
    if not title or not author:
      flash("Title and author are required.", "danger")
      return redirect(url_for("books.add_book"))
    new_book = Book()
    new_book.title = title
    new_book.author = author
    new_book.cover_url = cover_url
    new_book.description = description
    new_book.isbn = isbn
    db.session.add(new_book)
    db.session.commit()
    flash("Book added successfully!", "success")
    return redirect(url_for("books.home"))
  return render_template("Books/add.html", form=form)
