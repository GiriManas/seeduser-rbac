from database import engine, SessionLocal
from models import Base, User, hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

admin_user = User(
    username="admin",
    email="admin@example.com",
    hashed_password=hash_password("admin123"),
    role="admin"
)

if not db.query(User).filter(User.email == admin_user.email).first():
    db.add(admin_user)
    db.commit()
    print("Admin user seeded successfully!")

db.close()
