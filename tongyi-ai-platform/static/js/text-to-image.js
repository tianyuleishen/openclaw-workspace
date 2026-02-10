// 文生图 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generate-form');
    const resultBox = document.getElementById('result');
    
    if (!form) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const btn = form.querySelector('button[type="submit"]');
        const btnText = btn.querySelector('.btn-text');
        const btnLoading = btn.querySelector('.btn-loading');
        
        const prompt = document.getElementById('prompt').value;
        const size = document.getElementById('size').value;
        const style = document.getElementById('style').value;
        
        if (!prompt.trim()) {
            alert('请输入描述文字');
            return;
        }
        
        // 显示加载状态
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        
        try {
            const response = await fetch('/api/text-to-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: prompt,
                    size: size,
                    style: style
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // 显示结果
                resultBox.style.display = 'block';
                document.getElementById('generated-image').src = result.image_url;
                document.getElementById('download-link').href = result.image_url;
                
                // 滚动到结果区域
                resultBox.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('生成失败：' + result.message);
            }
        } catch (error) {
            alert('请求失败：' + error.message);
        } finally {
            // 恢复按钮状态
            btn.disabled = false;
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        }
    });
});
