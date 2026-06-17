export const METHOD_META = {
    hybrid: {
        label: '混合推荐',
        shortLabel: '混合',
        description: '综合协同过滤和内容相似度，优先给出更稳妥的推荐结果。',
    },
    collaborative: {
        label: '协同过滤',
        shortLabel: '协同',
        description: '根据相似读者的评分行为，寻找你可能也会喜欢的图书。',
    },
    content: {
        label: '内容相似',
        shortLabel: '内容',
        description: '分析图书标题、作者、出版信息和文本特征，推荐相近作品。',
    },
};

export const getMethodMeta = (method) => METHOD_META[method] || METHOD_META.hybrid;
