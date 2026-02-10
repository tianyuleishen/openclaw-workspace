// 图生视频 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generate-form');
    const fileInput = document.getElementById('image');
    const uploadArea = document.getElementById('upload-area');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    
    if (!form) return;
    
    // 文件选择处理
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            showPreview(file);
        }
    });
    
    // 拖拽处理
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            showPreview(file);
        }
    });
    
    function showPreview(file) {
        if (!file.type.startsWith('image/')) {
            alert('请上传图片文件');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
    
    // 表单提交
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const btn = form.querySelector('button[type="submit"]');
        const btnText = btn.querySelector('.btn-text');
        const btnLoading = btn.querySelector('.btn-loading');
        
        const file = fileInput.files[0];
        const prompt = document.getElementById('prompt').value;
        const size = document.getElementById('size').value;
        
        if (!file) {
            alert('请上传图片');
            return;
        }
        
        // 显示加载状态
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        
        const formData = new FormData();
        formData.append('image', file);
        formData.append('prompt', prompt);
        formData.append('size', size);
        
        try {
            const response = await fetch('/api/image-to-video', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // 显示结果
                const resultBox = document.getElementById('result');
                resultBox.style.display = 'block';
                
                const videoElement = document.getElementById('generated-video');
                videoElement.src = result.video_url;
                document.getElementById('download-link').href = result.video_url;
                
                // 尝试播放
                videoElement.play().catch(() => {
                    console.log('自动播放被阻止，请手动点击播放');
                });
                
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
