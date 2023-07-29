from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
import sqlite3

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@admin_bp.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall
    conn.close()
    return render_template('admin_bp.index.html', posts=posts)

@admin_bp.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@admin_bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('O título é obrigatório!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            flash('Post criado com sucesso!')
            return redirect(url_for('admin_bp.index'))

    return render_template('create.html')

@admin_bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_bp.index'))

    return render_template('edit.html', post=post)

@admin_bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluído com sucesso!'.format(post['title']))
    return redirect(url_for('admin_bp.index'))

@admin_bp.route('/telegra')
def telegra():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY created DESC").fetchall()
    conn.close()
    return render_template('telegra.html', posts=posts)