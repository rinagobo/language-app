from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from random import *

SECRET_KEY = ''
DATABASE_URI = ''

### CREATE FLASK SERVER ###
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

### CREATE DB ###
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


### CREATE TABLE ###
class Vocabulary(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    word_phrase = db.Column(db.String(100), unique=True, nullable=False)
    meaning = db.Column(db.String(200), nullable=False)
    example = db.Column(db.String(500), nullable=False)
    topic = db.Column(db.String, nullable=False)

# db.create_all()

    ### CONVERT EACH DATABASE ROW OBJECT TO A DICTIONARY ###
    def to_dict(self):
        vocab_dict = {}
        # Loop through each column in the data record
        # where the key is the name of the column
        # and the value is the value of the column
        for column in self.__table__.columns:
            vocab_dict[column.name] = getattr(self, column.name)
        return vocab_dict



### CREATE ROUTE ###
# ROUTES FOR READ METHOD OF RESTful API
@app.route("/random")
def get_random_vocab():
    vocabs = db.session.query(Vocabulary).all()
    random_vocab = choice(vocabs)

    return jsonify(vocab=random_vocab.to_dict())

@app.route("/all")
def get_all_vocab():
    vocabs = db.session.query(Vocabulary).all()
    return jsonify(vocabs=[vocab.to_dict() for vocab in vocabs])

@app.route("/search")
def get_vocab_by_topic():
    query_topic = request.args.get("topic")
    # IF YOU WANT TO GET ONLY THE FIRST ITEM WHICH IS FILTERED
    # vocab = db.session.query(Vocabulary).filter_by(topic=query_topic).first()
    # if vocab:
    #     return jsonify(vocab=vocab.to_dict())
    vocabs_selected = db.session.query(Vocabulary).filter_by(topic=query_topic)
    if vocabs_selected:
        return jsonify(vocabs_selected=[vocab.to_dict() for vocab in vocabs_selected])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


# ROUTES FOR WEB PAGES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["POST", "GET"])
def add():
    # ADD AN NEW ITEM TO THE DATABASE
    if request.method == 'POST':
        new_item = Vocabulary(
            date=request.form["date"],
            word_phrase=request.form["word_phrase"],
            meaning=request.form["meaning"],
            example=request.form["example"],
            topic=request.form["topic"]
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for("archive"))
    return render_template("form.html")


@app.route("/quiz_page", methods=["POST", "GET"])
def quiz_page():
    all_items = Vocabulary.query.all()
    db.session.commit()
    # TO CHOOSE RANDOM ITEM FOR THE QUIZ
    item_selected = all_items[randint(0, len(all_items) - 1)]

    # VARIABLES THAT ARE TRACKED
    quiz_count = 1
    correct_count = 0
    wrong_items = []

    if request.method == 'POST':
        correct_count = request.args.get('correct_count', type=int)
        wrong_items = request.args.getlist('wrong_items')
        list(map(int, wrong_items))

        # WHEN AN USER CRICKS THE NEXT BUTTON IN "quiz.html"
        if request.args.get('btn') == 'next':
            # UPDATE "quiz_count"
            updated_count = int(request.args.get('quiz_count')) + 1
            # CHOOSE NEXT QUESTION RANDOMLY
            all_items = Vocabulary.query.all()
            db.session.commit()
            item_selected = all_items[randint(0, len(all_items) - 1)]
            return render_template("quiz.html", item_selected=item_selected, quiz_count=updated_count, correct_count=correct_count , wrong_items=wrong_items)
        # WHEN AN USER CRICKS THE YES OR NO BUTTON in "quiz.html"
        else:
            quiz_count = int(request.args.get('quiz_count'))
            item_id = request.args.get('id')
            item_selected = Vocabulary.query.get(item_id)
            # NO BUTTON
            if request.args.get('btn') == 'no':
                # ADD THE NEW WRONG ITEM IF IT WAS NOT ADDED BEFORE
                if item_id not in wrong_items:
                    wrong_items.append(item_id)

                    return render_template("quiz.html", item_selected=item_selected, quiz_count=quiz_count,correct_count=correct_count, wrong_items=wrong_items)
            # YES BUTTON
            else:
                # UPDATE CORRECT COUNT
                correct_count += 1
                # UPDATE "quiz_count"
                updated_count = int(request.args.get('quiz_count')) + 1
                # CHOOSE NEXT QUESTION RANDOMLY
                all_items = Vocabulary.query.all()
                db.session.commit()
                updated_item = all_items[randint(0, len(all_items) - 1)]

                return render_template("quiz.html", item_selected=updated_item, quiz_count=updated_count, correct_count=correct_count, wrong_items=wrong_items)

    return render_template("quiz.html", item_selected=item_selected, quiz_count=quiz_count, correct_count=correct_count, wrong_items=wrong_items)

@app.route("/archive")
def archive():
    all_items = Vocabulary.query.all()
    db.session.commit()

    # TO CATEGORIZE ARCHIVE DATA BY YEAR AND MONTH IN "archive.html"
    monthly_items = []
    for item in all_items:
        year_month = item.date[slice(0,7)]
        monthly_items.append(year_month)
    count_dict = {i: monthly_items.count(i) for i in monthly_items}
    monthly_counts = list(count_dict.items())
    # HOW TO RETRIEVE DATA FROM "monthly_counts"
    # monthly_count[0][0]...yealy_month, monthly_count[0][1]...count

    return render_template("archive.html", all_items=all_items, monthly_counts=monthly_counts, slice=slice)


@app.route("/show_item")
def show_item():
    item_id = request.args.get('id')
    item_selected = Vocabulary.query.get(item_id)

    # DISTINGUISH THE ACCESS ROUTE TO THIS ROUTE, BETWEEN "/archive" AND "/quiz_page"
    if request.args.get('route') == "/quiz_page":
        direct_route = False
    else:
        direct_route = True

    return render_template("show_item.html", item_selected=item_selected, direct_route=direct_route)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    item_id = request.args.get('id')
    item_selected = Vocabulary.query.get(item_id)

    # EDIT A RECORD BY ID
    if request.method == 'POST':
        item_id = request.args.get('id')
        item_to_update = Vocabulary.query.get(item_id)
        item_to_update.word_phrase = request.form["word_phrase"]
        item_to_update.meaning = request.form["meaning"]
        item_to_update.example = request.form["example"]
        item_to_update.topic = request.form["topic"]

        db.session.commit()
        return redirect(url_for('archive'))

    return render_template("form.html", item_selected=item_selected)


@app.route("/delete")
def delete():
    item_id = request.args.get('id')

    # DELETE A RECORD BY ID
    item_to_delete = Vocabulary.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('archive'))

if __name__ == '__main__':
    app.run(debug=True)

