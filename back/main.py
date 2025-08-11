from flask import Flask, request, jsonify, render_template, redirect, url_for
import model
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', articles=model.articles)

@app.route('/articles/<int:index>')
def article_view(index):
    try:
        article = model.articles[index]
        return render_template('article.html', article=article, index=index)
    except IndexError:
        return "Article not found", 404

@app.route('/add_article', methods=['POST'])
def add_article():
    url = request.form.get('url')
    if not url:
        return "URL is required", 400
    try:
        article = model.fetch_article(url)
        beautified_article = model.beatify_article(article)
        new_article = json.loads(beautified_article)
        model.articles.append(new_article)
        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(model.articles, f, ensure_ascii=False, indent=4)
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error adding article: {e}", 500

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    index = data.get('index')
    if question is None or index is None:
        return jsonify({'error': 'Question and index are required'}), 400
    try:
        answer = model.ask_ai(question, index)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
