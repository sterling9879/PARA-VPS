/**
 * LipSync Video Generator - Frontend Application
 * Interface web moderna para geração de vídeos com lip-sync
 */

// ============================================================================
// STATE & CONFIG
// ============================================================================

const state = {
    // Image management
    singleImages: [],
    multiImages: [],
    uploadedImagePaths: [],

    // Avatar state
    avatars: [],
    selectedAvatarId: null,
    selectedAvatarPath: null,
    pendingAvatarFile: null,

    // Batch image mode
    batchImageMode: 'fixed', // 'fixed' or 'individual'
    batchImages: {}, // {scriptId_batchNumber: avatarId}

    // Preview state
    previewData: null,
    voiceSelections: [],

    // Processing state
    currentVideoPath: null,
    processingJobs: [],
    completedVideos: [],

    // Projects
    projects: [],
    currentProject: null,
    tags: []
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSettings();
    initSliders();
    initImageUpload();
    initVoiceSelectors();
    initAvatarUpload();
    initSidebar();
    loadApiKeyStatus();
    loadAvatars();
    loadProjects();
    loadVideoHistory();
    loadProcessingJobs();

    // Event listeners
    document.getElementById('btnEstimate').addEventListener('click', calculateEstimate);
    document.getElementById('btnGenerate').addEventListener('click', generateSingleVideo);
    document.getElementById('btnGeneratePreview').addEventListener('click', generatePreview);
    document.getElementById('btnDownload').addEventListener('click', downloadVideo);

    // Refresh buttons
    document.getElementById('btnUploadAvatar').addEventListener('click', showAvatarUploadBox);
    document.getElementById('btnUploadMultipleAvatars').addEventListener('click', triggerBatchAvatarUpload);
    document.getElementById('avatarBatchUploadInput').addEventListener('change', handleBatchAvatarUpload);
});

// ============================================================================
// SIDEBAR
// ============================================================================

function initSidebar() {
    const btnToggle = document.getElementById('btnToggleSidebar');
    const sidebar = document.getElementById('sidebar');

    if (btnToggle && sidebar) {
        // Restore sidebar state from localStorage
        const isMinimized = localStorage.getItem('sidebarMinimized') === 'true';
        if (isMinimized) {
            sidebar.classList.add('minimized');
        }

        btnToggle.addEventListener('click', toggleSidebar);
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const btnToggle = document.getElementById('btnToggleSidebar');

    if (sidebar) {
        sidebar.classList.toggle('minimized');
        const isMinimized = sidebar.classList.contains('minimized');

        // Save state to localStorage
        localStorage.setItem('sidebarMinimized', isMinimized);

        // Update button title
        if (btnToggle) {
            btnToggle.title = isMinimized ? 'Expandir' : 'Minimizar';
        }
    }
}

// ============================================================================
// TABS NAVIGATION
// ============================================================================

function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;

            // Update buttons
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `tab-${tabId}`) {
                    content.classList.add('active');
                }
            });

            // Load data for specific tabs
            if (tabId === 'history') {
                loadVideoHistory();
            } else if (tabId === 'avatars') {
                loadAvatars();
            } else if (tabId === 'projects') {
                loadProjects();
            } else if (tabId === 'loading') {
                loadProcessingJobs();
            }
        });
    });
}

// ============================================================================
// SETTINGS MODAL
// ============================================================================

function initSettings() {
    const modal = document.getElementById('settingsModal');
    const btnOpen = document.getElementById('btnOpenSettings');
    const btnClose = document.getElementById('btnCloseSettings');
    const btnCancel = document.getElementById('btnCancelSettings');
    const btnSave = document.getElementById('btnSaveSettings');
    const overlay = document.getElementById('modalOverlay');

    btnOpen.addEventListener('click', () => modal.classList.add('active'));
    btnClose.addEventListener('click', () => modal.classList.remove('active'));
    btnCancel.addEventListener('click', () => modal.classList.remove('active'));
    overlay.addEventListener('click', () => modal.classList.remove('active'));

    btnSave.addEventListener('click', saveApiKeys);
}

async function loadApiKeyStatus() {
    try {
        const response = await fetch('/api/config/keys');
        const data = await response.json();

        if (data.success) {
            updateApiStatus('Elevenlabs', data.keys.elevenlabs);
            updateApiStatus('Minimax', data.keys.minimax);
            updateApiStatus('Gemini', data.keys.gemini);
            updateApiStatus('Wavespeed', data.keys.wavespeed);

            // Preencher os inputs com keys mascaradas como placeholder
            if (data.masked_keys) {
                setMaskedKeyPlaceholder('apiKeyElevenlabs', data.masked_keys.elevenlabs);
                setMaskedKeyPlaceholder('apiKeyMinimax', data.masked_keys.minimax);
                setMaskedKeyPlaceholder('apiKeyGemini', data.masked_keys.gemini);
                setMaskedKeyPlaceholder('apiKeyWavespeed', data.masked_keys.wavespeed);
            }
        }
    } catch (error) {
        console.error('Erro ao verificar API keys:', error);
    }
}

function setMaskedKeyPlaceholder(inputId, maskedKey) {
    const input = document.getElementById(inputId);
    if (input && maskedKey) {
        input.placeholder = maskedKey;
        input.dataset.hasKey = 'true';
    } else if (input) {
        input.placeholder = 'Cole sua API key aqui';
        input.dataset.hasKey = 'false';
    }
}

function updateApiStatus(name, configured) {
    const status = document.getElementById(`status${name}`);
    if (status) {
        status.textContent = configured ? 'Configurada' : 'Pendente';
        status.className = `api-status ${configured ? 'configured' : 'not-configured'}`;
    }
}

async function saveApiKeys() {
    const data = {
        elevenlabs_api_key: document.getElementById('apiKeyElevenlabs').value,
        minimax_api_key: document.getElementById('apiKeyMinimax').value,
        gemini_api_key: document.getElementById('apiKeyGemini').value,
        wavespeed_api_key: document.getElementById('apiKeyWavespeed').value
    };

    try {
        const response = await fetch('/api/config/keys', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showMessage('statusMessages', result.message, 'success');
            document.getElementById('settingsModal').classList.remove('active');
            loadApiKeyStatus();
            loadVoices('single');
            loadVoices('multi');
        } else {
            showMessage('statusMessages', result.error, 'error');
        }
    } catch (error) {
        showMessage('statusMessages', 'Erro ao salvar configurações', 'error');
    }
}

// ============================================================================
// SLIDERS
// ============================================================================

function initSliders() {
    const singleSlider = document.getElementById('singleWorkers');
    const singleValue = document.getElementById('singleWorkersValue');
    const multiSlider = document.getElementById('multiWorkers');
    const multiValue = document.getElementById('multiWorkersValue');
    const batchSizeSlider = document.getElementById('batchSize');
    const batchSizeValue = document.getElementById('batchSizeValue');

    singleSlider.addEventListener('input', () => {
        singleValue.textContent = singleSlider.value;
    });

    multiSlider.addEventListener('input', () => {
        multiValue.textContent = multiSlider.value;
    });

    if (batchSizeSlider && batchSizeValue) {
        batchSizeSlider.addEventListener('input', () => {
            batchSizeValue.textContent = batchSizeSlider.value;
        });
    }
}

// ============================================================================
// IMAGE SOURCE TOGGLE
// ============================================================================

function toggleImageSource(context, source) {
    // context: 'single' or 'multi'
    const avatarSelector = document.getElementById(`${context}AvatarSelector`);
    const uploadSection = document.getElementById(`${context}UploadSection`);
    const parentGroup = avatarSelector.closest('.form-group');
    const toggleBtns = parentGroup.querySelectorAll('.toggle-btn');

    toggleBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.source === source);
    });

    if (source === 'avatars') {
        avatarSelector.style.display = 'grid';
        uploadSection.style.display = 'none';
    } else {
        avatarSelector.style.display = 'none';
        uploadSection.style.display = 'block';
    }
}

// ============================================================================
// BATCH IMAGE MODE
// ============================================================================

function setBatchImageMode(mode) {
    state.batchImageMode = mode;

    // Update buttons
    document.querySelectorAll('.batch-mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    // Show/hide fixed image section
    const fixedSection = document.getElementById('fixedImageSection');
    if (mode === 'fixed') {
        fixedSection.style.display = 'block';
    } else {
        fixedSection.style.display = 'none';
    }

    // Re-render preview if exists
    if (state.previewData) {
        renderPreview(state.previewData);
    }
}

// ============================================================================
// IMAGE UPLOAD
// ============================================================================

function initImageUpload() {
    // Single video upload
    const singleUploadArea = document.getElementById('singleUploadArea');
    const singleInput = document.getElementById('singleImages');

    singleUploadArea.addEventListener('click', () => singleInput.click());
    singleUploadArea.addEventListener('dragover', handleDragOver);
    singleUploadArea.addEventListener('drop', (e) => handleDrop(e, 'single'));
    singleInput.addEventListener('change', (e) => handleFileSelect(e, 'single'));

    // Multi video upload
    const multiUploadArea = document.getElementById('multiUploadArea');
    const multiInput = document.getElementById('multiImages');

    multiUploadArea.addEventListener('click', () => multiInput.click());
    multiUploadArea.addEventListener('dragover', handleDragOver);
    multiUploadArea.addEventListener('drop', (e) => handleDrop(e, 'multi'));
    multiInput.addEventListener('change', (e) => handleFileSelect(e, 'multi'));
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDrop(e, context) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    addImages(files, context);
}

function handleFileSelect(e, context) {
    const files = Array.from(e.target.files);
    addImages(files, context);
}

function addImages(files, context) {
    const currentImages = context === 'single' ? state.singleImages : state.multiImages;
    const maxImages = 20;

    if (currentImages.length + files.length > maxImages) {
        showMessage('statusMessages', `Máximo de ${maxImages} imagens permitidas`, 'error');
        return;
    }

    files.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (context === 'single') {
                state.singleImages.push({ file, preview: e.target.result });
            } else {
                state.multiImages.push({ file, preview: e.target.result });
            }
            renderImagePreviews(context);
        };
        reader.readAsDataURL(file);
    });
}

function renderImagePreviews(context) {
    const images = context === 'single' ? state.singleImages : state.multiImages;
    const container = document.getElementById(`${context}ImagePreview`);

    container.innerHTML = images.map((img, idx) => `
        <div class="image-preview-item">
            <img src="${img.preview}" alt="Preview ${idx + 1}">
            <button class="image-preview-remove" onclick="removeImage(${idx}, '${context}')">&times;</button>
        </div>
    `).join('');
}

function removeImage(index, context) {
    if (context === 'single') {
        state.singleImages.splice(index, 1);
    } else {
        state.multiImages.splice(index, 1);
    }
    renderImagePreviews(context);
}

// ============================================================================
// AVATAR MANAGEMENT
// ============================================================================

async function loadAvatars() {
    try {
        const response = await fetch('/api/avatars');
        const data = await response.json();

        if (data.success) {
            state.avatars = data.avatars;
            renderAvatarsGallery();
            renderAvatarSelectors();
        }
    } catch (error) {
        console.error('Erro ao carregar avatares:', error);
    }
}

function renderAvatarsGallery() {
    const gallery = document.getElementById('avatarsGallery');

    if (state.avatars.length === 0) {
        gallery.innerHTML = `
            <div class="empty-state-large">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <p>Nenhum avatar salvo ainda</p>
                <p class="hint">Faça upload de imagens template para usar nos vídeos</p>
            </div>
        `;
        return;
    }

    gallery.innerHTML = state.avatars.map(avatar => `
        <div class="avatar-card" data-id="${avatar.id}">
            <img class="avatar-card-image" src="/api/avatars/${avatar.id}/image" alt="${avatar.name}">
            <div class="avatar-card-info">
                <div class="avatar-card-name">${avatar.name}</div>
                <div class="avatar-card-date">${formatDate(avatar.created_at)}</div>
                <div class="avatar-card-actions">
                    <button class="avatar-card-btn" onclick="selectAvatarForUse('${avatar.id}')">Usar</button>
                    <button class="avatar-card-btn danger" onclick="deleteAvatar('${avatar.id}')">Excluir</button>
                </div>
            </div>
        </div>
    `).join('');
}

function renderAvatarSelectors() {
    const selectors = ['singleAvatarSelector', 'multiAvatarSelector'];

    selectors.forEach(selectorId => {
        const selector = document.getElementById(selectorId);
        if (!selector) return;

        if (state.avatars.length === 0) {
            selector.innerHTML = '<p class="loading-text">Nenhum avatar disponível. Faça upload na aba "My Avatars"</p>';
            return;
        }

        selector.innerHTML = state.avatars.map(avatar => `
            <div class="avatar-selector-item ${state.selectedAvatarId === avatar.id ? 'selected' : ''}"
                 data-id="${avatar.id}"
                 data-path="${avatar.image_path}"
                 onclick="selectAvatar('${avatar.id}', '${avatar.image_path}')">
                <img class="avatar-selector-thumb" src="/api/avatars/${avatar.id}/image" alt="${avatar.name}">
                <span class="avatar-selector-name">${avatar.name}</span>
            </div>
        `).join('');
    });
}

function selectAvatar(avatarId, avatarPath) {
    state.selectedAvatarId = avatarId;
    state.selectedAvatarPath = avatarPath;

    // Update UI
    document.querySelectorAll('.avatar-selector-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.id === avatarId);
    });
}

function selectAvatarForUse(avatarId) {
    const avatar = state.avatars.find(a => a.id === avatarId);
    if (avatar) {
        selectAvatar(avatarId, avatar.image_path);
        // Switch to single video tab
        document.querySelector('[data-tab="single"]').click();
        // Switch to avatars source
        toggleImageSource('single', 'avatars');
    }
}

async function deleteAvatar(avatarId) {
    if (!confirm('Tem certeza que deseja excluir este avatar?')) return;

    try {
        const response = await fetch(`/api/avatars/${avatarId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            if (state.selectedAvatarId === avatarId) {
                state.selectedAvatarId = null;
                state.selectedAvatarPath = null;
            }
            loadAvatars();
        } else {
            alert('Erro ao excluir avatar: ' + data.error);
        }
    } catch (error) {
        console.error('Erro ao excluir avatar:', error);
    }
}

// ============================================================================
// AVATAR UPLOAD
// ============================================================================

function initAvatarUpload() {
    const input = document.getElementById('avatarUploadInput');
    const placeholder = document.getElementById('avatarPreviewPlaceholder');

    input.addEventListener('change', handleAvatarFileSelect);
    if (placeholder) {
        placeholder.addEventListener('click', () => input.click());
    }
}

function showAvatarUploadBox() {
    const uploadBox = document.getElementById('avatarUploadBox');
    uploadBox.style.display = 'flex';

    // Reset state
    state.pendingAvatarFile = null;
    document.getElementById('avatarName').value = '';
    document.getElementById('avatarPreviewImage').style.display = 'none';
    document.getElementById('avatarPreviewPlaceholder').style.display = 'flex';
}

function cancelAvatarUpload() {
    const uploadBox = document.getElementById('avatarUploadBox');
    uploadBox.style.display = 'none';
    state.pendingAvatarFile = null;
}

function handleAvatarFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    state.pendingAvatarFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImg = document.getElementById('avatarPreviewImage');
        const placeholder = document.getElementById('avatarPreviewPlaceholder');

        previewImg.src = e.target.result;
        previewImg.style.display = 'block';
        placeholder.style.display = 'none';
    };
    reader.readAsDataURL(file);

    // Auto-fill name if empty
    const nameInput = document.getElementById('avatarName');
    if (!nameInput.value) {
        nameInput.value = file.name.replace(/\.[^/.]+$/, '');
    }
}

async function saveAvatar() {
    if (!state.pendingAvatarFile) {
        alert('Selecione uma imagem primeiro');
        return;
    }

    const name = document.getElementById('avatarName').value || state.pendingAvatarFile.name;

    const formData = new FormData();
    formData.append('image', state.pendingAvatarFile);
    formData.append('name', name);

    try {
        const response = await fetch('/api/avatars', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            cancelAvatarUpload();
            loadAvatars();
        } else {
            alert('Erro ao salvar avatar: ' + data.error);
        }
    } catch (error) {
        console.error('Erro ao salvar avatar:', error);
        alert('Erro ao salvar avatar');
    }
}

function triggerBatchAvatarUpload() {
    document.getElementById('avatarBatchUploadInput').click();
}

async function handleBatchAvatarUpload(e) {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const totalFiles = files.length;
    let successCount = 0;
    let errorCount = 0;

    // Show progress message
    const gallery = document.getElementById('avatarsGallery');
    gallery.innerHTML = `
        <div class="empty-state-large">
            <div class="loading-spinner"></div>
            <p id="batchUploadProgress">Enviando 0/${totalFiles} avatares...</p>
        </div>
    `;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        // Extract name from filename (remove extension)
        const avatarName = file.name.replace(/\.[^/.]+$/, '');

        const formData = new FormData();
        formData.append('image', file);
        formData.append('name', avatarName);

        try {
            const response = await fetch('/api/avatars', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                successCount++;
            } else {
                errorCount++;
                console.error(`Erro ao salvar avatar ${avatarName}:`, data.error);
            }
        } catch (error) {
            errorCount++;
            console.error(`Erro ao salvar avatar ${avatarName}:`, error);
        }

        // Update progress
        document.getElementById('batchUploadProgress').textContent =
            `Enviando ${i + 1}/${totalFiles} avatares...`;
    }

    // Reset file input
    e.target.value = '';

    // Show result message
    if (errorCount === 0) {
        alert(`${successCount} avatar(es) enviado(s) com sucesso!`);
    } else {
        alert(`Upload concluído: ${successCount} sucesso(s), ${errorCount} erro(s)`);
    }

    // Reload avatars
    loadAvatars();
}

// ============================================================================
// VOICE SELECTORS
// ============================================================================

function initVoiceSelectors() {
    const singleProvider = document.getElementById('singleProvider');
    const multiProvider = document.getElementById('multiProvider');

    singleProvider.addEventListener('change', () => loadVoices('single'));
    multiProvider.addEventListener('change', () => loadVoices('multi'));

    // Load initial voices
    loadVoices('single');
    loadVoices('multi');
}

async function loadVoices(context) {
    const providerSelect = document.getElementById(`${context}Provider`);
    const voiceSelect = document.getElementById(`${context}Voice`);
    const provider = providerSelect.value;

    if (!voiceSelect) return;

    voiceSelect.innerHTML = '<option value="">Carregando...</option>';

    try {
        const response = await fetch(`/api/voices/${provider}`);
        const data = await response.json();

        if (data.success && data.voices.length > 0) {
            voiceSelect.innerHTML = data.voices.map(voice =>
                `<option value="${voice}">${voice}</option>`
            ).join('');
        } else {
            voiceSelect.innerHTML = '<option value="">Nenhuma voz disponível</option>';
        }
    } catch (error) {
        console.error(`Erro ao carregar vozes:`, error);
        voiceSelect.innerHTML = '<option value="">Erro ao carregar vozes</option>';
    }
}

// ============================================================================
// ESTIMATE
// ============================================================================

async function calculateEstimate() {
    const text = document.getElementById('singleText').value;

    if (!text.trim()) {
        showMessage('statusMessages', 'Digite um texto para estimar', 'error');
        return;
    }

    try {
        const response = await fetch('/api/estimate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (data.success) {
            const est = data.estimate;
            document.getElementById('estimateCard').style.display = 'block';
            document.getElementById('estimateContent').innerHTML = `
                <p><strong>Caracteres:</strong> ${est.total_chars ? est.total_chars.toLocaleString() : est.num_chars}</p>
                <p><strong>Batches:</strong> ${est.batches || est.num_batches}</p>
                <p><strong>Custo ElevenLabs:</strong> $${(est.cost_elevenlabs || 0).toFixed(4)}</p>
                <p><strong>Custo WaveSpeed:</strong> $${(est.cost_wavespeed || 0).toFixed(4)}</p>
                <p><strong>Custo Total Estimado:</strong> $${(est.total_cost || 0).toFixed(4)}</p>
            `;
        } else {
            showMessage('statusMessages', data.error, 'error');
        }
    } catch (error) {
        showMessage('statusMessages', 'Erro ao calcular estimativa', 'error');
    }
}

// ============================================================================
// SINGLE VIDEO GENERATION
// ============================================================================

async function generateSingleVideo() {
    const text = document.getElementById('singleText').value;
    const provider = document.getElementById('singleProvider').value;
    const voice = document.getElementById('singleVoice').value;
    const model = document.getElementById('singleModel').value;
    const workers = parseInt(document.getElementById('singleWorkers').value);

    // Validation
    if (!text.trim()) {
        showMessage('statusMessages', 'Digite um roteiro', 'error');
        return;
    }

    if (!voice) {
        showMessage('statusMessages', 'Selecione uma voz', 'error');
        return;
    }

    // Get image paths
    let imagePaths = [];

    if (state.selectedAvatarPath) {
        imagePaths = [state.selectedAvatarPath];
    } else if (state.singleImages.length > 0) {
        // Upload images first
        imagePaths = await uploadImages(state.singleImages);
    }

    if (imagePaths.length === 0) {
        showMessage('statusMessages', 'Selecione pelo menos uma imagem', 'error');
        return;
    }

    // Show progress
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const videoContainer = document.getElementById('videoContainer');

    progressContainer.style.display = 'block';
    videoContainer.style.display = 'none';
    progressFill.style.width = '0%';
    progressText.textContent = 'Iniciando geração...';

    // Add to loading tab
    const tempJobId = Date.now().toString();
    addToLoadingTab({
        id: tempJobId,
        title: 'Video em processamento',
        text: text.substring(0, 100) + '...',
        status: 'processing'
    });

    // Switch to loading tab to show animation
    document.querySelector('[data-tab="loading"]').click();

    try {
        progressFill.style.width = '20%';
        progressText.textContent = 'Enviando para processamento...';

        const response = await fetch('/api/generate/single', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                provider,
                voice_name: voice,
                model_id: model,
                image_paths: imagePaths,
                max_workers: workers
            })
        });

        const data = await response.json();

        if (data.success) {
            progressFill.style.width = '100%';
            progressText.textContent = 'Vídeo gerado com sucesso!';

            state.currentVideoPath = data.video_path;

            // Show video
            const videoPlayer = document.getElementById('videoPlayer');
            videoPlayer.src = `/api/download/${encodeURIComponent(data.video_path)}`;
            videoContainer.style.display = 'block';

            // Update loading tab
            updateLoadingTabItem(tempJobId, 'completed', data.video_path);

            showMessage('statusMessages', `Vídeo gerado em ${data.duration.toFixed(1)}s`, 'success');

            // Reload history
            loadVideoHistory();
            loadProcessingJobs();
        } else {
            progressContainer.style.display = 'none';
            updateLoadingTabItem(tempJobId, 'failed');
            showMessage('statusMessages', data.error, 'error');
        }
    } catch (error) {
        progressContainer.style.display = 'none';
        updateLoadingTabItem(tempJobId, 'failed');
        showMessage('statusMessages', 'Erro ao gerar vídeo', 'error');
        console.error(error);
    }
}

async function uploadImages(images) {
    const formData = new FormData();
    images.forEach(img => {
        formData.append('images', img.file);
    });

    try {
        const response = await fetch('/api/upload/images', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            return data.paths;
        }
    } catch (error) {
        console.error('Erro ao fazer upload:', error);
    }

    return [];
}

// ============================================================================
// PREVIEW GENERATION
// ============================================================================

async function generatePreview() {
    const text = document.getElementById('multiText').value;
    const batchSize = parseInt(document.getElementById('batchSize').value) || 3;

    if (!text.trim()) {
        showMessage('statusMessages', 'Digite os roteiros', 'error');
        return;
    }

    try {
        const response = await fetch('/api/preview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scripts_text: text, batch_size: batchSize })
        });

        const data = await response.json();

        if (data.success) {
            state.previewData = data;
            // Load voices for preview
            const provider = document.getElementById('multiProvider').value;
            const voicesResponse = await fetch(`/api/voices/${provider}`);
            const voicesData = await voicesResponse.json();
            state.voiceSelections = data.scripts.map(() => voicesData.success && voicesData.voices.length > 0 ? voicesData.voices[0] : '');
            renderPreview(data);
        } else {
            showMessage('statusMessages', data.error, 'error');
        }
    } catch (error) {
        showMessage('statusMessages', 'Erro ao gerar preview', 'error');
    }
}

async function renderPreview(data) {
    const container = document.getElementById('previewContent');
    const provider = document.getElementById('multiProvider').value;

    // Load voices for provider
    let voices = [];
    try {
        const voicesResponse = await fetch(`/api/voices/${provider}`);
        const voicesData = await voicesResponse.json();
        voices = voicesData.success ? voicesData.voices : [];
    } catch (e) {
        console.error('Error loading voices:', e);
    }

    let html = `
        <div class="preview-summary" style="display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap;">
            <span class="info-badge">${data.summary.total_scripts} roteiros</span>
            <span class="info-badge">${data.summary.total_batches} batches</span>
            <span class="info-badge">${data.summary.total_chars.toLocaleString()} caracteres</span>
        </div>
    `;

    data.scripts.forEach((script, scriptIdx) => {
        html += `
            <div class="script-card">
                <div class="script-header">
                    <span class="script-title">Roteiro ${script.id}</span>
                    <span class="script-stats">${script.total_batches} batches | ${script.total_chars} chars</span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <label style="color: white; font-size: 0.875rem; margin-bottom: 0.5rem; display: block;">Voz para este roteiro:</label>
                    <select class="voice-select" data-script="${scriptIdx}" onchange="updateVoiceSelection(${scriptIdx}, this.value)" style="width: 100%; padding: 0.5rem; border-radius: 8px; border: none;">
                        ${voices.map(v => `<option value="${v}">${v}</option>`).join('')}
                    </select>
                </div>
                <div class="batches-container">
        `;

        script.batches.forEach((batch, batchIdx) => {
            html += `
                <div class="batch-card">
                    <div class="batch-header">
                        <span class="batch-title">Batch ${batch.batch_number}</span>
                        <span style="font-size: 0.75rem; color: #666;">${batch.char_count} chars</span>
                    </div>
                    <div class="batch-text">${batch.text.replace(/\n/g, '<br>')}</div>
            `;

            // Add image selector if in individual mode
            if (state.batchImageMode === 'individual') {
                html += renderBatchImageSelector(script.id, batch.batch_number);
            }

            html += `</div>`;
        });

        html += `
                </div>
            </div>
        `;
    });

    html += `
        <button class="btn btn-primary btn-block" onclick="generateBatchVideos()" style="margin-top: 1.5rem;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            Gerar ${data.summary.total_scripts} Vídeos
        </button>
    `;

    container.innerHTML = html;
}

function renderBatchImageSelector(scriptId, batchNumber) {
    const key = `${scriptId}_${batchNumber}`;
    const selectedId = state.batchImages[key];

    let html = `
        <div class="batch-image-selector">
            <div class="batch-image-header">
                <span class="batch-image-title">Imagem para este batch:</span>
            </div>
            <div class="batch-image-mini-grid">
    `;

    state.avatars.forEach(avatar => {
        html += `
            <div class="batch-image-mini-item ${selectedId === avatar.id ? 'selected' : ''}"
                 onclick="selectBatchImage('${scriptId}', ${batchNumber}, '${avatar.id}')">
                <img src="/api/avatars/${avatar.id}/image" alt="${avatar.name}">
            </div>
        `;
    });

    html += `
            </div>
        </div>
    `;

    return html;
}

function selectBatchImage(scriptId, batchNumber, avatarId) {
    const key = `${scriptId}_${batchNumber}`;
    state.batchImages[key] = avatarId;

    // Update UI
    if (state.previewData) {
        renderPreview(state.previewData);
    }
}

function updateVoiceSelection(scriptIdx, voice) {
    state.voiceSelections[scriptIdx] = voice;
}

// ============================================================================
// BATCH VIDEO GENERATION
// ============================================================================

async function generateBatchVideos() {
    if (!state.previewData) {
        showMessage('statusMessages', 'Gere o preview primeiro', 'error');
        return;
    }

    const provider = document.getElementById('multiProvider').value;
    const model = document.getElementById('multiModel').value;
    const workers = parseInt(document.getElementById('multiWorkers').value);

    // Get image paths based on mode
    let imagePaths = [];
    let batchImagesMap = {}; // Mapa de scriptId_batchNumber -> image_path

    if (state.batchImageMode === 'fixed') {
        if (state.selectedAvatarPath) {
            imagePaths = [state.selectedAvatarPath];
        } else if (state.multiImages.length > 0) {
            imagePaths = await uploadImages(state.multiImages);
        }
    } else {
        // Individual mode - collect images and maintain batch association
        const uniqueAvatarPaths = new Set();

        // Build the batch images map with image paths
        for (const [key, avatarId] of Object.entries(state.batchImages)) {
            const avatar = state.avatars.find(a => a.id === avatarId);
            if (avatar) {
                batchImagesMap[key] = avatar.image_path;
                uniqueAvatarPaths.add(avatar.image_path);
            }
        }

        // Validate that all batches have images selected
        let allBatchesHaveImages = true;
        state.previewData.scripts.forEach(script => {
            script.batches.forEach(batch => {
                const key = `${script.id}_${batch.batch_number}`;
                if (!batchImagesMap[key]) {
                    allBatchesHaveImages = false;
                }
            });
        });

        if (!allBatchesHaveImages) {
            showMessage('statusMessages', 'Selecione uma imagem para cada batch no modo individual', 'error');
            return;
        }

        imagePaths = Array.from(uniqueAvatarPaths);
    }

    if (imagePaths.length === 0) {
        showMessage('statusMessages', 'Selecione pelo menos uma imagem', 'error');
        return;
    }

    // Validate voice selections
    if (state.voiceSelections.some(v => !v)) {
        showMessage('statusMessages', 'Selecione uma voz para cada roteiro', 'error');
        return;
    }

    // Switch to loading tab
    document.querySelector('[data-tab="loading"]').click();

    // Add items to loading tab
    state.previewData.scripts.forEach(script => {
        addToLoadingTab({
            id: `batch_${script.id}`,
            title: `Roteiro ${script.id}`,
            text: script.text.substring(0, 100) + '...',
            status: 'processing'
        });
    });

    try {
        const response = await fetch('/api/generate/batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                scripts: state.previewData.scripts,
                provider,
                model_id: model,
                image_paths: imagePaths,
                max_workers: workers,
                voice_selections: state.voiceSelections,
                batch_image_mode: state.batchImageMode,
                batch_images: batchImagesMap
            })
        });

        const data = await response.json();

        if (data.success) {
            const resultsCard = document.getElementById('multiResultsCard');
            const resultsContainer = document.getElementById('multiResults');

            let html = '<div class="results-grid">';

            data.results.forEach(result => {
                if (result.success) {
                    html += `
                        <div class="status-message status-success">
                            <strong>Roteiro ${result.script_id}:</strong>
                            Gerado em ${result.duration.toFixed(1)}s
                            <button class="btn btn-secondary" onclick="downloadVideoByPath('${result.video_path}')" style="margin-left: 1rem;">
                                Baixar
                            </button>
                        </div>
                    `;
                    updateLoadingTabItem(`batch_${result.script_id}`, 'completed', result.video_path);
                } else {
                    html += `
                        <div class="status-message status-error">
                            <strong>Roteiro ${result.script_id}:</strong> ${result.error}
                        </div>
                    `;
                    updateLoadingTabItem(`batch_${result.script_id}`, 'failed');
                }
            });

            html += '</div>';

            resultsCard.style.display = 'block';
            resultsContainer.innerHTML = html;

            showMessage('statusMessages', `${data.videos_count} de ${data.total_scripts} vídeos gerados`, 'success');

            // Reload history
            loadVideoHistory();
            loadProcessingJobs();
        } else {
            showMessage('statusMessages', data.error, 'error');
        }
    } catch (error) {
        showMessage('statusMessages', 'Erro ao gerar vídeos', 'error');
        console.error(error);
    }
}

// ============================================================================
// LOADING TAB
// ============================================================================

function addToLoadingTab(item) {
    const container = document.getElementById('loadingVideosContainer');

    // Remove empty state if present
    const emptyState = container.querySelector('.empty-state-large');
    if (emptyState) {
        emptyState.remove();
    }

    const itemHtml = `
        <div class="loading-video-card" data-id="${item.id}">
            <div class="loading-video-preview">
                <div class="loading-animation">
                    <div class="loading-spinner"></div>
                </div>
            </div>
            <div class="loading-video-info">
                <div class="loading-video-title">${item.title}</div>
                <div class="loading-video-meta">${item.text}</div>
                <div class="loading-video-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 30%;"></div>
                    </div>
                    <div class="loading-video-status">
                        Processando
                        <div class="processing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('afterbegin', itemHtml);
}

function updateLoadingTabItem(itemId, status, videoPath = null) {
    const item = document.querySelector(`.loading-video-card[data-id="${itemId}"]`);
    if (!item) return;

    if (status === 'completed' && videoPath) {
        // Move to completed section
        item.remove();
        addToCompletedVideos({
            id: itemId,
            path: videoPath,
            name: videoPath.split('/').pop()
        });
    } else if (status === 'failed') {
        item.querySelector('.loading-video-status').innerHTML = `
            <span style="color: var(--error);">Falhou</span>
        `;
        item.querySelector('.progress-fill').style.background = 'var(--error)';
    }
}

function addToCompletedVideos(video) {
    const container = document.getElementById('completedVideosContainer');

    // Remove empty state if present
    const emptyState = container.querySelector('.empty-state-large');
    if (emptyState) {
        emptyState.remove();
    }

    // Escape path for safe use in HTML attributes
    const escapedPath = video.path.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    const encodedPath = encodeURIComponent(video.path);

    const itemHtml = `
        <div class="completed-video-card" data-video-path="${encodedPath}">
            <div class="completed-video-thumbnail" onclick="playVideo('${escapedPath}')" style="cursor: pointer;">
                <video src="/api/stream/${encodedPath}" preload="metadata"></video>
                <div class="completed-video-play-overlay">
                    <div class="completed-video-play-btn">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                    </div>
                </div>
            </div>
            <div class="completed-video-info">
                <div class="completed-video-title">${video.name}</div>
                <div class="completed-video-meta">Concluído agora</div>
            </div>
            <div class="completed-video-actions">
                <button class="btn btn-secondary" onclick="playVideo('${escapedPath}')">
                    Assistir
                </button>
                <button class="btn btn-primary" onclick="downloadVideoByPath('${escapedPath}')">
                    Baixar
                </button>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('afterbegin', itemHtml);
}

async function loadProcessingJobs() {
    try {
        const response = await fetch('/api/jobs?status=processing');
        const data = await response.json();

        if (data.success) {
            state.processingJobs = data.jobs;
            // Update UI if needed
        }
    } catch (error) {
        console.error('Erro ao carregar jobs:', error);
    }
}

// ============================================================================
// VIDEO HISTORY
// ============================================================================

async function loadVideoHistory() {
    const container = document.getElementById('videoHistoryGrid');
    if (!container) return;

    try {
        const response = await fetch('/api/videos/history');
        const data = await response.json();

        if (data.success && data.videos.length > 0) {
            container.innerHTML = data.videos.map(video => {
                const escapedPath = video.path.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
                const encodedPath = encodeURIComponent(video.path);
                return `
                <div class="video-history-item">
                    <video class="video-history-thumb" src="/api/stream/${encodedPath}" preload="metadata"></video>
                    <div class="video-history-info">
                        <div class="video-history-name">${video.name}</div>
                        <div class="video-history-meta">${formatFileSize(video.size)} | ${formatDate(video.created_at * 1000)}</div>
                    </div>
                    <div class="video-history-actions">
                        <button class="btn btn-secondary" onclick="playVideo('${escapedPath}')">Assistir</button>
                        <button class="btn btn-primary" onclick="downloadVideoByPath('${escapedPath}')">Baixar</button>
                    </div>
                </div>
            `}).join('');
        } else {
            container.innerHTML = `
                <div class="empty-state-large" style="grid-column: 1/-1;">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                        <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                        <line x1="7" y1="2" x2="7" y2="22"></line>
                        <line x1="17" y1="2" x2="17" y2="22"></line>
                        <line x1="2" y1="12" x2="22" y2="12"></line>
                    </svg>
                    <p>Nenhum vídeo no histórico</p>
                    <p class="hint">Os vídeos gerados aparecerão aqui</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
    }
}

function playVideo(videoPath) {
    // Open video in new tab using stream endpoint
    window.open(`/api/stream/${encodeURIComponent(videoPath)}`, '_blank');
}

// ============================================================================
// DOWNLOAD
// ============================================================================

function downloadVideo() {
    if (state.currentVideoPath) {
        downloadVideoByPath(state.currentVideoPath);
    }
}

function downloadVideoByPath(videoPath) {
    // Create a proper download link using download endpoint
    const link = document.createElement('a');
    const downloadUrl = `/api/download/${encodeURIComponent(videoPath)}`;

    // Use fetch to get the file as blob for proper download
    fetch(downloadUrl)
        .then(response => {
            if (!response.ok) throw new Error('Download failed');
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            link.href = url;
            link.download = videoPath.split('/').pop() || 'video.mp4';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Download error:', error);
            // Fallback to direct download
            window.open(downloadUrl, '_blank');
        });
}

// ============================================================================
// PROJECTS
// ============================================================================

async function loadProjects() {
    try {
        const response = await fetch('/api/projects');
        const data = await response.json();

        if (data.success) {
            state.projects = data.projects;
            renderProjects();
            renderSidebarProjects();
        }
    } catch (error) {
        console.error('Erro ao carregar projetos:', error);
    }
}

function renderProjects() {
    const container = document.getElementById('projectsList');
    if (!container) return;

    if (state.projects.length === 0) {
        container.innerHTML = `
            <div class="empty-state-large">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
                <p>Nenhum projeto criado</p>
                <p class="hint">Crie projetos para organizar seus vídeos</p>
            </div>
        `;
        return;
    }

    container.innerHTML = state.projects.map(project => `
        <div class="project-card" data-id="${project.id}">
            <div class="project-header">
                <div>
                    <div class="project-title">${project.name}</div>
                    ${project.description ? `<div class="project-description">${project.description}</div>` : ''}
                </div>
                <div class="project-actions">
                    <button class="btn-icon" onclick="deleteProject('${project.id}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="project-tags">
                ${(project.tags || []).map(tag => `<span class="tag-badge">${tag}</span>`).join('')}
            </div>
            <div class="project-stats">
                <div class="project-stat">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 7l-7 5 7 5V7z"></path>
                        <rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect>
                    </svg>
                    ${(project.videos || []).length} vídeos
                </div>
                <div class="project-stat">
                    ${formatDate(project.created_at)}
                </div>
            </div>
        </div>
    `).join('');
}

function renderSidebarProjects() {
    const container = document.getElementById('sidebarProjects');
    if (!container) return;

    if (state.projects.length === 0) {
        container.innerHTML = '<p class="empty-state">Nenhum projeto ainda</p>';
        return;
    }

    container.innerHTML = state.projects.map(project => `
        <div class="project-item" data-id="${project.id}" onclick="selectProject('${project.id}')">
            <div class="project-name">${project.name}</div>
            <div class="project-meta">${(project.videos || []).length} vídeos</div>
        </div>
    `).join('');
}

async function deleteProject(projectId) {
    if (!confirm('Tem certeza que deseja excluir este projeto?')) return;

    try {
        const response = await fetch(`/api/projects/${projectId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            loadProjects();
        } else {
            alert('Erro ao excluir projeto: ' + data.error);
        }
    } catch (error) {
        console.error('Erro ao excluir projeto:', error);
    }
}

function selectProject(projectId) {
    state.currentProject = projectId;
    document.querySelectorAll('.project-item').forEach(item => {
        item.classList.toggle('active', item.dataset.id === projectId);
    });
}

// ============================================================================
// UTILITIES
// ============================================================================

function showMessage(containerId, message, type) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const div = document.createElement('div');
    div.className = `status-message status-${type}`;
    div.textContent = message;
    container.appendChild(div);

    setTimeout(() => div.remove(), 5000);
}

function formatDate(timestamp) {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Make functions globally accessible
window.toggleImageSource = toggleImageSource;
window.setBatchImageMode = setBatchImageMode;
window.selectAvatar = selectAvatar;
window.selectAvatarForUse = selectAvatarForUse;
window.deleteAvatar = deleteAvatar;
window.cancelAvatarUpload = cancelAvatarUpload;
window.saveAvatar = saveAvatar;
window.removeImage = removeImage;
window.updateVoiceSelection = updateVoiceSelection;
window.generateBatchVideos = generateBatchVideos;
window.selectBatchImage = selectBatchImage;
window.downloadVideoByPath = downloadVideoByPath;
window.toggleSidebar = toggleSidebar;
window.playVideo = playVideo;
window.loadVideoHistory = loadVideoHistory;
window.loadProcessingJobs = loadProcessingJobs;
window.selectProject = selectProject;
window.deleteProject = deleteProject;
