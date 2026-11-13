#!/usr/bin/env node
/* Builds dist/manifest.json — what each icon is, what it is used for, and its palette. */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';

const data = JSON.parse(readFileSync('data.json', 'utf8'));

const usage = {};
for (const collection of data.collections) {
  for (const group of collection.groups) {
    for (const item of group.items) {
      for (const option of item.options) {
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
}

const icons = readdirSync('dist/icons')
  .filter((file) => file.endsWith('.svg'))
  .sort()
  .map((file) => {
    const body = readFileSync(`dist/icons/${file}`, 'utf8');
    const name = file.replace(/\.svg$/, '');
    return {
      name,
      file: `icons/${file}`,
      title: (body.match(/<title>(.*?)<\/title>/) || [, name])[1],
      palette: [...body.matchAll(/stop-color="(#[0-9a-fA-F]{6})"/g)].map((m) => m[1]),
      accent: (body.match(/<g stroke="(#[0-9a-fA-F]{6})" stroke-opacity="\.3"/) || [, null])[1],
      usedIn: usage[name] || [],
    };
  });

const manifest = {
  generated: new Date().toISOString(),
  repo: 'https://github.com/indpriyanshuraj-bot/Levi-icon',
  source: data.source,
  grid: 24,
  strokeWidth: 1.8,
  tokens: data.tokens,
  icons,
};

writeFileSync('dist/manifest.json', JSON.stringify(manifest, null, 2));
console.log(`manifest.json — ${icons.length} icons`);
