import React, { useState } from 'react';
import { Search, Sparkles, Sidebar as Shuffle, Users, BookOpen } from 'lucide-react';
import BookCard from '../components/BookCard';
import { METHOD_META } from '../utils/recommendationLabels';

const HomeView = ({ popularBooks, onRecommend }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [showButtons, setShowButtons] = useState(false);

    const handleSearchChange = async (e) => {
        const val = e.target.value;
        setQuery(val);
        if (val.length >= 2) {
            try {
                const resp = await fetch(`/api/search_books?query=${encodeURIComponent(val)}`);
                const data = await resp.json();
                setResults(data);
            } catch (err) {
                console.error(err);
            }
        } else {
            setResults([]);
            setShowButtons(false);
        }
    };

    const handleSelect = (title) => {
        setQuery(title);
        setResults([]);
        setShowButtons(true);
    };

    const revealRecommendationMethods = () => {
        if (query.trim()) {
            setShowButtons(true);
        }
    };

    const requestRecommendation = (method) => {
        const title = query.trim();
        if (title) {
            onRecommend(title, method);
        }
    };

    return (
        <div className="home-view animate-in">
            {/* Hero Section */}
            <section className="hero-section pt-24 pb-16 px-4 text-center rounded-b-[40px] shadow-2xl relative z-20">
                <div className="container mx-auto max-w-4xl">
                    <div className="hero-badge cursor-default">
                        <Sparkles size={14} className="text-white" />
                        <span>AI 智能图书推荐</span>
                    </div>

                    <h1 className="hero-title">书灵 BookSage</h1>
                    <p className="hero-subtitle">
                        基于协同过滤、内容相似度与混合策略，为读者快速发现下一本值得阅读的书。
                    </p>

                    <div className="search-container max-w-xl mx-auto relative z-30">
                        <div className="search-input-wrapper">
                            <input
                                type="text"
                                className="flex-1 py-4 px-6 text-text-primary focus:outline-none text-[1rem]"
                                placeholder="搜索一本你喜欢的书..."
                                value={query}
                                onChange={handleSearchChange}
                                onKeyDown={(e) => e.key === 'Enter' && revealRecommendationMethods()}
                            />
                            <button
                                className="search-btn-accent"
                                onClick={revealRecommendationMethods}
                                aria-label="显示推荐方式"
                            >
                                <Search size={20} />
                            </button>
                        </div>

                        {results.length > 0 && (
                            <div className="absolute top-full left-0 w-full mt-2 bg-white border border-border rounded-lg shadow-xl z-50 overflow-hidden text-left">
                                {results.map((book, i) => (
                                    <button
                                        key={i}
                                        className="w-full flex items-center gap-3 p-3 hover:bg-bg-hover transition-all border-b border-border last:border-0"
                                        onClick={() => handleSelect(book.title)}
                                    >
                                        <img src={book.image_url} alt={book.title} className="w-9 h-13 object-cover rounded shadow-sm" />
                                        <div>
                                            <div className="font-semibold text-text-primary text-sm leading-tight">{book.title}</div>
                                            <div className="text-xs text-text-secondary mt-1">{book.author}</div>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        )}

                        {showButtons && (
                            <div className="recommend-buttons mt-6 flex flex-wrap justify-center gap-3 animate-slide-up">
                                <button
                                    onClick={() => requestRecommendation('hybrid')}
                                    className="bg-gradient-to-r from-[#f59e0b] to-[#d97706] text-white px-5 py-2.5 rounded-lg font-bold text-sm shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-2"
                                >
                                    <Shuffle size={16} /> {METHOD_META.hybrid.label}
                                </button>
                                <button
                                    onClick={() => requestRecommendation('collaborative')}
                                    className="bg-gradient-to-r from-[#6366f1] to-[#4f46e5] text-white px-5 py-2.5 rounded-lg font-bold text-sm shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-2"
                                >
                                    <Users size={16} /> {METHOD_META.collaborative.label}
                                </button>
                                <button
                                    onClick={() => requestRecommendation('content')}
                                    className="bg-gradient-to-r from-[#10b981] to-[#059669] text-white px-5 py-2.5 rounded-lg font-bold text-sm shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-2"
                                >
                                    <BookOpen size={16} /> {METHOD_META.content.label}
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Methods Section */}
            <section className="py-20 bg-white border-b border-border">
                <div className="container mx-auto max-w-6xl px-4 text-center">
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold text-text-primary mb-2">推荐方式</h2>
                        <p className="text-text-secondary text-sm">选择更适合当前图书的推荐策略</p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-6">
                        <div className="bg-bg-body p-8 rounded-xl border border-border hover:shadow-md transition-all text-center group">
                            <div className="w-11 h-11 bg-gradient-to-r from-[#6366f1] to-[#4f46e5] text-white rounded-lg flex items-center justify-center mx-auto mb-5">
                                <Users size={20} />
                            </div>
                            <h3 className="text-[1.05rem] font-bold mb-3">{METHOD_META.collaborative.label}</h3>
                            <p className="text-text-secondary text-sm leading-relaxed">{METHOD_META.collaborative.description}</p>
                        </div>
                        <div className="bg-bg-body p-8 rounded-xl border border-border hover:shadow-md transition-all text-center group">
                            <div className="w-11 h-11 bg-gradient-to-r from-[#10b981] to-[#059669] text-white rounded-lg flex items-center justify-center mx-auto mb-5">
                                <BookOpen size={20} />
                            </div>
                            <h3 className="text-[1.05rem] font-bold mb-3">{METHOD_META.content.label}</h3>
                            <p className="text-text-secondary text-sm leading-relaxed">{METHOD_META.content.description}</p>
                        </div>
                        <div className="bg-bg-body p-8 rounded-xl border border-border hover:shadow-md transition-all text-center group">
                            <div className="w-11 h-11 bg-gradient-to-r from-[#f59e0b] to-[#d97706] text-white rounded-lg flex items-center justify-center mx-auto mb-5">
                                <Shuffle size={20} />
                            </div>
                            <h3 className="text-[1.05rem] font-bold mb-3">{METHOD_META.hybrid.label}</h3>
                            <p className="text-text-secondary text-sm leading-relaxed">{METHOD_META.hybrid.description}</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Popular Books Section */}
            <section className="py-20">
                <div className="container mx-auto max-w-7xl px-4">
                    <div className="text-center mb-12">
                        <h2 className="text-2xl font-bold text-text-primary mb-2">热门图书</h2>
                        <p className="text-text-secondary text-sm">基于样本数据中评分和热度筛选的图书</p>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
                        {popularBooks.map((book, i) => (
                            <BookCard key={i} book={book} onRecommend={onRecommend} />
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default HomeView;
