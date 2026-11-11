const projectList = document.querySelector('#project-list');
const searchInput = document.querySelector('#search');
const empty = document.querySelector('#empty');
const themeToggle = document.querySelector('#theme-toggle');
const themeLabel = document.querySelector('#theme-label');
const themeIcon = document.querySelector('#theme-icon');
let manifest;

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

function setTheme(theme, persist = true) {
  const selected = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = selected;
  themeToggle.setAttribute('aria-pressed', String(selected === 'dark'));
  themeLabel.textContent = selected === 'dark' ? 'Light gallery' : 'Dark gallery';
  themeIcon.textContent = selected === 'dark' ? '☼' : '◐';
  document.querySelector('meta[name="theme-color"]').content = selected === 'dark' ? '#142619' : '#f1f4eb';
  if (persist) {
    try { localStorage.setItem('levi-icon-preview-theme', selected); } catch { /* Storage may be disabled. */ }
  }
}

let initialTheme = 'light';
try { initialTheme = localStorage.getItem('levi-icon-preview-theme') || 'light'; } catch { /* Keep the light default. */ }
setTheme(initialTheme, false);
themeToggle.addEventListener('click', () => {
  setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
});

function surfacePreview(src, label) {
  const safe = escapeHtml(src);
  const alt = escapeHtml(label);
  return `<div class="neutrality-preview">
    <div class="surface surface-light"><span class="surface-label">LIGHT</span><img src="${safe}" alt="${alt} on a light surface" loading="lazy"></div>
    <div class="surface surface-dark"><span class="surface-label">DARK</span><img src="${safe}" alt="${alt} on a dark surface" loading="lazy"></div>
  </div>`;
}

function variantCard(variant) {
  const file = escapeHtml(variant.file);
  const label = escapeHtml(variant.label);
  return `<article class="concept ${variant.recommended ? 'recommended' : ''}">
    <div class="concept-title-row"><h4>${label}</h4>${variant.recommended ? '<span class="concept-tag">Master</span>' : '<span class="concept-tag">Alternative</span>'}</div>
    ${surfacePreview(file, label)}
    <p>${escapeHtml(variant.description)}</p>
    <div class="concept-actions"><a href="${file}" target="_blank" rel="noreferrer">Open SVG ↗</a><a href="${file}" download>Download SVG</a></div>
  </article>`;
}

function assetLink(path, label, filename) {
  const p = escapeHtml(path);
  return `<a href="${p}" download="${escapeHtml(filename || path.split('/').pop())}">${escapeHtml(label)}</a>`;
}

function projectCard(project, index) {
  const slug = escapeHtml(project.slug);
  const variants = project.variants.map(variantCard).join('');
  const assets = [
    assetLink(project.icon, 'Primary SVG'),
    assetLink(project.banner, 'Banner SVG'),
    assetLink(project.favicon, 'Multi-size ICO'),
    assetLink(project.apple_touch_icon, 'Apple 180 PNG'),
    assetLink(project.og_image, 'OG 1200×630 PNG'),
    assetLink(project.og_image_svg, 'OG SVG source'),
    assetLink(project.asset_bundle, 'Complete asset-family ZIP')
  ].join('');
  return `<section class="project" data-project="${slug}">
    <header class="project-head">
      <div><span class="project-kicker">Project ${String(index + 1).padStart(2, '0')}</span><h3>${escapeHtml(project.name)}</h3><p class="project-description">${escapeHtml(project.summary)}</p></div>
      <span class="recommended-label">Master: ${escapeHtml(project.variants.find(v => v.recommended)?.label || '—')}</span>
    </header>
    <div class="concepts">${variants}</div>
    <div class="project-assets">
      <div><h4>Complete identity assets</h4><p>All derivatives are generated from the primary <code>icon.svg</code>. Use the SVG source as the editable master; replace raster exports only by regenerating them.</p><div class="asset-links">${assets}</div></div>
      <a href="${escapeHtml(project.og_image)}" target="_blank" rel="noreferrer" aria-label="Preview ${escapeHtml(project.name)} Open Graph image"><img class="og-thumb" src="${escapeHtml(project.og_image)}" alt="${escapeHtml(project.name)} Open Graph image" loading="lazy"></a>
    </div>
  </section>`;
}

function renderProjects() {
  const query = searchInput.value.trim().toLowerCase();
  const filtered = manifest.projects.filter((project) => {
    const searchable = [project.name, project.summary, project.subtitle, ...project.variants.flatMap(v => [v.label, v.description, v.slug])].join(' ').toLowerCase();
    return !query || searchable.includes(query);
  });
  projectList.innerHTML = filtered.map(projectCard).join('');
  empty.hidden = filtered.length !== 0;
}

searchInput.addEventListener('input', renderProjects);
fetch('manifest.json').then((response) => {
  if (!response.ok) throw new Error(`Could not load the SVG manifest (${response.status})`);
  return response.json();
}).then((data) => {
  manifest = data;
  document.querySelector('#project-count').textContent = String(data.projects.length);
  document.querySelector('#icon-count').textContent = String(data.icons.length);
  renderProjects();
}).catch((error) => {
  projectList.innerHTML = `<p class="empty">${escapeHtml(error.message)}. Open this page through a local web server or GitHub Pages.</p>`;
});
