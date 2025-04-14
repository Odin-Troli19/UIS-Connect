import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'uis_connect.db'),
)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Database connection helper functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

# Initialize database
def init_db():
    db = get_db()
    
    # Execute schema.sql
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    # Execute sample_data.sql if it exists
    try:
        with app.open_resource('sample_data.sql') as f:
            db.executescript(f.read().decode('utf8'))
    except:
        pass
    
    db.commit()

@app.route('/init-db')
def init_db_command():
    init_db()
    flash('Database initialized.')
    return redirect(url_for('index'))

# Authentication decorator
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# Auth routes
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        major = request.form.get('major', '')
        bio = request.form.get('bio', '')
        
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not first_name or not last_name:
            error = 'Full name is required.'
        elif db.execute(
            'SELECT user_id FROM Users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'
        elif db.execute(
            'SELECT user_id FROM Users WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = f'Email {email} is already registered.'
            
        if error is None:
            db.execute(
                'INSERT INTO Users (username, email, password_hash, first_name, last_name, bio, major, join_date, last_login) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (username, email, generate_password_hash(password), first_name, last_name, bio, major, datetime.now(), datetime.now())
            )
            db.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        
        flash(error)
    
    return render_template('auth/register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        error = None
        
        user = db.execute(
            'SELECT * FROM Users WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            
            # Update last login time
            db.execute(
                'UPDATE Users SET last_login = ? WHERE user_id = ?',
                (datetime.now(), user['user_id'])
            )
            db.commit()
            
            flash(f'Welcome back, {user["first_name"]}!')
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

# User routes
@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    
    user = db.execute(
        'SELECT * FROM Users WHERE username = ?', (username,)
    ).fetchone()
    
    if user is None:
        abort(404, f"User {username} doesn't exist.")
    
    # Get posts by this user
    posts = db.execute(
        '''SELECT p.*, COUNT(l.user_id) AS like_count
           FROM Posts p
           LEFT JOIN Likes l ON p.post_id = l.post_id
           WHERE p.user_id = ?
           GROUP BY p.post_id
           ORDER BY p.post_date DESC''',
        (user['user_id'],)
    ).fetchall()
    
    # Get courses this user is taking
    courses = db.execute(
        '''SELECT c.*
           FROM Courses c
           JOIN User_Courses uc ON c.course_id = uc.course_id
           WHERE uc.user_id = ?
           ORDER BY c.course_code''',
        (user['user_id'],)
    ).fetchall()
    
    # Check if logged-in user is friends with this user
    friendship_status = None
    if 'user_id' in session and session['user_id'] != user['user_id']:
        # Ensure user_id1 is the smaller id to match our schema constraint
        if session['user_id'] < user['user_id']:
            user_id1, user_id2 = session['user_id'], user['user_id']
        else:
            user_id1, user_id2 = user['user_id'], session['user_id']
            
        friendship = db.execute(
            'SELECT status FROM Friendships WHERE user_id1 = ? AND user_id2 = ?',
            (user_id1, user_id2)
        ).fetchone()
        
        if friendship:
            friendship_status = friendship['status']
    
    return render_template('user/profile.html', user=user, posts=posts, courses=courses, friendship_status=friendship_status)

@app.route('/profile/edit', methods=('GET', 'POST'))
@login_required
def edit_profile():
    db = get_db()
    
    user = db.execute(
        'SELECT * FROM Users WHERE user_id = ?', (session['user_id'],)
    ).fetchone()
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        bio = request.form.get('bio', '')
        major = request.form.get('major', '')
        
        error = None
        
        if not first_name or not last_name:
            error = 'Full name is required.'
        elif not email:
            error = 'Email is required.'
        elif email != user['email'] and db.execute(
            'SELECT user_id FROM Users WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = f'Email {email} is already in use.'
            
        if error is None:
            db.execute(
                '''UPDATE Users 
                   SET first_name = ?, last_name = ?, email = ?, bio = ?, major = ?
                   WHERE user_id = ?''',
                (first_name, last_name, email, bio, major, session['user_id'])
            )
            db.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('profile', username=user['username']))
        
        flash(error)
    
    return render_template('user/edit_profile.html', user=user)

# Friend routes
@app.route('/friends')
@login_required
def friends():
    db = get_db()
    
    # Get accepted friends
    accepted_friends = db.execute(
        '''SELECT u.*
           FROM Users u
           JOIN Friendships f ON (u.user_id = f.user_id1 OR u.user_id = f.user_id2)
           WHERE ((f.user_id1 = ? OR f.user_id2 = ?) 
                 AND u.user_id != ? 
                 AND f.status = 'accepted')''',
        (session['user_id'], session['user_id'], session['user_id'])
    ).fetchall()
    
    # Get pending friend requests (sent to the user)
    pending_requests = db.execute(
        '''SELECT u.*
           FROM Users u
           JOIN Friendships f ON (u.user_id = f.user_id1 OR u.user_id = f.user_id2)
           WHERE ((f.user_id1 = ? AND f.user_id2 = u.user_id) 
                 OR (f.user_id2 = ? AND f.user_id1 = u.user_id))
                 AND u.user_id != ? 
                 AND f.status = 'pending' ''',
        (session['user_id'], session['user_id'], session['user_id'])
    ).fetchall()
    
    # Get sent friend requests
    sent_requests = db.execute(
        '''SELECT u.*
           FROM Users u
           JOIN Friendships f ON (u.user_id = f.user_id1 OR u.user_id = f.user_id2)
           WHERE ((f.user_id1 = ? AND f.user_id2 = u.user_id) 
                 OR (f.user_id2 = ? AND f.user_id1 = u.user_id))
                 AND u.user_id != ? 
                 AND f.status = 'pending' ''',
        (session['user_id'], session['user_id'], session['user_id'])
    ).fetchall()
    
    return render_template('user/friends.html', 
                          accepted_friends=accepted_friends, 
                          pending_requests=pending_requests,
                          sent_requests=sent_requests)

@app.route('/friends/request/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id):
    db = get_db()
    
    # Check if user exists
    user = db.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    if user is None:
        abort(404, "User doesn't exist")
    
    # Check if friendship already exists
    # Ensure user_id1 is the smaller id to match our schema constraint
    if session['user_id'] < user_id:
        user_id1, user_id2 = session['user_id'], user_id
    else:
        user_id1, user_id2 = user_id, session['user_id']
        
    friendship = db.execute(
        'SELECT * FROM Friendships WHERE user_id1 = ? AND user_id2 = ?',
        (user_id1, user_id2)
    ).fetchone()
    
    if friendship:
        flash('A friendship or request already exists with this user.')
    else:
        db.execute(
            'INSERT INTO Friendships (user_id1, user_id2, status, action_date) VALUES (?, ?, ?, ?)',
            (user_id1, user_id2, 'pending', datetime.now())
        )
        db.commit()
        flash(f'Friend request sent to {user["username"]}.')
    
    return redirect(url_for('profile', username=user['username']))

@app.route('/friends/accept/<int:user_id>', methods=['POST'])
@login_required
def accept_friend_request(user_id):
    db = get_db()
    
    # Ensure user_id1 is the smaller id to match our schema constraint
    if session['user_id'] < user_id:
        user_id1, user_id2 = session['user_id'], user_id
    else:
        user_id1, user_id2 = user_id, session['user_id']
    
    db.execute(
        'UPDATE Friendships SET status = ?, action_date = ? WHERE user_id1 = ? AND user_id2 = ?',
        ('accepted', datetime.now(), user_id1, user_id2)
    )
    db.commit()
    
    user = db.execute('SELECT username FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    flash(f'You are now friends with {user["username"]}.')
    
    return redirect(url_for('friends'))

@app.route('/friends/reject/<int:user_id>', methods=['POST'])
@login_required
def reject_friend_request(user_id):
    db = get_db()
    
    # Ensure user_id1 is the smaller id to match our schema constraint
    if session['user_id'] < user_id:
        user_id1, user_id2 = session['user_id'], user_id
    else:
        user_id1, user_id2 = user_id, session['user_id']
    
    db.execute(
        'DELETE FROM Friendships WHERE user_id1 = ? AND user_id2 = ?',
        (user_id1, user_id2)
    )
    db.commit()
    
    user = db.execute('SELECT username FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    flash(f'Friend request from {user["username"]} rejected.')
    
    return redirect(url_for('friends'))

# Post routes
@app.route('/posts/create', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form['content']
        is_public = 1 if request.form.get('is_public') else 0
        course_ids = request.form.getlist('course_ids')
        
        error = None
        
        if not content:
            error = 'Content is required.'
            
        if error is None:
            db = get_db()
            cursor = db.execute(
                'INSERT INTO Posts (user_id, content, post_date, is_public) VALUES (?, ?, ?, ?)',
                (session['user_id'], content, datetime.now(), is_public)
            )
            post_id = cursor.lastrowid
            
            # Add course tags if selected
            for course_id in course_ids:
                db.execute(
                    'INSERT INTO Post_Courses (post_id, course_id) VALUES (?, ?)',
                    (post_id, course_id)
                )
                
            db.commit()
            flash('Post created successfully!')
            return redirect(url_for('index'))
        
        flash(error)
    
    # Get list of courses for the dropdown
    db = get_db()
    courses = db.execute('SELECT * FROM Courses ORDER BY course_code').fetchall()
    
    # Get courses the user is enrolled in
    user_courses = db.execute(
        '''SELECT c.*
           FROM Courses c
           JOIN User_Courses uc ON c.course_id = uc.course_id
           WHERE uc.user_id = ?
           ORDER BY c.course_code''',
        (session['user_id'],)
    ).fetchall()
    
    return render_template('posts/create.html', courses=courses, user_courses=user_courses)

@app.route('/posts/<int:post_id>')
def view_post(post_id):
    db = get_db()
    
    post = db.execute(
        '''SELECT p.*, u.username, u.first_name, u.last_name
           FROM Posts p
           JOIN Users u ON p.user_id = u.user_id
           WHERE p.post_id = ?''',
        (post_id,)
    ).fetchone()
    
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    
    # Get comments for this post
    comments = db.execute(
        '''SELECT c.*, u.username, u.first_name, u.last_name
           FROM Comments c
           JOIN Users u ON c.user_id = u.user_id
           WHERE c.post_id = ?
           ORDER BY c.comment_date''',
        (post_id,)
    ).fetchall()
    
    # Get like count and check if current user liked the post
    like_data = db.execute(
        '''SELECT COUNT(*) as like_count, 
                 SUM(CASE WHEN user_id = ? THEN 1 ELSE 0 END) as user_liked
           FROM Likes
           WHERE post_id = ?''',
        (session.get('user_id'), post_id)
    ).fetchone()
    
    # Get course tags for this post
    courses = db.execute(
        '''SELECT c.*
           FROM Courses c
           JOIN Post_Courses pc ON c.course_id = pc.course_id
           WHERE pc.post_id = ?
           ORDER BY c.course_code''',
        (post_id,)
    ).fetchall()
    
    return render_template('posts/view.html', 
                          post=post, 
                          comments=comments, 
                          like_count=like_data['like_count'],
                          user_liked=like_data['user_liked'],
                          courses=courses)

@app.route('/posts/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_post(post_id):
    db = get_db()
    
    post = db.execute(
        'SELECT * FROM Posts WHERE post_id = ?',
        (post_id,)
    ).fetchone()
    
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    
    # Check if the current user is the author
    if post['user_id'] != session['user_id']:
        abort(403, "You don't have permission to edit this post.")
    
    if request.method == 'POST':
        content = request.form['content']
        is_public = 1 if request.form.get('is_public') else 0
        course_ids = request.form.getlist('course_ids')
        
        error = None
        
        if not content:
            error = 'Content is required.'
            
        if error is None:
            db.execute(
                'UPDATE Posts SET content = ?, is_public = ? WHERE post_id = ?',
                (content, is_public, post_id)
            )
            
            # Remove existing course tags
            db.execute('DELETE FROM Post_Courses WHERE post_id = ?', (post_id,))
            
            # Add new course tags
            for course_id in course_ids:
                db.execute(
                    'INSERT INTO Post_Courses (post_id, course_id) VALUES (?, ?)',
                    (post_id, course_id)
                )
                
            db.commit()
            flash('Post updated successfully!')
            return redirect(url_for('view_post', post_id=post_id))
        
        flash(error)
    
    # Get all courses
    courses = db.execute('SELECT * FROM Courses ORDER BY course_code').fetchall()
    
    # Get courses tagged in this post
    post_courses = db.execute(
        '''SELECT course_id FROM Post_Courses WHERE post_id = ?''',
        (post_id,)
    ).fetchall()
    post_course_ids = [c['course_id'] for c in post_courses]
    
    return render_template('posts/edit.html', 
                          post=post, 
                          courses=courses, 
                          post_course_ids=post_course_ids)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    db = get_db()
    
    post = db.execute('SELECT * FROM Posts WHERE post_id = ?', (post_id,)).fetchone()
    
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    
    if post['user_id'] != session['user_id']:
        abort(403, "You don't have permission to delete this post.")
    
    db.execute('DELETE FROM Posts WHERE post_id = ?', (post_id,))
    db.commit()
    
    flash('Post deleted successfully!')
    return redirect(url_for('index'))

# Comment routes
@app.route('/posts/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form['content']
    
    if not content:
        flash('Comment content is required.')
        return redirect(url_for('view_post', post_id=post_id))
    
    db = get_db()
    
    # Verify post exists
    post = db.execute('SELECT * FROM Posts WHERE post_id = ?', (post_id,)).fetchone()
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    
    db.execute(
        'INSERT INTO Comments (post_id, user_id, content, comment_date) VALUES (?, ?, ?, ?)',
        (post_id, session['user_id'], content, datetime.now())
    )
    db.commit()
    
    flash('Comment added successfully!')
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    db = get_db()
    
    comment = db.execute(
        'SELECT * FROM Comments WHERE comment_id = ?', 
        (comment_id,)
    ).fetchone()
    
    if comment is None:
        abort(404, f"Comment id {comment_id} doesn't exist.")
    
    # Check if current user is the comment author
    if comment['user_id'] != session['user_id']:
        abort(403, "You don't have permission to delete this comment.")
    
    db.execute('DELETE FROM Comments WHERE comment_id = ?', (comment_id,))
    db.commit()
    
    flash('Comment deleted successfully!')
    return redirect(url_for('view_post', post_id=comment['post_id']))

# Like routes
@app.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    db = get_db()
    
    # Verify post exists
    post = db.execute('SELECT * FROM Posts WHERE post_id = ?', (post_id,)).fetchone()
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    
    # Check if user already liked the post
    like = db.execute(
        'SELECT * FROM Likes WHERE user_id = ? AND post_id = ?',
        (session['user_id'], post_id)
    ).fetchone()
    
    if like:
        # Unlike
        db.execute(
            'DELETE FROM Likes WHERE user_id = ? AND post_id = ?',
            (session['user_id'], post_id)
        )
        action = 'removed'
    else:
        # Like
        db.execute(
            'INSERT INTO Likes (user_id, post_id, like_date) VALUES (?, ?, ?)',
            (session['user_id'], post_id, datetime.now())
        )
        action = 'added'
    
    db.commit()
    flash(f'Like {action} successfully!')
    
    return redirect(url_for('view_post', post_id=post_id))

# Course routes
@app.route('/courses')
def list_courses():
    db = get_db()
    
    courses = db.execute(
        '''SELECT c.*, COUNT(uc.user_id) AS enrolled_count
           FROM Courses c
           LEFT JOIN User_Courses uc ON c.course_id = uc.course_id
           GROUP BY c.course_id
           ORDER BY c.department, c.course_code'''
    ).fetchall()
    
    # Get user's enrolled courses if logged in
    enrolled_course_ids = []
    if 'user_id' in session:
        user_courses = db.execute(
            'SELECT course_id FROM User_Courses WHERE user_id = ?',
            (session['user_id'],)
        ).fetchall()
        enrolled_course_ids = [c['course_id'] for c in user_courses]
    
    return render_template('courses/list.html', 
                          courses=courses, 
                          enrolled_course_ids=enrolled_course_ids)

@app.route('/courses/<int:course_id>')
def view_course(course_id):
    db = get_db()
    
    course = db.execute('SELECT * FROM Courses WHERE course_id = ?', (course_id,)).fetchone()
    
    if course is None:
        abort(404, f"Course id {course_id} doesn't exist.")
    
    # Get posts related to this course
    posts = db.execute(
        '''SELECT p.*, u.username, u.first_name, u.last_name, COUNT(l.user_id) AS like_count
           FROM Posts p
           JOIN Users u ON p.user_id = u.user_id
           JOIN Post_Courses pc ON p.post_id = pc.post_id
           LEFT JOIN Likes l ON p.post_id = l.post_id
           WHERE pc.course_id = ?
           GROUP BY p.post_id
           ORDER BY p.post_date DESC''',
        (course_id,)
    ).fetchall()
    
    # Get enrolled users
    enrolled_users = db.execute(
        '''SELECT u.*, uc.semester
           FROM Users u
           JOIN User_Courses uc ON u.user_id = uc.user_id
           WHERE uc.course_id = ?
           ORDER BY u.last_name, u.first_name''',
        (course_id,)
    ).fetchall()
    
    # Check if current user is enrolled
    is_enrolled = False
    if 'user_id' in session:
        enrollment = db.execute(
            'SELECT * FROM User_Courses WHERE user_id = ? AND course_id = ?',
            (session['user_id'], course_id)
        ).fetchone()
        is_enrolled = enrollment is not None
    
    return render_template('courses/view.html', 
                          course=course, 
                          posts=posts, 
                          enrolled_users=enrolled_users,
                          is_enrolled=is_enrolled)

@app.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    db = get_db()
    
    # Verify course exists
    course = db.execute('SELECT * FROM Courses WHERE course_id = ?', (course_id,)).fetchone()
    if course is None:
        abort(404, f"Course id {course_id} doesn't exist.")
    
    # Check if already enrolled
    enrollment = db.execute(
        'SELECT * FROM User_Courses WHERE user_id = ? AND course_id = ?',
        (session['user_id'], course_id)
    ).fetchone()
    
    if enrollment:
        flash(f'You are already enrolled in {course["course_code"]}.')
    else:
        semester = request.form.get('semester', 'Spring 2025')  # Default semester
        
        db.execute(
            'INSERT INTO User_Courses (user_id, course_id, semester) VALUES (?, ?, ?)',
            (session['user_id'], course_id, semester)
        )
        db.commit()
        
        flash(f'Successfully enrolled in {course["course_code"]}!')
    
    return redirect(url_for('view_course', course_id=course_id))

@app.route('/courses/<int:course_id>/unenroll', methods=['POST'])
@login_required
def unenroll_course(course_id):
    db = get_db()
    
    # Verify course exists
    course = db.execute('SELECT * FROM Courses WHERE course_id = ?', (course_id,)).fetchone()
    if course is None:
        abort(404, f"Course id {course_id} doesn't exist.")
    
    db.execute(
        'DELETE FROM User_Courses WHERE user_id = ? AND course_id = ?',
        (session['user_id'], course_id)
    )
    db.commit()
    
    flash(f'Successfully unenrolled from {course["course_code"]}.')
    return redirect(url_for('view_course', course_id=course_id))

# Search route
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('search.html', results=None, query=None)
    
    db = get_db()
    
    # Search users
    users = db.execute(
        '''SELECT * FROM Users 
           WHERE username LIKE ? 
              OR first_name LIKE ? 
              OR last_name LIKE ?
              OR major LIKE ?
           LIMIT 20''',
        (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%')
    ).fetchall()
    
    # Search posts
    posts = db.execute(
        '''SELECT p.*, u.username, u.first_name, u.last_name
           FROM Posts p
           JOIN Users u ON p.user_id = u.user_id
           WHERE p.content LIKE ?
           LIMIT 20''',
        (f'%{query}%',)
    ).fetchall()
    
    # Search courses
    courses = db.execute(
        '''SELECT * FROM Courses
           WHERE course_code LIKE ?
              OR course_name LIKE ?
              OR department LIKE ?
           LIMIT 20''',
        (f'%{query}%', f'%{query}%', f'%{query}%')
    ).fetchall()
    
    return render_template('search.html', 
                          users=users, 
                          posts=posts, 
                          courses=courses, 
                          query=query)

# Main Feed Route
@app.route('/')
def index():
    db = get_db()
    
    if 'user_id' in session:
        # Get posts from friends and the user