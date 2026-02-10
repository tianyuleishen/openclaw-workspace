// 历史记录 JavaScript

const typeMap = {
    'text-to-image': '📝 文生图',
    'text-to-video': '🎬 文生视频',
    'image-to-video': '🖼️ 图生视频'
};

document.addEventListener('DOMContentLoaded', function() {
    loadHistory();
});

async function loadHistory() {
    const historyList = document.getElementById('history-list');
    
    try {
        const response = await fetch('/api/history');
        const result = await response.json();
        
        if (result.status === 'success' && result.data.length > 0) {
            historyList.innerHTML = result.data.map(item => createHistoryItem(item)).join('');
        } else {
            historyList.innerHTML = `
                <div class="empty-state">
                    <div class="icon">📭</div>
                    <p>暂无历史记录</p>
                    <p style="font-size: 14px; margin-top: 10px;">开始您的第一次创作吧！</p>
                </div>
            `;
        }
    } catch (error) {
        historyList.innerHTML = `
            <div class="empty-state">
                <div class="icon">❌</div>
                <p>加载失败</p>
                <p style="font-size: 14px; margin-top: 10px;">${error.message}</p>
            </div>
        `;
    }
}

function createHistoryItem(item) {
    const isImage = item.type === 'text-to-image';
    const thumbnail = isImage ? item.result : '/static/images/video-placeholder.png';
    const typeLabel = typeMap[item.type] || '📋 创作';
    
    return `
        <div class="history-item" onclick="viewDetail('${item.id}')">
            <img src="${thumbnail}" alt="缩略图" class="history-thumb" 
                 onerror="this.src='/static/images/placeholder.png'">
            <div class="history-info">
                <span class="history-type">${typeLabel}</span>
                <p class="history-prompt">${item.prompt || '无描述'}</p>
                <p class="history-time">${formatTime(item.created_at)}</p>
            </div>
        </div>
    `;
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function viewDetail(id) {
    // 可以扩展为详情页
    console.log('查看详情:', id);
}
