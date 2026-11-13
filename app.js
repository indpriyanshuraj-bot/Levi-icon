/* LeviMC icon review — data-driven comparison app.
   Everything comes from data.json. Add an icon and an entry, it appears. */

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const STORE = 'levi-icon-review-v1';
const BUILD = '5';

const state = {
  data: null,
  setId: null,
  decisions: {},
  activeId: null,
  preview: {},
  filter: 'all',
};

const CHECK = '<svg class="chip-check" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8.5 6.2 12 13 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

/* ------------------------------------------------------------ helpers */

const kebab = (name) => String(name).replace(/[A-Z]/g, (m) => '-' + m.toLowerCase());

const collection = () => (state.data ? state.data.collections.find((c) => c.id === state.setId) : null);

function items() {
  const set = collection();
  if (!set || !set.groups) return [];
  return set.groups.flatMap((group) => group.items.map((item) => Object.assign({}, item, { group })));
}

function activeItem() {
  return items().find((item) => item.id === state.activeId) || items()[0] || null;
}

function optionOf(item, name) {
  return (item.options || []).find((o) => o.name === name || o.label === name);
}

function decisionOf(item) {
  return state.decisions[item.id] || null;
}

function optionSrc(option) {
  if (option.src) return option.src;
  return `${collection().optionBase}/${option.name}.svg`;
}

/* current icon: hotlinked from the source repository, never copied */
function spriteHTML(item, size, cls = '') {
  const c = item.current;
  const base = collection().currentBase;
  const fallback = collection().currentFallback || base;
  if (!base) return '';
  const file = kebab(c.name);
  const mono = (c.palette || [])[0] === 'currentColor' ? ' mono' : '';
  return `<img class="sprite${mono} ${cls}" src="${base}/${file}.svg" data-fallback="${fallback}/${file}.svg"
    onerror="if(this.dataset.retried){this.style.visibility='hidden'}else{this.dataset.retried=1;this.src=this.dataset.fallback}"
    width="${size}" height="${size}" alt="" draggable="false">`;
}

function candHTML(option, size, cls = '') {
  return `<img class="cand ${cls}" src="${optionSrc(option)}" width="${size}" height="${size}" alt="" draggable="false">`;
}

function chosenHTML(item, size) {
  const choice = decisionOf(item);
  if (!choice) return '<span class="chip-tag">—</span>';
  if (choice === 'keep') return spriteHTML(item, size);
  const option = optionOf(item, choice);
  return option ? candHTML(option, size) : '<span class="chip-tag">—</span>';
}

/* the recommended option sits in the middle of the row */
function orderedOptions(item) {
  const best = item.options.filter((o) => o.verdict === 'best');
  const rest = item.options.filter((o) => o.verdict !== 'best');
  const out = [];
  const before = Math.ceil(rest.length / 2);
  rest.forEach((o, i) => {
    if (i === before) out.push(...best);
    out.push(o);
  });
  if (!best.length || out.length === rest.length) out.push(...best);
  return out;
}

/* the stage opens on the recommendation, not on whatever is first */
function previewIndex(item, ordered) {
  const stored = state.preview[item.id];
  if (stored !== undefined && ordered[stored]) return stored;
  const best = ordered.findIndex((o) => o.verdict === 'best');
  return best >= 0 ? best : 0;
}

/* ------------------------------------------------------------ persistence */

function load() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE) || '{}');
    state.decisions = raw[state.setId] || {};
  } catch { state.decisions = {}; }
}

function save() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE) || '{}');
    raw[state.setId] = state.decisions;
    localStorage.setItem(STORE, JSON.stringify(raw));
  } catch { /* private mode */ }
}

/* ------------------------------------------------------------ start screen */

function renderStart() {
  const sets = state.data.collections;
  $('#body').classList.add('is-start');
  $('#start').innerHTML = `
    <div class="start-head">
      <p class="eyebrow">LeviMC design review</p>
      <h1>What do you want to review?</h1>
      <p class="start-copy">Pick a set. Decisions are kept per set in this browser, and each set exports on its own.</p>
    </div>
    <div class="start-grid">
      ${sets.map((set) => {
        const count = (set.groups || []).reduce((n, g) => n + g.items.length, 0);
        const decided = count
          ? (() => {
              let stored = {};
              try { stored = (JSON.parse(localStorage.getItem(STORE) || '{}'))[set.id] || {}; } catch { /* ignore */ }
              return Object.keys(stored).length;
            })()
          : 0;
        return `<button class="set-card${count ? '' : ' is-empty'}" type="button" data-set="${set.id}" ${count ? '' : 'disabled'}>
          <span class="set-name">${set.title}</span>
          <span class="set-note">${set.note || ''}</span>
          <span class="set-meta">${count ? `${count} placements · ${decided} decided` : 'No placements yet'}</span>
          <span class="set-go">${count ? 'Open →' : 'Empty'}</span>
        </button>`;
      }).join('')}
    </div>`;

  $$('.set-card[data-set]', $('#start')).forEach((card) =>
    card.addEventListener('click', () => openSet(card.dataset.set)),
  );
}

function openSet(id, itemId) {
  state.setId = id;
  load();
  state.filter = 'all';
  state.activeId = itemId || null;
  $('#body').classList.remove('is-start');
  renderGroups();
  const list = visibleItems();
  const wanted = itemId ? list.find((i) => i.id === itemId) : null;
  state.activeId = wanted ? wanted.id : list[0] ? list[0].id : null;
  renderRail();
  renderStage();
  renderProgress();
  if (location.hash !== `#${id}`) history.replaceState(null, '', `#${id}`);
}

/* ------------------------------------------------------------ chrome */

function renderGroups() {
  const nav = $('#groups');
  const groups = collection().groups || [];
  if (!groups.length) { nav.innerHTML = ''; return; }
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
  const groups = (collection().groups || []).filter((g) => state.filter === 'all' || g.id === state.filter);
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
  $$('.row', rail).forEach((row) => row.addEventListener('click', () => setActive(row.dataset.id)));
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
  if (!item) {
    $('#stage').innerHTML = `<p class="empty">This set has no placements yet. Add items to <code>data.json</code> under
      <code>${state.setId}</code> and drop the SVGs in <code>${collection().optionBase}/</code>.</p>`;
    return;
  }
  const group = item.group;
  const ordered = orderedOptions(item);
  const current = ordered[previewIndex(item, ordered)] || ordered[0];
  const choice = decisionOf(item);
  const list = visibleItems();
  const pos = list.findIndex((i) => i.id === item.id) + 1;
  const ladder = [16, 24, 32, 64];

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
        <div class="ladder">${ladder.map((s) => `<div>${spriteHTML(item, s)}<span>${s}px</span></div>`).join('')}</div>
      </section>
      <section class="pane pane-prop">
        <p class="pane-label">Proposed <b>${current.name}</b></p>
        <div class="big">${candHTML(current, 150)}</div>
        <div class="ladder">${ladder.map((s) => `<div>${candHTML(current, s)}<span>${s}px</span></div>`).join('')}</div>
      </section>
    </div>

    <div class="tray">
      <button class="chip${choice === 'keep' ? ' is-chosen' : ''}" type="button" data-pick="keep" title="Leave this icon as it is">
        <span class="chip-ic">${spriteHTML(item, 22)}</span>
        <span class="chip-body"><span class="chip-name">Keep current</span><span class="chip-tag">${item.current.name}</span></span>
        ${choice === 'keep' ? CHECK : ''}
      </button>
      <div class="chip-group">
        ${ordered
          .map(
            (o) => `<button class="chip${choice === o.name ? ' is-chosen' : ''}" type="button" data-pick="${o.name}"
              data-verdict="${o.verdict || ''}" aria-pressed="${current.name === o.name}">
              <span class="chip-ic">${candHTML(o, 22)}</span>
              <span class="chip-body">
                <span class="chip-name">${o.name}</span>
                <span class="chip-tag">${o.verdict === 'best' ? 'recommended' : 'alternative'}</span>
              </span>
              ${choice === o.name ? CHECK : ''}
            </button>`,
          )
          .join('')}
      </div>
      <div class="tray-actions">
        <button class="btn ghost sm" type="button" id="prev" ${pos === 1 ? 'disabled' : ''}>←</button>
        <button class="btn primary" type="button" id="choose">${choice === current.name ? 'Chosen · ' + current.name : 'Choose ' + current.name}</button>
        <button class="btn ghost sm" type="button" id="next" ${pos === list.length ? 'disabled' : ''}>→</button>
      </div>
    </div>`;

  $$('.chip[data-pick]', $('#stage')).forEach((chip) => {
    const value = chip.dataset.pick;
    chip.addEventListener('click', () => {
      if (value === 'keep') choose('keep');
      else {
        state.preview[item.id] = ordered.findIndex((o) => o.name === value);
        renderStage();
      }
    });
  });

  $('#choose').addEventListener('click', () => choose(current.name));
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
  if (value !== 'keep' && pos < list.length - 1) step(1);
}

function step(delta) {
  const list = visibleItems();
  const pos = list.findIndex((i) => i.id === state.activeId);
  const next = list[pos + delta];
  if (next) setActive(next.id);
}

/* ------------------------------------------------------------ export */

function rows() {
  return items()
    .map((item) => {
      const choice = decisionOf(item);
      if (!choice) return null;
      const option = choice === 'keep' ? null : optionOf(item, choice);
      return {
        id: item.id,
        choice: option ? option.name : item.current.name,
        keep: !option,
        ref: item.ref || '',
        file: option ? `${collection().optionBase}/${option.name}.svg` : '',
      };
    })
    .filter(Boolean);
}

function exportAs(format) {
  const set = state.setId;
  const list = rows();

  if (format === 'json') {
    return JSON.stringify({ set, choices: list }, null, 2);
  }

  if (format === 'csv') {
    const head = 'placement,choice,applies_at,file';
    const body = list.map((r) => [r.id, r.choice, r.ref, r.file].map((v) => (/[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v)).join(','));
    return [head, ...body].join('\n');
  }

  if (format === 'md') {
    const head = ['| Placement | Choice | Applies at | File |', '| --- | --- | --- | --- |'];
    const body = list.map((r) => `| \`${r.id}\` | \`${r.choice}\`${r.keep ? ' (keep)' : ''} | \`${r.ref}\` | ${r.file ? `\`${r.file}\`` : '—'} |`);
    return [`# ${collection().title} — decisions`, '', ...head, ...body].join('\n');
  }

  return [
    `${collection().title} — ${list.length} decisions`,
    '',
    ...list.map((r) => `${r.id}: ${r.choice}${r.keep ? ' (keep current)' : ''}${r.ref ? `  →  ${r.ref}` : ''}`),
  ].join('\n');
}

function download(format) {
  const text = exportAs(format);
  const type = { json: 'application/json', csv: 'text/csv', md: 'text/markdown', txt: 'text/plain' }[format];
  const blob = new Blob([text], { type: `${type};charset=utf-8` });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `levimc-${state.setId}-choices-${new Date().toISOString().slice(0, 10)}.${format}`;
  a.click();
  URL.revokeObjectURL(url);
}

/* ------------------------------------------------------------ sheet */

function renderSheet() {
  const list = items();
  $('#sheet-body').innerHTML = list.length
    ? list
        .map((item) => {
          const choice = decisionOf(item);
          const label = !choice ? 'not decided' : choice === 'keep' ? 'keep current' : choice;
          return `<div class="sheet-row">
            <div><h3>${item.title}</h3><p>${item.group.title} · ${item.ref || ''}</p></div>
            <div class="cell">${spriteHTML(item, 22)}</div>
            <div class="cell">${chosenHTML(item, 22)}</div>
            <div class="picked"><b>${label}</b></div>
          </div>`;
        })
        .join('')
    : '<p class="empty">This set has no placements yet.</p>';

  const done = list.filter((i) => decisionOf(i)).length;
  $('#sheet-hint').textContent = `${done} of ${list.length} decided · ${collection().title}`;

  ['json', 'csv', 'md', 'txt'].forEach((format) => {
    const btn = $(`#export-${format}`);
    if (!btn) return;
    btn.onclick = () => download(format);
    btn.disabled = !done;
  });

  $('#reset').onclick = () => {
    state.decisions = {};
    save();
    renderSheet();
    renderRail();
    renderStage();
  };
}

function openSheet() {
  if (!state.setId) return;
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
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName)) return;

  if (event.key === 'Escape') {
    if (!$('#sheet').hidden) closeSheet();
    else if (state.setId) { state.setId = null; renderStart(); history.replaceState(null, '', location.pathname); }
    return;
  }
  if (!state.setId) return;

  if (event.key === 'ArrowRight') { step(1); event.preventDefault(); }
  else if (event.key === 'ArrowLeft') { step(-1); event.preventDefault(); }
  else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
    const item = activeItem();
    if (!item) return;
    const ordered = orderedOptions(item);
    const index = previewIndex(item, ordered);
    state.preview[item.id] = (index + (event.key === 'ArrowDown' ? 1 : -1) + ordered.length) % ordered.length;
    renderStage();
    event.preventDefault();
  } else if (event.key === 'Enter') {
    const item = activeItem();
    if (!item) return;
    const ordered = orderedOptions(item);
    choose((ordered[previewIndex(item, ordered)] || ordered[0]).name);
    event.preventDefault();
  } else if (event.key.toLowerCase() === 'k') {
    choose('keep');
  }
});

/* ------------------------------------------------------------ boot */

function fail(title, detail) {
  $('#body').classList.add('is-start');
  $('#start').innerHTML = `<div class="start-head"><p class="eyebrow">Error</p><h1>${title}</h1><p class="start-copy">${detail}</p></div>`;
  $('#progress-count').textContent = '—';
}

async function boot() {
  let payload;
  try {
    const response = await fetch(`data.json?v=${BUILD}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    payload = await response.json();
  } catch (error) {
    fail('Could not load data.json', `The browser could not read <code>data.json</code> (${error.message}). Reload the page.`);
    return;
  }
  if (Array.isArray(payload) || !payload.collections) {
    fail('Out-of-date data.json', 'This browser is holding an old copy of the data file. Hard-reload (Ctrl/Cmd + Shift + R).');
    return;
  }

  state.data = payload;
  setTheme(localStorage.getItem(STORE + '-theme') || 'light', false);

  $('#theme-btn').addEventListener('click', () =>
    setTheme(document.documentElement.dataset.theme === 'oled' ? 'light' : 'oled'),
  );
  $('#summary-btn').addEventListener('click', openSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  $('#sheet').addEventListener('click', (event) => { if (event.target.id === 'sheet') closeSheet(); });
  $('#brand').addEventListener('click', () => {
    state.setId = null;
    renderStart();
    history.replaceState(null, '', location.pathname);
  });

  const hash = decodeURIComponent(location.hash.slice(1));
  if (hash === 'review') {
    const first = state.data.collections.find((c) => (c.groups || []).length);
    if (first) openSet(first.id);
    openSheet();
    return;
  }
  const [setId, itemId] = hash.split('/');
  const known = state.data.collections.some((c) => c.id === setId);
  if (known) openSet(setId, itemId);
  else renderStart();
}

boot().catch((error) => fail('The review could not start', error.message));
