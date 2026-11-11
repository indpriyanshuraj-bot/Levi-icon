const cards = document.querySelector('#cards');
const searchInput = document.querySelector('#search');
const areaSelect = document.querySelector('#area-filter');
const empty = document.querySelector('#empty');
let proposals = [];

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const iconPath = (name) => `assets/icons/${name}.svg`;
const currentPath = (name) => `assets/icons/current/${name}.svg`;
const iconTones = {
  blue: new Set(['devices', 'laptop', 'smartphone', 'user-round', 'users', 'info']),
  cyan: new Set(['terminal', 'code', 'braces', 'file-code', 'git-branch', 'git-pull-request', 'code-merge', 'wrench']),
  violet: new Set(['languages', 'book-open', 'bookmark', 'file-text', 'scroll', 'id-card']),
  green: new Set(['server', 'database', 'network', 'package-check', 'layers', 'blocks', 'folder', 'grid', 'github', 'circle-dollar']),
  orange: new Set(['download', 'lightbulb', 'message-question', 'badge-help']),
  rose: new Set(['gamepad', 'person-play', 'heart', 'heart-handshake']),
};
const toneFor = (name) => Object.entries(iconTones).find(([, names]) => names.has(name))?.[0] ?? 'blue';

function renderOption(icon, index, recommended) {
  const [name, status, reason] = icon;
  const best = name === recommended;
  return `<article class="option ${best ? 'best' : ''}">
    <span class="icon-frame tone-${toneFor(name)}"><img src="${iconPath(name)}" alt="" loading="lazy"></span>
    <span class="option-name">${escapeHtml(name)}</span>
    <small>${escapeHtml(status)}</small>
    <p>${escapeHtml(reason)}</p>
    <div class="option-actions">
      <button type="button" data-copy="${escapeHtml(name)}">copy path</button>
      <button type="button" data-download="${escapeHtml(name)}">download</button>
    </div>
  </article>`;
}

function renderCard(item) {
  return `<article class="proposal" data-id="${escapeHtml(item.id)}">
    <div class="proposal-head"><div><span class="area">${escapeHtml(item.area)}</span><h3>${escapeHtml(item.title)}</h3><div class="file">${escapeHtml(item.file)}</div></div></div>
    <div class="compare">
      <div class="current"><span class="icon-frame current-tone"><img src="${currentPath(item.current)}" alt="" loading="lazy"></span><small>Current · ${escapeHtml(item.current)}</small></div>
      <div class="arrow" aria-hidden="true">→</div>
      <div class="option-list">${item.options.map((option, index) => renderOption(option, index, item.recommended)).join('')}</div>
    </div>
    <p class="why">${escapeHtml(item.why)}</p>
  </article>`;
}

function applyFilters() {
  const query = searchInput.value.trim().toLowerCase();
  const area = areaSelect.value;
  const filtered = proposals.filter((item) => {
    const searchable = [item.area, item.title, item.file, item.current, item.why, ...item.options.flat()].join(' ').toLowerCase();
    return (!query || searchable.includes(query)) && (area === 'all' || item.area === area);
  });
  cards.innerHTML = filtered.map(renderCard).join('');
  empty.hidden = filtered.length !== 0;
}

async function copyText(value) {
  try {
    await navigator.clipboard.writeText(value);
    return true;
  } catch {
    window.prompt('Copy this text:', value);
    return false;
  }
}

cards.addEventListener('click', async (event) => {
  const button = event.target.closest('button');
  if (!button) return;
  if (button.dataset.copy) {
    const name = button.dataset.copy;
    await copyText(`assets/icons/${name}.svg`);
    button.textContent = 'copied';
    window.setTimeout(() => { button.textContent = 'copy path'; }, 1100);
  }
  if (button.dataset.download) {
    const name = button.dataset.download;
    const link = document.createElement('a');
    link.href = iconPath(name);
    link.download = `${name}.svg`;
    document.body.append(link);
    link.click();
    link.remove();
  }
});

searchInput.addEventListener('input', applyFilters);
areaSelect.addEventListener('change', applyFilters);
document.querySelector('#copy-map').addEventListener('click', async (event) => {
  const lines = ['| Area | Placement | Current | Recommended | Alternatives |', '|---|---|---|---|---|'];
  for (const item of proposals) {
    const other = item.options.filter((option) => option[0] !== item.recommended).map((option) => option[0]).join(', ');
    lines.push(`| ${item.area} | ${item.title} | ${item.current} | **${item.recommended}** | ${other} |`);
  }
  await copyText(lines.join('\n'));
  const button = event.currentTarget;
  button.textContent = 'Copied mapping';
  window.setTimeout(() => { button.textContent = 'Copy mapping'; }, 1500);
});

fetch('data.json').then((response) => {
  if (!response.ok) throw new Error(`Could not load proposal data (${response.status})`);
  return response.json();
}).then((data) => {
  proposals = data;
  document.querySelector('#stat-points').textContent = String(data.length);
  document.querySelector('#stat-options').textContent = String(data.reduce((total, item) => total + item.options.length, 0));
  for (const area of [...new Set(data.map((item) => item.area))]) {
    const option = document.createElement('option');
    option.value = area;
    option.textContent = area;
    areaSelect.append(option);
  }
  applyFilters();
}).catch((error) => {
  cards.innerHTML = `<p class="empty">${escapeHtml(error.message)}. Open this project through a local web server or GitHub Pages; browser file URLs may block data.json.</p>`;
});
