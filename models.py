"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    def __repr__(self):
        return f"<user={self.username} first name={self.first_name} last name={self.last_name}>"

    username = db.Column(db.String(20), 
                        unique = True,
                        nullable = False,
                        primary_key = True)

    password = db.Column(db.Text,
                        nullable = False)

    email = db.Column(db.String(50),
                        nullable = False)

    first_name = db.Column(db.String(30),
                        nullable = False)

    last_name = db.Column(db.String(30),
                        nullable = False)


    @classmethod
    def add(self, uname, passwd, email, first, last):

        bcrypt = Bcrypt()
        hash = bcrypt.generate_password_hash(passwd)
        utf8_hash = hash.decode('utf8')

        user = User(username = uname, password = utf8_hash, email = email, first_name = first, last_name = last)
        db.session.add(user)
        db.session.commit()

        return {'successful' : True, 'user' : user}


    @classmethod
    def login(self, uname, passwd):
        """Authenticate a user"""
        bcrypt = Bcrypt()
        user = User.query.filter_by(username=uname).first()

        if user and bcrypt.check_password_hash(user.password, passwd):
            return user
        else:
            return False


    @classmethod
    def delete_user(self, uname):
        Feedback.query.filter_by(contributor = uname).delete()
        db.session.commit()
        User.query.filter_by(username = uname).delete()
        db.session.commit()



class Feedback(db.Model):
    __tablename__ = 'feedback'

    def __repr__(self) -> str:
        return f"post id: {self.id}, title: {self.title}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.String(100),
                        nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)

    contributor = db.Column(db.String(20), db.ForeignKey('users.username'))


    all = (id, title, content, contributor)

    @classmethod
    def add(self, ftitle, fcontent, fcontributor):
        """Adds new feedback to database and returns its id """
        feedback = Feedback(title = ftitle, content = fcontent, contributor = fcontributor)
        db.session.add(feedback)
        db.session.commit()
        return feedback.id

    @classmethod
    def edit(self, feedback_id, request):
        """Updates feedback in the database"""
        feedback = Feedback.query.get(feedback_id)
        feedback.title = request.form['title']
        feedback.content = request.form['content']
        db.session.commit()

    @classmethod
    def delete(self, feedback_id):
        """Delete feedback from the database"""
        Post.query.filter_by(id = postid).delete()
        db.session.commit()


def getJoin(fields, joinTable, fromTable=None, joinTable2 = "nothing", joinTable3 = "nothing", filter = "nothing"):
    """Sends back a table with the fields and records requested from two inner-joined tables
        Takes field, joinTable, filter(optional)
        fields - an iterable containing selected fields form two tables. Use *Post.all for all fields
        fromTable - The left table, required for more than one join
        joinTable - the table with the inner join
        filter - Where clauses, required to get specific record(s)
        *Note you can't use .get or .first with this return value
        *You must select and filter the records you want using this method's
        *filter argument (i.e. Post.id == 1).  
        *You can attach other modifiers like .order_by .limit and .all
    """
    if joinTable2 == "nothing":
        if filter == "nothing":
            print("\n\n\n\nNot using where clause")
            print(f"Filter: {filter}\n\n\n\n" )
            return db.session.query(*fields).outerjoin(joinTable)
        else:
            print("\n\n\n\nUsing filter\n\n\n\n")
            return db.session.query(*fields).outerjoin(joinTable).filter(filter)

    else:
        if joinTable3 == "nothing":
            if filter == "nothing":
                print("\n\n\n\nNot using where clause")
                print(f"Filter: {filter}\n\n\n\n" )
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2)
            else:
                print("\n\n\n\nUsing filter\n\n\n\n")
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2).filter(filter)
        else:
            if filter == "nothing":
                print("\n\n\n\nNot using where clause")
                print(f"Filter: {filter}\n\n\n\n" )
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2).join(joinTable3)
            else:
                print("\n\n\n\nUsing filter\n\n\n\n")
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2).join(joinTable3).filter(filter)



def make_db():
    db.drop_all()
    db.create_all()

def seed_db():
    user1 = User(username = 'user1', email = 'jolsen@thedailyplanet.com', first_name = "James", last_name = "Olsen", password = "notHashed!")
    user3 = User(username = 'user2', email = 'kzorel@catcomedia.com', first_name = "Kara", last_name = "Zor-el", password = "notHashed!")
    user2 = User(username = 'user3', email = 'potus@whitehouse.com', first_name = "Calvin", last_name = "Elis", password = "notHashed!")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    feedback1 = Feedback(title = "Feedback 1 title", content = "feedback 1 content blah blah blah", contributor = 1)
    feedback3 = Feedback(title = "Feedback 3 title?", content = "feedback 3 content blah blah blah", contributor = 3)
    feedback4 = Feedback(title = "Feedback 4 title", content = "feedback 4 content blah blah blah", contributor = 1)
    feedback2 = Feedback(title = "Feedback 2 title!", content = "feedback 2 content blah blah blah", contributor = 2)
    feedback5 = Feedback(title = "Feedback 5 title!", content = "feedback 5 content blah blah blah", contributor = 2)
    feedback6 = Feedback(title = "Feedback 6 title?", content = "feedback 6 content blah blah blah", contributor = 3)

    db.session.add(feedback2)
    db.session.add(feedback3)
    db.session.add(feedback1)
    db.session.add(feedback4)
    db.session.add(feedback5)
    db.session.add(feedback6)
    db.session.commit()
