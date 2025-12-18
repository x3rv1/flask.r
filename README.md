# Flask App Assignment 🚀

Welcome! This is a single-file Flask application built to demonstrate how to handle **relationships** and **serialization** in a database.

## 🎯 What We Built

We created a simple API involving Users, Posts, and Tags. Think of it like a mini-social media backend!

### 1. The Models (Our "Objects")
We defined three main types of data:
- **User**: Someone who writes posts.
- **Post**: A piece of content written by a User.
- **Tag**: A label (like `#coding` or `#life`) that can be attached to Posts.

### 2. The Relationships
We connected these models together in two ways:

- **One-to-Many (User ↔ Posts)**:
    - One User can write *many* Posts.
    - But each Post belongs to only *one* User.
    - *Code:* `db.relationship('Post', back_populates='user')`

- **Many-to-Many (Posts ↔ Tags)**:
    - One Post can have *many* Tags.
    - One Tag can be on *many* Posts.
    - To make this work, we used a helper table called `post_tags` to bridge them together.

### 3. Serialization (Turning Objects into JSON)
This was the tricky part! We used `SerializerMixin` to easily convert our database objects into a format (JSON) that the browser can understand.

**The "Infinite Loop" Problem:**
Imagine asking for a User. Only to get their Posts. Each Post has a User. That User has Posts... and it goes on forever! 🌀

**The Solution:**
We utilized `serialize_rules` to stop this recursion:
- When looking at a **User**, we stop after loading their **Posts**. We say: *"Don't show the User inside those Posts."* (`-posts.user`)
- When looking at a **Post's Tags**, we say: *"Don't show the Posts inside those Tags."* (`-tags.posts`)

## 🛠️ How to Run It

1.  **Install the tools:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the app:**
    ```bash
    python app.py
    ```

3.  **Test it out:**
    Open another terminal and type:
    ```bash
    # Get all users and their posts/tags
    curl http://127.0.0.1:5000/users
    ```

## 📂 Files
- `app.py`: All of our code lives here!
- `requirements.txt`: List of python packages we need.
- `seed_*.py`: Helper scripts to add fake data for testing.
