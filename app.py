from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickled models/data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

# Home page route
@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_rating'].values),
        rating=list(popular_df['avg_rating'].values)
    )

# Recommendation UI page
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

# Recommendation logic
@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        return render_template('recommend.html', data=data)

    except IndexError:
        return render_template('recommend.html', data=[], error="Book not found! Try entering an exact title.")

if __name__ == '__main__':
    app.run(debug=True)
