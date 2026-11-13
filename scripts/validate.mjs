#!/usr/bin/env node
/* Checks data.json against the files in the repo. Runs on every push.
   Exits non-zero so a broken reference never reaches Pages. */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const errors = [];
const warnings = [];

let data;
try {
  data = JSON.parse(readFileSync(join(root, 'data.json'), 'utf8'));
} catch (error) {
  console.error('data.json is not valid JSON:', error.message);
  process.exit(1);
}

if (!Array.isArray(data.collections) || !data.collections.length) {
  errors.push('data.json has no collections');
}

const seen = new Set();

for (const collection of data.collections || []) {
  const optionBase = collection.optionBase || 'assets';
  const filled = (collection.groups || []).some((g) => (g.items || []).length);
  if (filled && !collection.currentBase) errors.push(`${collection.id}: currentBase is required once it has items`);
  if (!filled) continue;

  for (const group of collection.groups || []) {
    if (!group.items || !group.items.length) warnings.push(`${collection.id}/${group.id}: group has no items`);
    for (const item of group.items || []) {
      const where = `${collection.id}/${group.id}/${item.id}`;
      if (seen.has(item.id)) errors.push(`${where}: duplicate item id`);
      seen.add(item.id);
      if (!item.current || !item.current.name) errors.push(`${where}: current.name is required`);
      if (!item.options || !item.options.length) errors.push(`${where}: needs at least one option`);
      if (!item.ref) warnings.push(`${where}: no source reference`);

      for (const option of item.options || []) {
        if (!option.src && !option.name) errors.push(`${where}: option needs a name or src`);
        if (option.src) continue;
        const file = join(root, optionBase, option.name + '.svg');
        if (!existsSync(file)) errors.push(`${where}: missing icon file ${optionBase}/${option.name}.svg`);
        if (!option.color && !(data.tokens || {})[option.token]) {
          errors.push(`${where}/${option.name}: unknown token "${option.token}"`);
        }
      }
    }
  }
}

/* every candidate carries its own two-tone artwork */
const bases = [...new Set((data.collections || []).map((c) => c.optionBase || 'assets'))];
for (const base of bases) {
  const iconDir = join(root, base);
  if (!existsSync(iconDir)) continue;
  for (const file of readdirSync(iconDir).filter((f) => f.endsWith('.svg'))) {
    const body = readFileSync(join(iconDir, file), 'utf8');
    if (!/<linearGradient/.test(body)) {
      errors.push(`${base}/${file}: needs a <linearGradient> for its two-tone stroke`);
    }
    if (/stroke="currentColor"/.test(body)) {
      errors.push(`${base}/${file}: still colourless; the set ships its own palette`);
    }
    if (!/<title>/.test(body)) {
      warnings.push(`${base}/${file}: no <title>`);
    }
    if (!/viewBox="0 0 24 24"/.test(body)) {
      warnings.push(`${base}/${file}: not on the 24x24 grid`);
    }
  }
}

for (const line of warnings) console.warn('warning:', line);

if (errors.length) {
  for (const line of errors) console.error('error:', line);
  process.exit(1);
}

console.log('data.json ok - ' + seen.size + ' placements, ' + (data.collections || []).length + ' collection(s)');
