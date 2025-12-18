from app import app, db, Post

with app.app_context():
    # Assuming user with ID 1 exists (Alice)
    post = Post(title="Alice's First Post", content="Hello World", user_id=1)
    db.session.add(post)
    db.session.commit()
    print("Post added")
