import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import model
import json

# 加载环境变量
load_dotenv()

app = Flask(__name__)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """获取所有文章列表"""
    return jsonify({
        'articles': model.articles,
        'total': len(model.articles)
    })

@app.route('/api/articles/<int:index>', methods=['GET'])
def get_article(index):
    """获取指定索引的文章详情"""
    try:
        if index < 0 or index >= len(model.articles):
            return jsonify({'error': 'Article not found'}), 404
        article = model.articles[index]
        return jsonify({'article': article, 'index': index})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles', methods=['POST'])
def add_article():
    """添加新文章"""
    data = request.get_json()
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        article = model.fetch_article(url)
        beautified_article = model.beatify_article(article)
        if not beautified_article:
            return jsonify({'error': 'Failed to beautify article'}), 500
        new_article = json.loads(beautified_article)
        model.articles.append(new_article)
        
        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(model.articles, f, ensure_ascii=False, indent=4)
        
        return jsonify({
            'message': 'Article added successfully',
            'article': new_article,
            'index': len(model.articles) - 1
        }), 201
    except Exception as e:
        return jsonify({'error': f'Error adding article: {str(e)}'}), 500

@app.route('/api/ask', methods=['POST'])
def ask():
    """向AI提问关于文章的问题"""
    data = request.get_json()
    question = data.get('question')
    index = data.get('index')
    
    if question is None or index is None:
        return jsonify({'error': 'Question and index are required'}), 400
    
    if index < 0 or index >= len(model.articles):
        return jsonify({'error': 'Article not found'}), 404
    
    try:
        answer = model.ask_ai(question, index)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'articles_count': len(model.articles)
    })

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=4000)
