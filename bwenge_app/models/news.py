# # from flask_sqlalchemy import SQLAlchemy
# # from datetime import datetime
# # from bwenge_app.extensions import db


# # class News(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String(255), nullable=False)
# #     content = db.Column(db.Text, nullable=False)
# #     image_url = db.Column(db.String(255), nullable=True)  # Optional image
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# #     def to_dict(self):
# #         return {
# #             "id": self.id,
# #             "title": self.title,
# #             "content": self.content,
# #             "image_url": self.image_url,
# #             "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
# #         }


# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from bwenge_app.extensions import db

# class News(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     image_url = db.Column(db.String(255), nullable=True)  # Stores filename of uploaded image
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "content": self.content,
#             "image_url": self.image_url,  # Filename of uploaded image
#             "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
#             "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
#         }

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bwenge_app.extensions import db

class News(db.Model):
    __tablename__ = 'news'  # Match RhemaBlog's naming convention

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # Optional image, same as RhemaBlog
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Added to match RhemaBlog

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "image_url": self.image_url,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
        }

    def __repr__(self):  # Added to match RhemaBlog's repr
        return f'<News {self.title}>'