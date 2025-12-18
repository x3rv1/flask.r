from app import app, db, User, Post, Tag

with app.app_context():
    # create all
    db.create_all()
    
    # Create User
    u1 = User(name="Bob")
    db.session.add(u1)
    db.session.commit()
    
    # Create Posts
    p1 = Post(title="Post 1", content="Content 1", user=u1)
    p2 = Post(title="Post 2", content="Content 2", user=u1)
    
    # Create Tags
    t1 = Tag(name="Tech")
    t2 = Tag(name="Life")
    
    # Associate
    p1.tags.append(t1)
    p1.tags.append(t2)
    p2.tags.append(t2)
    
    db.session.add_all([p1, p2, t1, t2])
    db.session.commit()
    print("Seeded Bob with posts and tags")
