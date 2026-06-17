import React from 'react';
import { BookOpen, Github, Server, Sparkles } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="footer bg-white border-t border-border pt-16 pb-10 px-4 relative z-10">
            <div className="container mx-auto max-w-7xl">
                <div className="grid md:grid-cols-3 gap-10 mb-12">
                    <div>
                        <h5 className="text-[0.95rem] font-bold mb-5 text-text-primary">书灵 BookSage</h5>
                        <div className="developer-card">
                            <p className="font-bold text-text-primary mb-0.5">智能图书推荐系统</p>
                            <p className="text-text-secondary text-[0.82rem] mb-4">基于 Book-Crossing 数据集，整合协同过滤、内容相似度与混合推荐策略。</p>
                            <div className="flex flex-wrap gap-2.5">
                                <a href="https://github.com/ZeroPointSix/BookSage-AI" target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 px-3 py-1.5 border border-border rounded-md text-text-secondary hover:bg-bg-hover hover:text-accent hover:border-accent transition-all text-xs font-medium decoration-0">
                                    <Github size={14} /> 项目仓库
                                </a>
                            </div>
                        </div>
                    </div>
                    <div>
                        <h5 className="text-[0.95rem] font-bold mb-5 text-text-primary">核心能力</h5>
                        <ul className="list-none space-y-3.5">
                            <li className="flex items-center gap-3 text-text-secondary text-[0.88rem]">
                                <Sparkles size={16} className="text-accent shrink-0" /> 搜索图书并生成推荐
                            </li>
                            <li className="flex items-center gap-3 text-text-secondary text-[0.88rem]">
                                <BookOpen size={16} className="text-accent shrink-0" /> 热门图书与推荐强度展示
                            </li>
                            <li className="flex items-center gap-3 text-text-secondary text-[0.88rem]">
                                <Server size={16} className="text-accent shrink-0" /> FastAPI + React 前后端分离
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h5 className="text-[0.95rem] font-bold mb-5 text-text-primary">验收重点</h5>
                        <p className="text-text-secondary text-[0.88rem] leading-relaxed">推荐接口保持兼容，前端展示完成中文化，并可通过 Docker Compose 一键启动前后端服务。</p>
                    </div>
                </div>
                <div className="text-center pt-6 border-t border-border text-text-muted text-[0.82rem]">
                    <p>&copy; 2026 书灵 BookSage. 智能图书推荐系统项目展示版。</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
