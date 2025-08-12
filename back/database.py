import mysql.connector
import os

def get_db_connection():
    """获取数据库连接"""
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        port=os.getenv('MYSQL_PORT', 3306)
    )
    return conn

def init_db():
    """初始化数据库，创建表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(2083) NOT NULL UNIQUE,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def add_article(url: str, title: str, content: str):
    """向数据库中添加新文章"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO articles (url, title, content) VALUES (%s, %s, %s)",
            (url, title, content)
        )
        conn.commit()
        new_id = cursor.lastrowid
        if new_id is None:
            return None
        return get_article_by_id(new_id)
    except mysql.connector.Error as err:
        # 处理URL已存在等错误
        print(f"Database Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_articles():
    """获取所有文章"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM articles ORDER BY created_at DESC')
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return articles

def get_article_by_id(article_id: int):
    """通过ID获取单篇文章"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM articles WHERE id = %s', (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    return article

def get_articles_count():
    """获取文章总数"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(id) FROM articles')
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return 0
