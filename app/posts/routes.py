from app.posts.models import Post
from app.posts.forms import PostForm
from flask_login import current_user, login_required
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        Post.create_post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        flash('Message posted', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.get_post_by_id(post_id=post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.get_post_by_id(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        Post.update_post(post=post, form=form)        
        flash('Post updated successfully', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.get_post_by_id(post_id)
    if post.author != current_user:
        abort(403)
    Post.delete_post(post)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


