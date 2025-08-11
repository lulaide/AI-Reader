import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Loader from './Loader';
import './Home.css';

const Home = () => {
    // URL输入框的状态
    const [url, setUrl] = useState('');
    // 文章列表的状态
    const [articles, setArticles] = useState([]);
    // 加载状态
    const [loading, setLoading] = useState(false);
    // 错误信息状态
    const [error, setError] = useState('');

    // 组件加载时获取文章列表
    useEffect(() => {
        const fetchArticles = async () => {
            setLoading(true);
            try {
                const response = await fetch('/api/articles');
                if (!response.ok) throw new Error('获取文章列表失败');
                const data = await response.json();
                // 将文章倒序，使最新添加的显示在最前面
                setArticles(data.articles.reverse());
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchArticles();
    }, []);

    // 处理添加文章的表单提交
    const handleAddArticle = async (e) => {
        e.preventDefault();
        if (!url.trim()) return;
        setLoading(true);
        setError('');
        try {
            const response = await fetch('/api/articles', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url }),
            });
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || '添加文章失败');
            }
            const newArticleData = await response.json();
            // 在文章列表前面追加新文章
            setArticles([newArticleData.article, ...articles]);
            setUrl('');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // 从剪贴板粘贴URL
    const handlePaste = async () => {
        try {
            const text = await navigator.clipboard.readText();
            setUrl(text);
        } catch (err) {
            console.error('无法读取剪贴板内容: ', err);
        }
    };

    return (
        <main>
            {loading && <Loader />}
            <header>
                <h1>AI 文章阅读器</h1>
            </header>
            <form id="add-form" onSubmit={handleAddArticle}>
                <div className="input-wrapper">
                    <input
                        id="url-input"
                        type="url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="输入文章链接"
                        required
                    />
                    <button type="button" id="paste-btn" onClick={handlePaste} title="粘贴链接">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zM8 7a.5.5 0 0 1 .5.5V11a.5.5 0 0 1-1 0V7.5A.5.5 0 0 1 8 7z"/>
                        </svg>
                    </button>
                </div>
                <button id="add-btn" type="submit">添加文章</button>
            </form>
            {error && <p className="error-message">{error}</p>}

            <h2>我的文章</h2>
            <div id="articles-grid">
                {articles.map((article) => (
                    <Link to={`/article/${article.id}`} key={article.id} className="article-card">
                        <h3>{article.title}</h3>
                    </Link>
                ))}
            </div>
        </main>
    );
};

export default Home;
