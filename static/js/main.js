/* static/js/main.js */
document.addEventListener('DOMContentLoaded', () => {
    // Form auto-submit on change
    const autoSubmitForms = document.querySelectorAll('form[data-auto-submit="true"]');
    autoSubmitForms.forEach(form => {
        const inputs = form.querySelectorAll('select, input[type="radio"], input[type="checkbox"]');
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                form.submit();
                // Show loading state if needed
                if (form.dataset.loadingTarget) {
                    const target = document.getElementById(form.dataset.loadingTarget);
                    if (target) {
                        target.innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';
                    }
                }
            });
        });
    });

    // Toggle section visibility
    const toggles = document.querySelectorAll('[data-toggle]');
    toggles.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = btn.dataset.toggle;
            const target = document.getElementById(targetId);
            if (target) {
                target.classList.toggle('show');
                btn.textContent = target.classList.contains('show') ? 'Hide Rows' : 'Show Rows';
            }
        });
    });
});
