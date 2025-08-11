import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import model
import json
import database

# 加载环境变量
load_dotenv()

# 初始化数据库
database.init_db()

app = Flask(__name__)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """获取所有文章列表"""
    articles = database.get_all_articles()
    return jsonify({
        'articles': articles,
        'total': len(articles)
    })

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """获取指定ID的文章详情"""
    try:
        article = database.get_article_by_id(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        return jsonify({'article': article})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles', methods=['POST'])
def add_article_route():
    """添加新文章"""
    data = request.get_json()
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # 1. 抓取和解析文章
        fetched_article = model.fetch_article(url)
        
        # 2. 美化文章内容
        beautified_content_str = model.beatify_article(fetched_article)
        if not beautified_content_str:
            return jsonify({'error': 'Failed to beautify article'}), 500
        
        beautified_data = json.loads(beautified_content_str)
        title = beautified_data.get("title")
        content = beautified_data.get("content")

        if not title or not content:
            return jsonify({'error': 'Beautified article missing title or content'}), 500

        # 3. 存入数据库
        new_article = database.add_article(url, title, content)
        if new_article is None:
            return jsonify({'error': 'Article with this URL already exists'}), 409

        return jsonify({
            'message': 'Article added successfully',
            'article': new_article
        }), 201
    except Exception as e:
        return jsonify({'error': f'Error adding article: {str(e)}'}), 500

@app.route('/api/ask', methods=['POST'])
def ask():
    """向AI提问关于文章的问题"""
    data = request.get_json()
    question = data.get('question')
    article_id = data.get('article_id')
    
    if question is None or article_id is None:
        return jsonify({'error': 'Question and article_id are required'}), 400
    
    try:
        answer = model.ask_ai(question, article_id)
        return jsonify({'answer': answer})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'articles_count': database.get_articles_count()
    })

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=4000)
