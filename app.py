from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import markdown
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Context processor to add variables to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Data storage - in a real app, you'd use a database
WIKI_CONTENT_DIR = 'content'
USERS_FILE = 'users.json'

# Ensure content directory exists
os.makedirs(WIKI_CONTENT_DIR, exist_ok=True)

# User management functions
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Wiki content functions
def get_page_path(title):
    safe_title = "".join([c for c in title if c.isalnum() or c in ' -_']).strip()
    safe_title = safe_title.replace(' ', '_')
    return os.path.join(WIKI_CONTENT_DIR, f"{safe_title}.md")

def page_exists(title):
    return os.path.exists(get_page_path(title))

def get_page_content(title):
    if page_exists(title):
        with open(get_page_path(title), 'r') as f:
            return f.read()
    return ""

def save_page_content(title, content):
    with open(get_page_path(title), 'w') as f:
        f.write(content)

def get_all_pages():
    pages = []
    for filename in os.listdir(WIKI_CONTENT_DIR):
        if filename.endswith('.md'):
            page_title = filename[:-3].replace('_', ' ')
            pages.append(page_title)
    return sorted(pages)

# Routes
@app.route('/')
def index():
    pages = get_all_pages()
    return render_template('index.html', pages=pages)

import re

@app.route('/page/<title>')
def view_page(title):
    content = get_page_content(title)
    if not content:
        return redirect(url_for('edit_page', title=title))
    
    # Process wiki links [[Page Name]] before rendering markdown
    def wiki_link_replace(match):
        page_name = match.group(1)
        return f'[{page_name}]({url_for("view_page", title=page_name)})'
    
    content = re.sub(r'\[\[(.*?)\]\]', wiki_link_replace, content)
    
    html_content = markdown.markdown(content)
    return render_template('page.html', title=title, content=html_content)

@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_page(title):
    if request.method == 'POST':
        content = request.form['content']
        save_page_content(title, content)
        return redirect(url_for('view_page', title=title))
    
    content = get_page_content(title)
    return render_template('edit.html', title=title, content=content)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    
    if query:
        for page_title in get_all_pages():
            content = get_page_content(page_title)
            if query in page_title.lower() or query in content.lower():
                results.append(page_title)
    
    return render_template('search.html', query=query, results=results)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        if username in users:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        users[username] = {
            'password_hash': generate_password_hash(password),
            'created_at': datetime.now().isoformat()
        }
        save_users(users)
        
        flash('Registration successful, please log in')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        if username in users and check_password_hash(users[username]['password_hash'], password):
            session['username'] = username
            flash('Login successful')
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
