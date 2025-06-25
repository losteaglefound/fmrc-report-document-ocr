class FileUploadSystem {
    constructor() {
        this.files = [];
        this.uploadEndpoint = '/api/upload'; // Update this to your actual endpoint
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.fileListContainer = document.getElementById('fileListContainer');
        this.fileList = document.getElementById('fileList');
        this.uploadProgress = document.getElementById('uploadProgress');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        this.resultModal = document.getElementById('resultModal');
        this.overlay = document.getElementById('overlay');
        this.closeModal = document.getElementById('closeModal');
        this.resultContent = document.getElementById('resultContent');
    }

    bindEvents() {
        // File input change
        this.uploadBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));

        // Modal events
        this.closeModal.addEventListener('click', () => this.closeResultModal());
        this.overlay.addEventListener('click', () => this.closeResultModal());

        // Keyboard events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeResultModal();
        });
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files);
        this.addFiles(files);
    }

    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.addFiles(files);
    }

    addFiles(newFiles) {
        newFiles.forEach(file => {
            if (!this.files.find(f => f.name === file.name && f.size === file.size)) {
                this.files.push({
                    file: file,
                    name: file.name,
                    size: file.size,
                    status: 'pending'
                });
            }
        });
        this.updateFileList();
        this.fileInput.value = ''; // Reset input
    }

    updateFileList() {
        if (this.files.length > 0) {
            this.fileListContainer.style.display = 'block';
            this.fileList.innerHTML = '';
            
            this.files.forEach((fileObj, index) => {
                const fileItem = this.createFileItem(fileObj, index);
                this.fileList.appendChild(fileItem);
            });
        } else {
            this.fileListContainer.style.display = 'none';
        }
    }

    createFileItem(fileObj, index) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const icon = this.getFileIcon(fileObj.name);
        const size = this.formatFileSize(fileObj.size);
        
        fileItem.innerHTML = `
            <div class="file-icon">
                <i class="${icon}"></i>
            </div>
            <div class="file-info">
                <div class="file-name">${fileObj.name}</div>
                <div class="file-size">${size}</div>
            </div>
            <div class="file-status ${fileObj.status}">
                ${this.getStatusText(fileObj.status)}
            </div>
        `;
        
        return fileItem;
    }

    getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const iconMap = {
            'pdf': 'fas fa-file-pdf',
            'doc': 'fas fa-file-word',
            'docx': 'fas fa-file-word',
            'xls': 'fas fa-file-excel',
            'xlsx': 'fas fa-file-excel',
            'ppt': 'fas fa-file-powerpoint',
            'pptx': 'fas fa-file-powerpoint',
            'txt': 'fas fa-file-alt',
            'jpg': 'fas fa-file-image',
            'jpeg': 'fas fa-file-image',
            'png': 'fas fa-file-image',
            'gif': 'fas fa-file-image',
            'mp4': 'fas fa-file-video',
            'avi': 'fas fa-file-video',
            'mp3': 'fas fa-file-audio',
            'zip': 'fas fa-file-archive',
            'rar': 'fas fa-file-archive'
        };
        return iconMap[ext] || 'fas fa-file';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    getStatusText(status) {
        const statusMap = {
            'pending': 'Pending',
            'uploading': 'Uploading...',
            'completed': 'Completed',
            'error': 'Error'
        };
        return statusMap[status] || 'Unknown';
    }

    async uploadFiles() {
        if (this.files.length === 0) {
            this.showNotification('Please select files to upload', 'error');
            return;
        }

        this.showUploadProgress();
        
        try {
            const formData = new FormData();
            this.files.forEach((fileObj, index) => {
                formData.append('files', fileObj.file);
                this.updateFileStatus(index, 'uploading');
            });

            const response = await this.sendUploadRequest(formData);
            this.handleUploadResponse(response);
        } catch (error) {
            console.error('Upload error:', error);
            this.showNotification('Upload failed. Please try again.', 'error');
            this.hideUploadProgress();
        }
    }

    async sendUploadRequest(formData) {
        // Simulate upload progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            this.updateProgress(progress);
        }, 200);

        try {
            const response = await fetch(this.uploadEndpoint, {
                method: 'POST',
                body: formData
            });

            clearInterval(progressInterval);
            this.updateProgress(100);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.text();
        } catch (error) {
            clearInterval(progressInterval);
            throw error;
        }
    }

    updateProgress(percentage) {
        this.progressFill.style.width = `${percentage}%`;
        this.progressText.textContent = `${Math.round(percentage)}% Complete`;
    }

    updateFileStatus(index, status) {
        this.files[index].status = status;
        this.updateFileList();
    }

    showUploadProgress() {
        this.uploadProgress.style.display = 'block';
        this.updateProgress(0);
    }

    hideUploadProgress() {
        this.uploadProgress.style.display = 'none';
    }

    handleUploadResponse(response) {
        this.hideUploadProgress();
        
        // Update all files to completed status
        this.files.forEach((_, index) => {
            this.updateFileStatus(index, 'completed');
        });

        // Extract URL from response using regex
        const urlMatch = response.match(/https?:\/\/[^\s]+/);
        const extractedUrl = urlMatch ? urlMatch[0] : null;

        this.showResultModal(response, extractedUrl);
    }

    showResultModal(response, extractedUrl) {
        let modalContent = `
            <div class="result-content">
                <p><strong>Response:</strong></p>
                <p>${response}</p>
        `;

        if (extractedUrl) {
            modalContent += `
                <div class="url-container">
                    <p><strong>Extracted URL:</strong></p>
                    <div class="url-text">${extractedUrl}</div>
                    <div class="url-actions">
                        <button class="url-btn copy-btn" onclick="fileUploadSystem.copyToClipboard('${extractedUrl}')">
                            <i class="fas fa-copy"></i> Copy URL
                        </button>
                        <button class="url-btn open-btn" onclick="fileUploadSystem.openUrl('${extractedUrl}')">
                            <i class="fas fa-external-link-alt"></i> Open in New Tab
                        </button>
                    </div>
                </div>
            `;
        }

        modalContent += '</div>';
        
        this.resultContent.innerHTML = modalContent;
        this.resultModal.classList.add('show');
        this.overlay.classList.add('show');
    }

    closeResultModal() {
        this.resultModal.classList.remove('show');
        this.overlay.classList.remove('show');
    }

    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showNotification('URL copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
            this.showNotification('Failed to copy URL', 'error');
        }
    }

    openUrl(url) {
        window.open(url, '_blank');
        this.showNotification('Opening URL in new tab...', 'success');
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
            word-wrap: break-word;
        `;

        // Set background color based on type
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            info: '#17a2b8',
            warning: '#ffc107'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        notification.textContent = message;
        document.body.appendChild(notification);

        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    clearFiles() {
        this.files = [];
        this.updateFileList();
        this.hideUploadProgress();
    }
}

// Initialize the file upload system
const fileUploadSystem = new FileUploadSystem();

// Add upload button functionality
document.addEventListener('DOMContentLoaded', () => {
    // Add an upload button to the UI
    const uploadContainer = document.querySelector('.upload-container');
    const uploadButton = document.createElement('button');
    uploadButton.className = 'upload-btn';
    uploadButton.style.cssText = `
        margin-top: 20px;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
    `;
    uploadButton.innerHTML = '<i class="fas fa-upload"></i> Upload Files';
    uploadButton.addEventListener('click', () => fileUploadSystem.uploadFiles());
    
    uploadContainer.appendChild(uploadButton);

    // Add clear button
    const clearButton = document.createElement('button');
    clearButton.className = 'upload-btn';
    clearButton.style.cssText = `
        margin-top: 10px;
        margin-left: 10px;
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
    `;
    clearButton.innerHTML = '<i class="fas fa-trash"></i> Clear Files';
    clearButton.addEventListener('click', () => fileUploadSystem.clearFiles());
    
    uploadContainer.appendChild(clearButton);
});

// Add slideOutRight animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style); 