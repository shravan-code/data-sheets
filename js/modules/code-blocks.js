/* Code Block Module JS */

(function () {
    function initCodeBlocks() {
        const preElements = document.querySelectorAll('pre');

        preElements.forEach(pre => {
            // Avoid re-initializing or wrapping already wrapped blocks
            if (pre.parentElement.classList.contains('ds-code-block') || pre.classList.contains('mermaid')) return;

            const code = pre.querySelector('code');
            if (!code) return;

            // Get language from class
            let lang = 'code';
            const langClass = Array.from(code.classList).find(c => c.startsWith('language-'));
            if (langClass) {
                lang = langClass.replace('language-', '');
            } else if (pre.previousElementSibling && pre.previousElementSibling.textContent.trim().toLowerCase() === 'python') {
                // Fallback for some specific markup patterns seen in snapshots
                lang = 'python';
            }

            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.className = 'ds-code-block';

            // Create header
            const header = document.createElement('div');
            header.className = 'ds-code-header';

            const langLabel = document.createElement('span');
            langLabel.className = 'ds-code-lang';
            langLabel.textContent = lang;

            const copyBtn = document.createElement('button');
            copyBtn.className = 'ds-code-copy';
            copyBtn.innerHTML = '<i data-lucide="copy"></i><span>Copy</span>';

            copyBtn.addEventListener('click', async () => {
                const text = code.textContent;
                try {
                    await navigator.clipboard.writeText(text);
                    const span = copyBtn.querySelector('span');
                    const icon = copyBtn.querySelector('i');

                    span.textContent = 'Copied!';
                    copyBtn.classList.add('text-accent-emerald');

                    if (typeof lucide !== 'undefined') {
                        copyBtn.innerHTML = '<i data-lucide="check"></i><span>Copied!</span>';
                        lucide.createIcons({ props: { class: 'w-3.5 h-3.5' }, nameAttr: 'data-lucide', attrs: { 'data-lucide': 'check' } });
                    }

                    setTimeout(() => {
                        span.textContent = 'Copy';
                        copyBtn.classList.remove('text-accent-emerald');
                        copyBtn.innerHTML = '<i data-lucide="copy"></i><span>Copy</span>';
                        if (typeof lucide !== 'undefined') lucide.createIcons();
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy!', err);
                }
            });

            header.appendChild(langLabel);
            header.appendChild(copyBtn);

            // Handle Output grouping
            let outputElement = null;
            let outputLabel = null;

            // Check if next element is an output label
            if (pre.nextElementSibling && pre.nextElementSibling.classList.contains('ds-output-label')) {
                outputLabel = pre.nextElementSibling;
                if (outputLabel.nextElementSibling && (outputLabel.nextElementSibling.tagName === 'PRE' || outputLabel.nextElementSibling.tagName === 'TABLE')) {
                    outputElement = outputLabel.nextElementSibling;
                }
            } else if (pre.nextElementSibling && (pre.nextElementSibling.classList.contains('language-output') || pre.nextElementSibling.classList.contains('output'))) {
                outputElement = pre.nextElementSibling;
            }

            // Wrap pre
            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(header);
            wrapper.appendChild(pre);

            // Add output if found
            if (outputElement) {
                if (outputLabel) wrapper.appendChild(outputLabel);
                
                // If it's a table, wrap it in an output container
                if (outputElement.tagName === 'TABLE') {
                    const outputContainer = document.createElement('div');
                    outputContainer.className = 'ds-output-container';
                    outputContainer.appendChild(outputElement);
                    wrapper.appendChild(outputContainer);
                } else {
                    outputElement.classList.add('ds-output-block');
                    wrapper.appendChild(outputElement);
                }
            }
        });
    }

    // Initialize on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCodeBlocks);
    } else {
        initCodeBlocks();
    }

    // Expose globally if needed
    window.dsInitCodeBlocks = initCodeBlocks;
})();
