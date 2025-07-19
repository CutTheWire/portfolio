document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('pre code.language-directory').forEach(block => {
        const pre = block.closest('pre');
        const owner = pre?.dataset.owner || "TreeNut-KR";
        const repo = pre?.dataset.repo || "ChatBot-AI";
        const folder = pre?.dataset.folder || "";
        const treeData = parseDirectoryTree(block.textContent);
        const container = document.createElement('div');
        container.className = 'vscode-directory-tree';
        container.innerHTML = renderDirectoryTree(treeData, 0, owner, repo, folder);

        // 래퍼 추가
        const wrapper = document.createElement('div');
        wrapper.className = 'directory-tree-wrapper';
        wrapper.appendChild(container);

        pre.replaceWith(wrapper);
        addTreeInteractivity(container);
    });
});

function parseDirectoryTree(text) {
    const lines = text.split('\n').filter(l => l.trim());
    const stack = [];
    const roots = [];

    lines.forEach(line => {
        const indent = (line.match(/^[\s┃]*/)?.[0] || '').replace(/[^┃]/g, '').length;
        let name = line.replace(/[┃┣┗ ]+/g, '').replace(/[📦📂📜]/g, '').trim();
        if (!name) return;

        // []() 패턴 감지
        const linkMatch = name.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
        const isLink = !!linkMatch;

        const isFolder = line.includes('📦') || line.includes('📂');
        const node = { name, children: [], isFolder, level: indent, isLink };

        while (stack.length && stack[stack.length - 1].level >= indent) stack.pop();

        if (stack.length === 0) {
            roots.push(node);
        } else {
            stack[stack.length - 1].children.push(node);
        }

        stack.push(node);
    });

    return roots;
}

function getIconClass(name, isFolder, isLink = false) {
    if (isLink) {
        return 'fa-solid fa-link';
    }
    if (isFolder) {
        const folderIcons = {
            'src': 'fa-solid fa-folder-tree',
            'docs': 'fa-solid fa-book',
            'test': 'fa-solid fa-vial',
            'logs': 'fa-solid fa-file-lines',
            'batch': 'fa-solid fa-terminal',
            'certificates': 'fa-solid fa-certificate',
            'ai_model': 'fa-solid fa-brain',
            'prompt': 'fa-solid fa-comment-dots',
            'domain': 'fa-solid fa-layer-group',
            'core': 'fa-solid fa-cogs',
            'server': 'fa-solid fa-server',
            'performance_results': 'fa-solid fa-chart-line'
        };
        return folderIcons[name.toLowerCase()] || 'fa-solid fa-folder';
    } else {
        const ext = name.split('.').pop().toLowerCase();
        if (name.startsWith('.')) return 'fa-solid fa-gear';
        if (ext === 'md') return 'fa-brands fa-markdown';
        if (ext === 'py') return 'fa-brands fa-python';
        if (ext === 'bat' || ext === 'sh') return 'fa-solid fa-terminal';
        if (ext === 'json' || ext === 'yaml' || ext === 'yml') return 'fa-solid fa-file-code';
        if (ext === 'txt' || ext === 'log') return 'fa-solid fa-file-lines';
        if (ext === 'dockerfile') return 'fa-brands fa-docker';
        if (ext === 'env') return 'fa-solid fa-gear';
        return 'fa-solid fa-file';
    }
}

function renderDirectoryTree(nodes, depth = 0, owner = "TreeNut-KR", repo = "ChatBot-AI", folder = "", parentPath = "") {
    // folder가 있으면 blob/main/{folder}/, 없으면 blob/main/
    const baseUrl = folder
        ? `https://github.com/${owner}/${repo}/blob/main/${folder}/`
        : `https://github.com/${owner}/${repo}/blob/main/`;
    let html = '<ul class="vscode-tree-root">';
    nodes.forEach(node => {
        const iconClass = getIconClass(node.name, node.isFolder, node.isLink);
        const icon = `<span class="vscode-icon"><i class="${iconClass}"></i></span>`;
        const toggle = node.isFolder && node.children.length
            ? `<span class="vscode-tree-toggle" data-collapsed="false"></span>`
            : `<span class="vscode-tree-indent"></span>`;

        let labelHtml;
        const linkMatch = node.name.match(/^\[([^\]]+)\]\(([^)]+)\)$/);

        // 1. [파일명](링크) 패턴: 기존대로 링크 처리
        if (linkMatch) {
            let url = linkMatch[2];
            if (!/^https?:\/\//.test(url)) {
                url = url.replace(/^\/+/, '');
                url = baseUrl + url;
            }
            labelHtml = `<a href="${url}" target="_blank" rel="noopener noreferrer" class="vscode-tree-link">${linkMatch[1]}</a>`;
        }
        // 2. 폴더가 아니고 링크도 아니면, 자동으로 GitHub 파일 링크 처리
        else if (!node.isFolder && !node.isLink) {
            // parentPath가 있으면 경로 붙이기
            const filePath = (parentPath ? parentPath + "/" : "") + node.name;
            const url = baseUrl + filePath;
            labelHtml = `<a href="${url}" target="_blank" rel="noopener noreferrer" class="vscode-tree-link">${node.name}</a>`;
        }
        // 3. 폴더는 기존대로 span 처리
        else {
            labelHtml = `<span class="vscode-tree-label">${node.name}</span>`;
        }

        html += `<li class="vscode-tree-item ${node.isFolder ? 'folder' : 'file'}" data-depth="${depth}">`;
        html += `${toggle}${icon}${labelHtml}`;

        if (node.children.length) {
            // 폴더 경로 누적
            const nextParentPath = (parentPath ? parentPath + "/" : "") + node.name;
            html += `<div class="vscode-tree-children"${depth === 0 ? '' : ' style="display: none;"'}>`;
            html += renderDirectoryTree(node.children, depth + 1, owner, repo, folder, nextParentPath);
            html += `</div>`;
        }

        html += `</li>`;
    });
    html += '</ul>';
    return html;
}

function addTreeInteractivity(container) {
    container.querySelectorAll('.vscode-tree-item.folder > .vscode-tree-toggle').forEach(toggle => {
        toggle.innerHTML = getToggleSVG(false);
        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            const item = toggle.closest('.vscode-tree-item');
            const children = item.querySelector('.vscode-tree-children');
            const isCollapsed = children.style.display === 'none';

            children.style.display = isCollapsed ? 'block' : 'none';
            toggle.innerHTML = getToggleSVG(isCollapsed);
        });
    });

    // 호버링 이벤트: 하위에서 상위로 겹겹이 적용
    container.querySelectorAll('.vscode-tree-item').forEach(item => {
        item.addEventListener('mouseover', (e) => {
            e.stopPropagation();
            let current = item;
            while (current && current.classList.contains('vscode-tree-item')) {
                current.classList.add('hovered');
                // 상위 폴더로 이동
                current = current.parentElement.closest('.vscode-tree-item');
            }
        });
        item.addEventListener('mouseout', (e) => {
            e.stopPropagation();
            let current = item;
            while (current && current.classList.contains('vscode-tree-item')) {
                current.classList.remove('hovered');
                current = current.parentElement.closest('.vscode-tree-item');
            }
        });
    });
}

function getToggleSVG(collapsed) {
    return collapsed
        ? `<svg width="12" height="12" viewBox="0 0 12 12"><polyline points="3,4 6,8 9,4" style="fill:none;stroke:#42f5b3;stroke-width:2"/></svg>`
        : `<svg width="12" height="12" viewBox="0 0 12 12"><polyline points="4,3 8,6 4,9" style="fill:none;stroke:#42f5b3;stroke-width:2"/></svg>`;
}
