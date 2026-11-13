/* LeviMC icon review — data-driven comparison app.
   Everything it shows comes from data.json. Add an icon, add an entry, it appears. */

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const STORE = 'levi-icon-review-v1';

const state = {
  data: null,
  collection: null,
  decisions: {},
  activeId: null,
  preview: {},
  filter: 'all',
};

/* ------------------------------------------------------------ helpers */

const kebab = (name) => String(name).replace(/[A-Z]/g, (m) => '-' + m.toLowerCase());

function items() {
  return state.collection.groups.flatMap((group) =>
    group.items.map((item) => Object.assign({}, item, { group })),
  );
}

function activeItem() {
  return items().find((item) => item.id === state.activeId) || items()[0];
}

function optionOf(item, name) {
  return (item.options || []).find((o) => o.name === name || o.label === name);
}

function decisionOf(item) {
  return state.decisions[item.id] || null;
}

function optionSrc(option) {
  if (option.src) return option.src;
  return `${state.collection.optionBase}/${option.name}.svg`;
}

function tintOf(option) {
  const tokens = state.data.tokens || {};
  return option.color || tokens[option.token] || 'currentColor';
}

/* current icon: hotlinked from the source repository, never copied */
function spriteHTML(item, size, cls = '') {
  const c = item.current;
  const base = state.collection.currentBase;
  const fallback = state.collection.currentFallback || base;
  const file = kebab(c.name);
  const mono = (c.palette || [])[0] === 'currentColor' ? ' mono' : '';
  return `<img class="sprite${mono} ${cls}" src="${base}/${file}.svg" data-fallback="${fallback}/${file}.svg"
    onerror="if(this.dataset.retried){this.style.visibility='hidden'}else{this.dataset.retried=1;this.src=this.dataset.fallback}"
    width="${size}" height="${size}" alt="" draggable="false">`;
}

/* candidate icon: masked so one file can carry any token colour */
function maskHTML(option, size, cls = '') {
  return `<span class="mask ${cls}" style="--src:url('${optionSrc(option)}');--tint:${tintOf(option)};width:${size}px;height:${size}px" aria-hidden="true"></span>`;
}

function chosenHTML(item, size, cls = '') {
  const choice = decisionOf(item);
  if (!choice) return '<span class="chip-tag">—</span>';
  if (choice === 'keep') return spriteHTML(item, size, cls);
  const option = optionOf(item, choice);
  return option ? maskHTML(option, size, cls) : '<span class="chip-tag">—</span>';
}

/* ------------------------------------------------------------ persistence */

function load() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE) || '{}');
    state.decisions = raw[state.collection.id] || {};
  } catch { state.decisions = {}; }
}

function save() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE) || '{}');
    raw[state.collection.id] = state.decisions;
    localStorage.setItem(STORE, JSON.stringify(raw));
  } catch { /* private mode: decisions stay in memory */ }
}

/* ------------------------------------------------------------ chrome */

function renderGroups() {
  const nav = $('#groups');
  const groups = state.collection.groups;
  const all = [{ id: 'all', title: 'All' }].concat(groups);
  nav.innerHTML = all
    .map((g) => `<button type="button" data-group="${g.id}" aria-current="${state.filter === g.id}">${g.title}</button>`)
    .join('');
  $$('button', nav).forEach((btn) =>
    btn.addEventListener('click', () => {
      state.filter = btn.dataset.group;
      renderGroups();
      renderRail();
      const first = visibleItems()[0];
      if (first) setActive(first.id);
    }),
  );
}

function visibleItems() {
  const list = items();
  return state.filter === 'all' ? list : list.filter((i) => i.group.id === state.filter);
}

function renderRail() {
  const rail = $('#rail');
  const groups = state.collection.groups.filter((g) => state.filter === 'all' || g.id === state.filter);
  rail.innerHTML = groups
    .map((group) => {
      const rows = group.items
        .map((item) => {
          const choice = decisionOf(item);
          const dotState = !choice ? '' : choice === 'keep' ? 'keep' : 'set';
          return `<button class="row" type="button" data-id="${item.id}" aria-current="${item.id === state.activeId}">
            <span class="row-thumb">${spriteHTML(item, 24)}</span>
            <span class="row-text">
              <span class="row-title">${item.title}</span>
              <span class="row-ref">${item.ref || ''}</span>
            </span>
            <span class="row-dot" data-state="${dotState}"></span>
          </button>`;
        })
        .join('');
      return `<p class="rail-group">${group.title}</p>${rows}`;
    })
    .join('');

  $$('.row', rail).forEach((row) =>
    row.addEventListener('click', () => setActive(row.dataset.id)),
  );
}

function setActive(id) {
  state.activeId = id;
  if (state.preview[id] === undefined) state.preview[id] = 0;
  renderRail();
  renderStage();
  const current = $(`.row[data-id="${id}"]`);
  if (current && current.scrollIntoView) current.scrollIntoView({ block: 'nearest' });
}

function renderProgress() {
  const total = items().length;
  const done = items().filter((i) => decisionOf(i)).length;
  $('#progress-count').textContent = `${done} / ${total}`;
  $('#progress-fill').style.width = total ? `${(done / total) * 100}%` : '0';
}

/* ------------------------------------------------------------ stage */

function renderStage() {
  const item = activeItem();
  if (!item) return;
  const group = item.group;
  const index = state.preview[item.id] || 0;
  const option = item.options[index];
  const choice = decisionOf(item);
  const list = visibleItems();
  const pos = list.findIndex((i) => i.id === item.id) + 1;

  const ladderSizes = [16, 24, 32, 64];

  $('#stage').innerHTML = `
    <div class="stage-head">
      <div>
        <p class="eyebrow">${group.title}</p>
        <h1>${item.title}</h1>
        <p class="stage-meta">
          <code>${item.ref || ''}</code>
          <span>${item.size} px on the site</span>
          ${choice ? `<span class="chip-tag">${choice === 'keep' ? 'keeping current' : 'chosen: ' + choice}</span>` : ''}
        </p>
      </div>
      <div class="counter"><b>${String(pos).padStart(2, '0')}</b> / ${String(list.length).padStart(2, '0')}</div>
    </div>

    <div class="compare">
      <section class="pane">
        <p class="pane-label">Now <b>${item.current.name}</b></p>
        <div class="big">${spriteHTML(item, 150)}</div>
        <div class="ladder">${ladderSizes
          .map((s) => `<div>${spriteHTML(item, s)}<span>${s}px</span></div>`)
          .join('')}</div>
      </section>
      <section class="pane pane-prop">
        <p class="pane-label">Proposed <b>${option.name}</b></p>
        <div class="big">${maskHTML(option, 150)}</div>
        <div class="ladder">${ladderSizes
          .map((s) => `<div>${maskHTML(option, s)}<span>${s}px</span></div>`)
          .join('')}</div>
      </section>
    </div>

    <div class="tray">
      <div class="tray-items">
        <button class="chip" type="button" data-pick="keep" aria-pressed="${choice === 'keep'}">
          ${spriteHTML(item, 18)}
          <span class="chip-name">Keep current</span>
        </button>
        ${item.options
          .map(
            (o, i) => `<button class="chip" type="button" data-pick="${o.name}" data-verdict="${o.verdict || ''}"
              aria-pressed="${index === i}">
              ${maskHTML(o, 18)}
              <span class="chip-name">${o.name}</span>
              ${o.verdict === 'best' ? '<span class="chip-tag">best</span>' : ''}
            </button>`,
          )
          .join('')}
      </div>
      <div class="tray-actions">
        <button class="btn ghost sm" type="button" id="prev" ${pos === 1 ? 'disabled' : ''}>←</button>
        <button class="btn primary" type="button" id="choose">Choose ${option.name}</button>
        <button class="btn ghost sm" type="button" id="next" ${pos === list.length ? 'disabled' : ''}>→</button>
      </div>
    </div>`;

  $$('.chip[data-pick]', $('#stage')).forEach((chip) => {
    const value = chip.dataset.pick;
    chip.addEventListener('click', () => {
      if (value === 'keep') {
        choose('keep');
      } else {
        const i = item.options.findIndex((o) => o.name === value);
        state.preview[item.id] = i;
        renderStage();
      }
    });
  });

  $('#choose').addEventListener('click', () => choose(option.name));
  $('#prev').addEventListener('click', () => step(-1));
  $('#next').addEventListener('click', () => step(1));
  renderProgress();
}

function choose(value) {
  const item = activeItem();
  if (!item) return;
  state.decisions[item.id] = value;
  save();
  renderRail();
  renderStage();
  const list = visibleItems();
  const pos = list.findIndex((i) => i.id === item.id);
  if (pos < list.length - 1) step(1);
}

function step(delta) {
  const list = visibleItems();
  const pos = list.findIndex((i) => i.id === state.activeId);
  const next = list[pos + delta];
  if (next) setActive(next.id);
}

/* ------------------------------------------------------------ sheet */

function renderSheet() {
  const list = items();
  const rows = list
    .map((item) => {
      const choice = decisionOf(item);
      const label = !choice ? 'not decided' : choice === 'keep' ? 'keep current' : choice;
      return `<div class="sheet-row">
        <div>
          <h3>${item.title}</h3>
          <p>${item.group.title} · ${item.ref || ''}</p>
        </div>
        <div class="cell">${spriteHTML(item, 22)}</div>
        <div class="cell">${chosenHTML(item, 22)}</div>
        <div class="picked"><b>${label}</b></div>
      </div>`;
    })
    .join('');

  $('#sheet-body').innerHTML = rows || '<p class="empty">Nothing to review yet.</p>';

  const done = list.filter((i) => decisionOf(i)).length;
  $('#sheet-hint').textContent = `${done} of ${list.length} decided · choices are saved in this browser`;

  $('#export-copy').onclick = () => {
    const text = JSON.stringify(exportData(), null, 2);
    navigator.clipboard.writeText(text).then(
      () => { $('#sheet-hint').textContent = 'JSON copied to the clipboard.'; },
      () => { $('#sheet-hint').textContent = 'Clipboard blocked — use Download JSON.'; },
    );
  };

  $('#export-file').onclick = () => {
    const blob = new Blob([JSON.stringify(exportData(), null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${state.collection.id}-decisions.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  $('#reset').onclick = () => {
    state.decisions = {};
    save();
    renderSheet();
    renderRail();
    renderStage();
  };
}

function exportData() {
  const choices = {};
  items().forEach((item) => {
    const choice = decisionOf(item);
    if (!choice) return;
    choices[item.id] = {
      choice,
      verdict: choice === 'keep' ? 'keep' : (optionOf(item, choice) || {}).verdict || null,
    };
  });
  return {
    collection: state.collection.id,
    source: state.data.source,
    decided: Object.keys(choices).length,
    total: items().length,
    choices,
  };
}

function openSheet() {
  renderSheet();
  $('#sheet').hidden = false;
  $('#sheet-close').focus();
}

function closeSheet() {
  $('#sheet').hidden = true;
}

/* ------------------------------------------------------------ theme */

function setTheme(theme, persist = true) {
  const value = theme === 'oled' ? 'oled' : 'light';
  document.documentElement.dataset.theme = value;
  $('#theme-label').textContent = value === 'oled' ? 'Light' : 'Dark';
  $('#theme-btn').setAttribute('aria-pressed', String(value === 'oled'));
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = value === 'oled' ? '#0b1015' : '#f7f3e8';
  if (persist) {
    try { localStorage.setItem(STORE + '-theme', value); } catch { /* ignore */ }
  }
}

/* ------------------------------------------------------------ keys */

document.addEventListener('keydown', (event) => {
  if (event.metaKey || event.ctrlKey || event.altKey) return;
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName);

  if (event.key === 'Escape') {
    if (!$('#sheet').hidden) closeSheet();
    return;
  }
  if (typing) return;

  if (event.key === 'ArrowRight') { step(1); event.preventDefault(); }
  else if (event.key === 'ArrowLeft') { step(-1); event.preventDefault(); }
  else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
    const item = activeItem();
    if (!item) return;
    const count = item.options.length;
    const index = state.preview[item.id] || 0;
    const next = (index + (event.key === 'ArrowDown' ? 1 : -1) + count) % count;
    state.preview[item.id] = next;
    renderStage();
    event.preventDefault();
  } else if (event.key === 'Enter') {
    const item = activeItem();
    if (item) choose(item.options[state.preview[item.id] || 0].name);
    event.preventDefault();
  } else if (event.key.toLowerCase() === 'k') {
    choose('keep');
  }
});

/* ------------------------------------------------------------ boot */

async function boot() {
  try {
    state.data = await (await fetch('data.json', { cache: 'no-cache' })).json();
  } catch (error) {
    $('#rail').innerHTML = '<p class="empty">Could not load data.json. Serve the folder over HTTP (for example <code>python3 -m http.server</code>) rather than opening the file directly.</p>';
    return;
  }

  state.collection = state.data.collections[0];
  load();
  setTheme(localStorage.getItem(STORE + '-theme') || 'light', false);

  $('#theme-btn').addEventListener('click', () =>
    setTheme(document.documentElement.dataset.theme === 'oled' ? 'light' : 'oled'),
  );
  $('#summary-btn').addEventListener('click', openSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  $('#sheet').addEventListener('click', (event) => {
    if (event.target.id === 'sheet') closeSheet();
  });

  if (location.hash === '#review') openSheet();

  renderGroups();
  const first = visibleItems()[0];
  state.activeId = first ? first.id : null;
  renderRail();
  renderStage();
  renderProgress();
}

boot();
