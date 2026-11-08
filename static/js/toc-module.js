document.addEventListener('DOMContentLoaded', () => {
    const content = document.querySelector('.reference-content');
    if (!content) return;
    const headings = [...content.querySelectorAll('h1, h2, h3')];
    if (!headings.length) return;

    const details = document.createElement('details');
    details.className = 'document-toc';
    const summary = document.createElement('summary');
    summary.textContent = '문서 목차';
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', '문서 목차');
    const list = document.createElement('ul');
    headings.forEach((heading, index) => {
        if (!heading.id) heading.id = `document-heading-${index}`;
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${heading.id}`;
        link.textContent = heading.textContent.trim();
        item.append(link);
        list.append(item);
    });
    nav.append(list);
    details.append(summary, nav);
    content.prepend(details);
});
