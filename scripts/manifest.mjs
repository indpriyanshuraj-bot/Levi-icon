#!/usr/bin/env node
/* Builds dist/manifest.json — every set, every icon, its palette and where it is used. */
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';

const data = JSON.parse(readFileSync('data.json', 'utf8'));
const sets = [];

for (const collection of data.collections) {
  const usage = {};
  const groups = collection.groups || [];

  for (const group of groups) {
    for (const item of group.items || []) {
      for (const option of item.options || []) {
        (usage[option.name] ||= []).push({
          placement: item.id,
          title: item.title,
          page: group.title,
          ref: item.ref,
          size: item.size,
          verdict: option.verdict || null,
        });
      }
    }
  }

  const dir = `dist/set/${collection.id}`;
  const icons = existsSync(dir)
    ? readdirSync(dir)
        .filter((file) => file.endsWith('.svg'))
        .sort()
        .map((file) => {
          const body = readFileSync(`${dir}/${file}`, 'utf8');
          const name = file.replace(/\.svg$/, '');
          return {
            name,
            path: `${collection.optionBase}/${file}`,
            title: (body.match(/<title>(.*?)<\/title>/) || [, name])[1],
            palette: [...body.matchAll(/stop-color="(#[0-9a-fA-F]{6})"/g)].map((m) => m[1]),
            accent: ([...body.matchAll(/stroke="(#[0-9a-fA-F]{6})"/g)][0] || [])[1] || null,
            usedIn: usage[name] || [],
          };
        })
    : [];

  sets.push({
    id: collection.id,
    title: collection.title,
    folder: collection.optionBase,
    placements: groups.reduce((n, g) => n + (g.items || []).length, 0),
    icons,
  });
}

const seen = new Map();
for (const set of sets) {
  for (const icon of set.icons) {
    if (seen.has(icon.name)) {
      console.error(`error: icon name "${icon.name}" appears in both ${seen.get(icon.name)} and ${set.id}`);
      process.exit(1);
    }
    seen.set(icon.name, set.id);
  }
}

writeFileSync(
  'dist/manifest.json',
  JSON.stringify(
    {
      generated: new Date().toISOString(),
      repo: 'https://github.com/indpriyanshuraj-bot/Levi-icon',
      source: data.source,
      grid: 24,
      strokeWidth: 1.8,
      tokens: data.tokens,
      sets,
    },
    null,
    2,
  ),
);
console.log(`manifest.json — ${sets.length} sets, ${sets.reduce((n, s) => n + s.icons.length, 0)} icons`);
