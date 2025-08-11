import sqlite3

DB_FILE = 'articles.db'

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库，创建表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_article(url: str, title: str, content: str):
    """向数据库中添加新文章"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO articles (url, title, content) VALUES (?, ?, ?)",
            (url, title, content)
        )
        conn.commit()
        new_id = cursor.lastrowid
        if new_id is None:
            return None
        return get_article_by_id(new_id)
    except sqlite3.IntegrityError:
        # URL已存在
        return None
    finally:
        conn.close()

def get_all_articles():
    """获取所有文章"""
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(row) for row in articles]

def get_article_by_id(article_id: int):
    """通过ID获取单篇文章"""
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()
    return dict(article) if article else None

def get_articles_count():
    """获取文章总数"""
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(id) FROM articles').fetchone()[0]
    conn.close()
    return count
