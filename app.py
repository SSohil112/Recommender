from flask import Flask, render_template, request
import pickle
import numpy

app = Flask(__name__)

# Load data and model
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Book not found in dataset
    if user_input not in pt.index:
        return render_template('recommend.html', error=f"❌ Book '{user_input}' not found in our system. Please try another.")

    index = pt.index.get_loc(user_input)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        book_title = pt.index[i[0]]
        temp_df = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title')

        if not temp_df.empty:
            title = temp_df['Book-Title'].values[0]
            author = temp_df['Book-Author'].values[0]
            image = temp_df['Image-URL-M'].values[0]
            data.append([title, author, image])

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
