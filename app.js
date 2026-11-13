const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

let websiteData = [];
let projectData = [];
let websiteStyle = 'multicolor';

const ASSET_LABELS = {
  icon: {label:'Icon SVG', caption:'512 × 512 transparent SVG master', ext:'svg'},
  banner: {label:'Banner SVG', caption:'Transparent SVG lockup · icon and project name', ext:'svg'},
  favicon: {label:'Favicon', caption:'Multi-resolution ICO · 16, 32, 48, 64, 128 and 256 px', ext:'ico'},
  apple: {label:'Apple touch icon', caption:'180 × 180 PNG', ext:'png'},
  og: {label:'Open Graph image', caption:'1200 × 630 PNG · social-sharing preview', ext:'png'}
};

function setTheme(mode, persist = true) {
  const theme = mode === 'oled' ? 'oled' : 'light';
  document.documentElement.dataset.theme = theme;
  $('#theme-toggle').setAttribute('aria-pressed', String(theme === 'oled'));
  $('#theme-label').textContent = theme === 'oled' ? 'White' : 'OLED black';
  $('#theme-icon').textContent = theme === 'oled' ? '☼' : '◐';
  $('meta[name="theme-color"]').content = theme === 'oled' ? '#000000' : '#ffffff';
  if (persist) {
    try { localStorage.setItem('levi-icon-study-theme', theme); } catch { /* Storage can be unavailable in private mode. */ }
  }
}

try { setTheme(localStorage.getItem('levi-icon-study-theme') || 'light', false); }
catch { setTheme('light', false); }
$('#theme-toggle').addEventListener('click', () => {
  setTheme(document.documentElement.dataset.theme === 'oled' ? 'light' : 'oled');
});

function setView(view, updateHash = true) {
  const selected = ['website', 'projects', 'official'].includes(view) ? view : 'website';
  $$('.view-tab').forEach((button) => {
    const active = button.dataset.view === selected;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-selected', String(active));
  });
  $$('.view-section').forEach((section) => {
    const active = section.id === selected;
    section.hidden = !active;
    section.classList.toggle('is-visible', active);
  });
  if (updateHash) history.replaceState(null, '', `#${selected}`);
}

$$('.view-tab').forEach((button) => button.addEventListener('click', () => setView(button.dataset.view)));
function initialView() {
  const hash = location.hash.slice(1);
  if (['website', 'projects', 'official'].includes(hash)) return hash;
  return 'website';
}

function setWebsiteStyle(style) {
  websiteStyle = style === 'filled' ? 'filled' : 'multicolor';
  $$('.style-tab').forEach((button) => {
    const active = button.dataset.style === websiteStyle;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-selected', String(active));
  });
  renderWebsiteIcons();
}
$$('.style-tab').forEach((button) => button.addEventListener('click', () => setWebsiteStyle(button.dataset.style)));

function websiteOption(option, item) {
  const file = `assets/icons/styles/${websiteStyle}/${option.name}.svg`;
  const best = option.name === item.recommended;
  return `<article class="website-option ${best ? 'recommended' : ''}">
    <div class="website-icon-surfaces">
      <div class="mini-surface"><img src="${file}" alt="${escapeHtml(option.name)} on white" loading="lazy"></div>
      <div class="mini-surface dark"><img src="${file}" alt="${escapeHtml(option.name)} on OLED black" loading="lazy"></div>
    </div>
    <strong>${escapeHtml(option.name)}</strong>
    <span class="option-status">${best ? 'Best fit for this placement' : 'Other option'}</span>
    <p>${escapeHtml(option.reason)}</p>
    <a class="text-link" href="${file}" download>Download SVG ↗</a>
  </article>`;
}

function renderWebsiteIcons() {
  const query = $('#website-search').value.trim().toLowerCase();
  const filtered = websiteData.filter((item) => [
    item.area, item.title, item.file, item.current, item.recommended,
    ...item.options.flatMap((option) => [option.name, option.reason])
  ].join(' ').toLowerCase().includes(query));

  $('#website-list').innerHTML = filtered.map((item) => {
    const currentFile = `assets/icons/current/${item.current}.svg`;
    return `<article class="website-card">
      <header class="card-heading">
        <div><span class="group-label">${escapeHtml(item.area)}</span><h3>${escapeHtml(item.title)}</h3><span class="source-file">${escapeHtml(item.file)}</span></div>
      </header>
      <div class="current-icon-row">
        <div class="current-icon-tile"><img src="${currentFile}" alt="Original ${escapeHtml(item.current)} icon" loading="lazy"></div>
        <div class="current-icon-copy"><strong>Current icon · original pixel artwork</strong><span>Original source SVG copied unchanged from <code>kit/assets/icons/${escapeHtml(item.current)}.svg</code></span></div>
        <a class="text-link" href="${currentFile}" download>Download original ↗</a>
      </div>
      <div class="website-options">${item.options.map((option) => websiteOption(option, item)).join('')}</div>
    </article>`;
  }).join('');
  $('#website-empty').hidden = filtered.length !== 0;
}
$('#website-search').addEventListener('input', renderWebsiteIcons);

function paletteDots(palette = []) {
  return `<div class="palette-dots" aria-label="Project-specific palette">${palette.map((colour) => `<span style="background:${escapeHtml(colour)}"></span>`).join('')}</div>`;
}
function assetPath(variant, asset) {
  if (asset === 'icon') return variant.file;
  if (asset === 'banner') return variant.banner;
  if (asset === 'favicon') return variant.favicon.replace(/\.ico$/i, '-256x256.png');
  if (asset === 'apple') return variant.apple_touch_icon;
  return variant.og_image;
}

function proposedPreview(project, variant, asset) {
  const src = assetPath(variant, asset);
  const alt = `${project.name} proposed ${variant.label} ${ASSET_LABELS[asset].label}`;
  const previewClass = asset;
  const downloadHref = asset === 'favicon' ? variant.favicon : src;
  const sourceHref = asset === 'og' ? variant.og_image_svg : '';
  const sizeLinks = asset === 'favicon'
    ? `<div class="asset-size-links"><a href="${escapeHtml(variant.favicon)}" download>ICO</a>${[16,32,48,64,128,256].map((size) => {
        const base = variant.favicon.replace(/\.ico$/i, '');
        const png = variant.favicon.includes('/variants/')
          ? `${base}-${size}x${size}.png`
          : `${base.replace(/favicon$/, 'favicon')}-${size}x${size}.png`;
        return `<a href="${escapeHtml(png)}" download>${size}px PNG</a>`;
      }).join('')}</div>`
    : '';
  return `<div class="asset-preview ${previewClass}"><img src="${escapeHtml(src)}" alt="${escapeHtml(alt)}" loading="lazy"></div>
    <div class="asset-meta">
      <span class="asset-caption">${ASSET_LABELS[asset].caption}</span>
      <div class="asset-actions">
        <a href="${escapeHtml(downloadHref)}" download>Download ${asset === 'favicon' ? 'ICO' : ASSET_LABELS[asset].ext.toUpperCase()}</a>
        ${sourceHref ? `<a href="${escapeHtml(sourceHref)}" download>Download OG SVG source</a>` : ''}
      </div>
      ${sizeLinks}
    </div>`;
}

function projectCard(project, index) {
  const variantTabs = project.variants.map((variant) => `<button class="variant-tab" type="button" role="tab" data-variant="${escapeHtml(variant.slug)}" aria-selected="false">${escapeHtml(variant.label)}</button>`).join('');
  const assetTabs = Object.entries(ASSET_LABELS).map(([key, meta], position) => `<button class="asset-tab" type="button" role="tab" data-asset="${key}" aria-selected="${position === 0}">${meta.label}</button>`).join('');
  return `<article class="project-card" data-project="${escapeHtml(project.slug)}" data-variant="" data-asset="icon">
    <header class="project-head">
      <div><span class="project-index">PROJECT ${String(index + 1).padStart(2, '0')}</span><h3>${escapeHtml(project.name)}</h3><p class="project-summary">${escapeHtml(project.summary)}</p></div>
      ${paletteDots(project.palette)}
    </header>
    <div class="variant-picker">
      <span class="picker-label">Select a proposed direction</span>
      <div class="variant-tabs" role="tablist" aria-label="${escapeHtml(project.name)} proposed logo concepts">${variantTabs}</div>
    </div>
    <div class="logo-comparison">
      <section class="logo-column current-column">
        <div class="column-heading"><strong>Current logo</strong><a href="${escapeHtml(project.current_source)}" target="_blank" rel="noreferrer">Original source ↗</a></div>
        <div class="current-logo-stage"><img src="${escapeHtml(project.current_icon)}" alt="Current ${escapeHtml(project.name)} logo" loading="lazy" data-current-logo></div>
        <p class="column-note">Existing project artwork · displayed as published</p>
      </section>
      <section class="logo-column proposed-column">
        <div class="column-heading"><strong>Proposed logo</strong><span class="proposed-label">Choose a direction</span></div>
        <div class="proposed-empty"><span class="empty-mark">＋</span><strong>No concept selected</strong><p>Select one of the proposed directions above to compare it with the current logo.</p></div>
        <div class="proposed-output" hidden>
          <div class="proposed-description"></div>
          <div class="asset-tabs" role="tablist" aria-label="${escapeHtml(project.name)} proposed assets">${assetTabs}</div>
          <div class="preview-slot"></div>
          <div class="project-detail"><a class="text-link" href="${escapeHtml(project.asset_bundle)}" download>Download complete project asset family ↗</a></div>
        </div>
      </section>
    </div>
  </article>`;
}

function renderProjects() {
  const query = $('#project-search').value.trim().toLowerCase();
  const filtered = projectData.filter((project) => [
    project.name, project.summary, project.subtitle,
    ...project.variants.flatMap((variant) => [variant.label, variant.description, variant.slug])
  ].join(' ').toLowerCase().includes(query));
  $('#project-list').innerHTML = filtered.map(projectCard).join('');
  $('#project-empty').hidden = filtered.length !== 0;
}

function updateProjectCard(card) {
  const project = projectData.find((entry) => entry.slug === card.dataset.project);
  if (!project || !card.dataset.variant) return;
  const variant = project.variants.find((entry) => entry.slug === card.dataset.variant);
  if (!variant) return;
  const asset = card.dataset.asset || 'icon';
  const proposed = $('.proposed-output', card);
  $('.proposed-empty', card).hidden = true;
  proposed.hidden = false;
  $('.proposed-label', card).textContent = variant.label;
  $('.proposed-description', card).innerHTML = `<strong>${escapeHtml(variant.label)}</strong><p>${escapeHtml(variant.description)}</p>`;
  $$('.asset-tab', card).forEach((button) => button.setAttribute('aria-selected', String(button.dataset.asset === asset)));
  $('.preview-slot', card).innerHTML = proposedPreview(project, variant, asset);
}

$('#project-search').addEventListener('input', renderProjects);
$('#project-list').addEventListener('click', (event) => {
  const card = event.target.closest('.project-card');
  if (!card) return;
  const variantButton = event.target.closest('.variant-tab');
  const assetButton = event.target.closest('.asset-tab');
  if (variantButton) {
    card.dataset.variant = variantButton.dataset.variant;
    card.dataset.asset = 'icon';
    $$('.variant-tab', card).forEach((button) => button.setAttribute('aria-selected', String(button === variantButton)));
    updateProjectCard(card);
  } else if (assetButton && card.dataset.variant) {
    card.dataset.asset = assetButton.dataset.asset;
    updateProjectCard(card);
  }
});

$('#project-list').addEventListener('error', (event) => {
  if (event.target.matches('[data-current-logo]')) {
    event.target.classList.add('logo-load-failed');
    const stage = event.target.closest('.current-logo-stage');
    if (stage) stage.insertAdjacentHTML('beforeend', '<span class="logo-fallback">Current logo could not be loaded. Use the original source link above.</span>');
  }
}, true);

function renderOfficialQuickLinks() {
  $('#official-project-links').innerHTML = projectData.map((project) => `<button class="quick-project" type="button" data-go-project="${escapeHtml(project.slug)}"><img src="${escapeHtml(project.icon)}" alt="" loading="lazy"><span>${escapeHtml(project.name)}</span></button>`).join('');
}
$('#official-project-links').addEventListener('click', (event) => {
  const button = event.target.closest('[data-go-project]');
  if (!button) return;
  $('#project-search').value = '';
  renderProjects();
  setView('projects');
  const target = $(`[data-project="${CSS.escape(button.dataset.goProject)}"]`, $('#project-list'));
  target?.scrollIntoView({behavior:'smooth', block:'center'});
});

Promise.all([
  fetch('data.json').then((response) => { if (!response.ok) throw new Error('Website icon data failed to load'); return response.json(); }),
  fetch('official/manifest.json').then((response) => { if (!response.ok) throw new Error('Project logo manifest failed to load'); return response.json(); })
]).then(([websiteIcons, manifest]) => {
  websiteData = websiteIcons;
  projectData = manifest.projects;
  $('#website-count').textContent = String(websiteIcons.length);
  $('#website-icon-count').textContent = String(websiteIcons.reduce((sum, item) => sum + item.options.length, 0));
  $('#project-count').textContent = String(projectData.length);
  $('#project-icon-count').textContent = String(manifest.icons.length);
  renderWebsiteIcons();
  renderProjects();
  renderOfficialQuickLinks();
  setView(initialView(), false);
}).catch((error) => {
  $('#website-list').innerHTML = `<p class="empty">${escapeHtml(error.message)}. Open the gallery through a local HTTP server, not a file URL.</p>`;
  $('#project-list').innerHTML = `<p class="empty">${escapeHtml(error.message)}.</p>`;
});
