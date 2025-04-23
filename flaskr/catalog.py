from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint("catalog", __name__)


@bp.route("/")
def index():
    db = get_db()
    movies = db.execute("SELECT * FROM movies ORDER BY year, id DESC").fetchall()
    return render_template("catalog/index.html", movies=movies)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        rating = request.form["rating"]
        url = request.form["url"]
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO movies (title, year, rating, url) VALUES (?, ?, ?, ?)",
                (title, year, rating, url),
            )
            db.commit()
            return redirect(url_for("catalog.index"))

    return render_template("catalog/create.html")


def get_movie(id):
    movie = get_db().execute("SELECT * FROM movies WHERE id = ?", (id,)).fetchone()

    if movie is None:
        abort(404, f"Movie id {id} doesn't exist.")

    return movie


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    movie = get_movie(id)

    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        rating = request.form["rating"]
        url = request.form["url"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE movies SET "
                " title = ?, "
                " year = ?, "
                " rating = ?, "
                " url = ? "
                " WHERE id = ?",
                (title, year, rating, url, id),
            )
            db.commit()
            return redirect(url_for("catalog.index"))

    return render_template("catalog/update.html", movie=movie)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_movie(id)
    db = get_db()
    db.execute("DELETE FROM movies WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("catalog.index"))
