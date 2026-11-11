const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
let v1Data = [];
let projectData = [];

const ASSET_LABELS = {
  icon: {label:'Main SVG icon', caption:'512 × 512 transparent SVG master', ext:'svg'},
  banner: {label:'Icon banner', caption:'Transparent SVG lockup with project name', ext:'svg'},
  favicon: {label:'Multi-resolution favicon', caption:'ICO containing 16, 32, 48, 64, 128 and 256 px images', ext:'ico'},
  apple: {label:'Apple touch icon', caption:'180 × 180 PNG', ext:'png'},
  og: {label:'Open Graph image', caption:'1200 × 630 PNG · social preview', ext:'png'}
};

function setTheme(mode, persist = true) {
  const theme = mode === 'oled' ? 'oled' : 'light';
  document.documentElement.dataset.theme = theme;
  $('#theme-toggle').setAttribute('aria-pressed', String(theme === 'oled'));
  $('#theme-label').textContent = theme === 'oled' ? 'White' : 'OLED black';
  $('#theme-icon').textContent = theme === 'oled' ? '☼' : '◐';
  $('meta[name="theme-color"]').content = theme === 'oled' ? '#000000' : '#ffffff';
  if (persist) { try { localStorage.setItem('levi-icon-study-theme', theme); } catch {} }
}
try { setTheme(localStorage.getItem('levi-icon-study-theme') || 'light', false); } catch { setTheme('light', false); }
$('#theme-toggle').addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'oled' ? 'light' : 'oled'));

function setView(view, updateHash = true) {
  const selected = ['v1','projects','official'].includes(view) ? view : 'v1';
  $$('.view-tab').forEach(button => {
    const active = button.dataset.view === selected;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-selected', String(active));
  });
  $$('.view-section').forEach(section => {
    const active = section.id === selected;
    section.hidden = !active;
    section.classList.toggle('is-visible', active);
  });
  if (updateHash) history.replaceState(null, '', `#${selected}`);
  window.scrollTo({top:0,behavior:'smooth'});
}
$$('.view-tab').forEach(button => button.addEventListener('click', () => setView(button.dataset.view)));
function initialView() {
  const hash = location.hash.replace('#','');
  if (hash === 'official') return 'official';
  if (hash === 'projects' || hash === 'v2') return 'projects';
  return 'v1';
}

function v1Option(option, item) {
  const file = `assets/icons/${option.name}.svg`;
  const best = option.name === item.recommended;
  return `<article class="v1-option ${best ? 'recommended' : ''}">
    <div class="v1-icon-surfaces">
      <div class="mini-surface"><img src="${file}" alt="${escapeHtml(option.name)} on white" loading="lazy"></div>
      <div class="mini-surface dark"><img src="${file}" alt="${escapeHtml(option.name)} on OLED black" loading="lazy"></div>
    </div>
    <strong>${escapeHtml(option.name)}</strong>
    <span class="option-status">${best ? 'Recommended' : 'Alternative'}</span>
    <p>${escapeHtml(option.reason)}</p>
    <a class="text-link" href="${file}" download>Download SVG ↗</a>
  </article>`;
}
function renderV1() {
  const query = $('#v1-search').value.trim().toLowerCase();
  const filtered = v1Data.filter(item => [item.area,item.title,item.file,item.current,item.recommended,...item.options.flatMap(x=>[x.name,x.reason])].join(' ').toLowerCase().includes(query));
  $('#v1-list').innerHTML = filtered.map(item => {
    const currentFile = `assets/icons/current/${item.current}.svg`;
    return `<article class="v1-card">
      <header class="card-heading"><div><span class="group-label">${escapeHtml(item.area)}</span><h3>${escapeHtml(item.title)}</h3><span class="source-file">${escapeHtml(item.file)}</span></div></header>
      <div class="current-icon-row">
        <div class="current-icon-tile"><img src="${currentFile}" alt="Original ${escapeHtml(item.current)} icon" loading="lazy"></div>
        <div class="current-icon-copy"><strong>Current icon · original source SVG</strong><span>Copied unchanged from <code>kit/assets/icons/${escapeHtml(item.current)}.svg</code></span></div>
        <a class="text-link" href="${currentFile}" download>Download original ↗</a>
      </div>
      <div class="v1-options">${item.options.map(option => v1Option(option,item)).join('')}</div>
    </article>`;
  }).join('');
  $('#v1-empty').hidden = filtered.length !== 0;
}
$('#v1-search').addEventListener('input', renderV1);

function paletteDots(palette = []) { return `<div class="palette-dots" aria-label="Project palette">${palette.map(colour=>`<span style="background:${escapeHtml(colour)}"></span>`).join('')}</div>`; }
function v2Path(path) { return `official/${String(path).replace(/^\/+/, '')}`; }

function previewHtml(project, selectedVariant, asset) {
  const master = project.variants.find(v=>v.recommended) || project.variants[0];
  const variant = project.variants.find(v=>v.slug===selectedVariant) || master;
  let src = project.icon;
  let download = project.icon;
  let alt = `${project.name} ${variant.label}`;
  let klass = asset;
  if (asset === 'icon') { src = v2Path(variant.file); download = v2Path(variant.file); }
  if (asset === 'banner') { src = v2Path(project.banner); download = v2Path(project.banner); }
  if (asset === 'favicon') { src = v2Path(project.favicon_png); download = v2Path(project.favicon); }
  if (asset === 'apple') { src = v2Path(project.apple_touch_icon); download = v2Path(project.apple_touch_icon); }
  if (asset === 'og') { src = v2Path(project.og_image); download = v2Path(project.og_image); alt = `${project.name} social preview`; }
  const external = asset === 'og' ? `<a href="${escapeHtml(v2Path(project.og_image_svg))}" download>OG SVG source</a>` : '';
  return `<div class="asset-preview ${klass}"><img src="${escapeHtml(src)}" alt="${escapeHtml(alt)}" loading="lazy"></div>
    <div class="asset-meta"><span class="asset-caption">${ASSET_LABELS[asset].caption}</span><div class="asset-actions"><a href="${escapeHtml(download)}" download>Download ${ASSET_LABELS[asset].ext.toUpperCase()}</a>${external}</div></div>`;
}
function projectCard(project, index) {
  const master = project.variants.find(v=>v.recommended) || project.variants[0];
  const variants = project.variants.map(v=>`<button class="variant-button" type="button" data-variant="${escapeHtml(v.slug)}" aria-pressed="${v.slug===master.slug}">${escapeHtml(v.label)}</button>`).join('');
  const tabs = Object.entries(ASSET_LABELS).map(([id,meta],i)=>`<button class="asset-tab" type="button" role="tab" data-asset="${id}" aria-selected="${i===0}">${meta.label}</button>`).join('');
  return `<article class="project-card" data-project="${escapeHtml(project.slug)}" data-variant="${escapeHtml(master.slug)}" data-asset="icon">
    <header class="project-head"><div><span class="project-index">PROJECT ${String(index+1).padStart(2,'0')}</span><h3>${escapeHtml(project.name)}</h3><p class="project-summary">${escapeHtml(project.summary)}</p></div>${paletteDots(project.palette)}</header>
    <div class="variant-row">${variants}</div>
    <div class="asset-tabs" role="tablist" aria-label="${escapeHtml(project.name)} assets">${tabs}</div>
    <div class="preview-slot">${previewHtml(project,master.slug,'icon')}</div>
    <div class="project-detail"><strong>Direction:</strong> ${escapeHtml(master.description)} <span> · </span><a class="text-link" href="${escapeHtml(v2Path(project.asset_bundle))}" download>Download complete asset family ↗</a></div>
  </article>`;
}
function renderProjects() {
  const query = $('#project-search').value.trim().toLowerCase();
  const filtered = projectData.filter(p => [p.name,p.summary,p.subtitle,...p.variants.flatMap(v=>[v.label,v.description,v.slug])].join(' ').toLowerCase().includes(query));
  $('#project-list').innerHTML = filtered.map(projectCard).join('');
  $('#project-empty').hidden = filtered.length !== 0;
}
$('#project-search').addEventListener('input', renderProjects);
$('#project-list').addEventListener('click', event => {
  const card = event.target.closest('.project-card');
  if (!card) return;
  const project = projectData.find(p=>p.slug===card.dataset.project);
  if (!project) return;
  const variantButton = event.target.closest('[data-variant]');
  const assetButton = event.target.closest('[data-asset]');
  if (variantButton) {
    card.dataset.variant = variantButton.dataset.variant;
    $$('.variant-button',card).forEach(btn=>btn.setAttribute('aria-pressed',String(btn===variantButton)));
  }
  if (assetButton) {
    card.dataset.asset = assetButton.dataset.asset;
    $$('.asset-tab',card).forEach(btn=>btn.setAttribute('aria-selected',String(btn===assetButton)));
  }
  const selected = project.variants.find(v=>v.slug===card.dataset.variant) || project.variants[0];
  card.querySelector('.preview-slot').innerHTML = previewHtml(project,selected.slug,card.dataset.asset);
  card.querySelector('.project-detail').innerHTML = `<strong>Direction:</strong> ${escapeHtml(selected.description)} <span> · </span><a class="text-link" href="${escapeHtml(v2Path(project.asset_bundle))}" download>Download complete asset family ↗</a>`;
});

function renderOfficialQuickLinks() {
  $('#official-project-links').innerHTML = projectData.map(p=>`<button class="quick-project" type="button" data-go-project="${escapeHtml(p.slug)}"><img src="${escapeHtml(v2Path(p.icon))}" alt="" loading="lazy"><span>${escapeHtml(p.name)}</span></button>`).join('');
}
$('#official-project-links').addEventListener('click', event => {
  const btn = event.target.closest('[data-go-project]');
  if (!btn) return;
  setView('projects');
  const target = $(`[data-project="${CSS.escape(btn.dataset.goProject)}"]`, $('#project-list'));
  if (target) target.scrollIntoView({behavior:'smooth',block:'center'});
});

Promise.all([fetch('data.json').then(r=>{if(!r.ok)throw new Error('V1 data failed to load');return r.json();}),fetch('official/manifest.json').then(r=>{if(!r.ok)throw new Error('V2 manifest failed to load');return r.json();})]).then(([v1,manifest])=>{
  v1Data=v1; projectData=manifest.projects.map(p=>({...p, favicon_png:p.favicon.replace('favicon.ico','favicon-256x256.png')}));
  $('#v1-count').textContent=String(v1.length);
  $('#v1-icon-count').textContent=String(v1.reduce((sum,x)=>sum+x.options.length,0));
  $('#project-count').textContent=String(projectData.length);
  $('#project-icon-count').textContent=String(manifest.icons.length);
  renderV1();renderProjects();renderOfficialQuickLinks();setView(initialView(),false);
}).catch(error=>{
  $('#v1-list').innerHTML=`<p class="empty">${escapeHtml(error.message)}. Run the site through a local HTTP server rather than a file URL.</p>`;
  $('#project-list').innerHTML=`<p class="empty">${escapeHtml(error.message)}.</p>`;
});
