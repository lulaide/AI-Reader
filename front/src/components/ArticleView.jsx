import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Loader from './Loader';
import './ArticleView.css';

const ArticleView = () => {
    const { id } = useParams();
    // 文章状态
    const [article, setArticle] = useState(null);
    // 问题输入框状态
    const [question, setQuestion] = useState('');
    // AI回答状态
    const [answer, setAnswer] = useState('');
    // 页面加载状态
    const [loading, setLoading] = useState(true);
    // AI问答加载状态
    const [asking, setAsking] = useState(false);
    // 聊天记录状态
    const [chatHistory, setChatHistory] = useState([]);

    // 根据URL中的id获取文章
    useEffect(() => {
        const fetchArticle = async () => {
            try {
                const response = await fetch(`/api/articles/${id}`);
                if (!response.ok) {
                    throw new Error('网络响应失败');
                }
                const data = await response.json();
                setArticle(data.article);
            } catch (error) {
                console.error('获取文章失败:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchArticle();
    }, [id]);

    // 处理提问
    const handleAsk = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        setAsking(true);
        setAnswer('');
        const currentQuestion = question;
        setQuestion('');

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: currentQuestion, article_id: parseInt(id) }),
            });
            if (!response.ok) {
                throw new Error('网络响应失败');
            }
            const data = await response.json();
            setAnswer(data.answer);
            // 更新聊天记录
            setChatHistory([...chatHistory, { question: currentQuestion, answer: data.answer }]);
        } catch (error) {
            console.error('提问失败:', error);
            const errorMessage = '抱歉，出错了。';
            setAnswer(errorMessage);
            setChatHistory([...chatHistory, { question: currentQuestion, answer: errorMessage }]);
        } finally {
            setAsking(false);
        }
    };

    // 用于在文章内容中渲染HTML标签
    const createMarkup = (htmlContent) => {
        // 对内容中的<red>和<green>标签进行处理，以便正确显示高亮
        const processedContent = htmlContent
            .replace(/<red>/g, '<span class="highlight-red">')
            .replace(/<\/red>/g, '</span>')
            .replace(/<green>/g, '<span class="highlight-green">')
            .replace(/<\/green>/g, '</span>');
        return { __html: processedContent };
    };

    if (loading) {
        return <Loader />;
    }

    if (!article) {
        return <div>文章未找到。 <Link to="/">返回主页</Link></div>;
    }

    return (
        <div className="page-container">
            <div className="left-column">
                <h1>{article.title}</h1>
                <div id="article-content" dangerouslySetInnerHTML={createMarkup(article.content)} />
            </div>
            <div className="right-column">
                <div id="ask-container">
                    <h3>关于本文</h3>
                    <div id="chat-area">
                        {chatHistory.map((chat, i) => (
                            <div key={i}>
                                <div className="chat-bubble user">{chat.question}</div>
                                <div className="chat-bubble ai">{chat.answer}</div>
                            </div>
                        ))}
                    </div>
                    <form onSubmit={handleAsk} className="ask-input-group">
                        <input
                            id="question-input"
                            type="text"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            placeholder="输入你的问题..."
                            disabled={asking}
                        />
                        <button type="submit" disabled={asking}>
                            {asking ? <div className="button-loader"></div> : '提问'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ArticleView;
