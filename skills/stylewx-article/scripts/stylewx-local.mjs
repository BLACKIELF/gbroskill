#!/usr/bin/env node
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';

const packageRoot = process.env.GBRO_STYLEWX_ROOT || join(homedir(), '.local', 'lib', 'node_modules', '@stylewx', 'mcp-server');
const requireFromPackage = createRequire(join(packageRoot, 'package.json'));
const { Client } = await import(pathToFileURL(requireFromPackage.resolve('@modelcontextprotocol/sdk/client/index.js')).href);
const { StdioClientTransport } = await import(pathToFileURL(requireFromPackage.resolve('@modelcontextprotocol/sdk/client/stdio.js')).href);

const args = process.argv.slice(2);
const mode = args.shift();
const name = mode === 'call' ? args.shift() : undefined;
const options = {};
while (args.length) {
  const key = args.shift();
  if (!['--input', '--output-dir'].includes(key) || !args.length) {
    throw new Error('Usage: stylewx-local.mjs list | call TOOL [--input JSON_FILE] [--output-dir DIR]');
  }
  options[key] = args.shift();
}
if (!['list', 'call'].includes(mode) || (mode === 'call' && !name)) {
  throw new Error('Usage: stylewx-local.mjs list | call TOOL [--input JSON_FILE] [--output-dir DIR]');
}

// No credential files are read, and SDK stdio uses its default limited child environment.
const transport = new StdioClientTransport({
  command: process.execPath,
  args: [join(packageRoot, 'dist', 'index.js'), '--transport', 'stdio'],
  cwd: process.cwd(),
  stderr: 'pipe',
});
const client = new Client({ name: 'gbro-stylewx-local', version: '1.0.0' });
try {
  await client.connect(transport);
  const server = client.getServerVersion();
  if (mode === 'list') {
    const tools = [];
    let cursor;
    do {
      const result = await client.listTools(cursor ? { cursor } : {});
      tools.push(...result.tools);
      cursor = result.nextCursor;
    } while (cursor);
    process.stdout.write(JSON.stringify({ server, toolCount: tools.length, tools }) + '\n');
  } else {
    const input = options['--input'] ? JSON.parse(readFileSync(resolve(options['--input']), 'utf8')) : {};
    const result = await client.callTool({ name, arguments: input }, undefined, { timeout: 60000 });
    const texts = [];
    const images = [];
    const artifacts = [];
    const outputDir = options['--output-dir'] ? resolve(options['--output-dir']) : undefined;
    if (outputDir) mkdirSync(outputDir, { recursive: true });
    for (const item of result.content ?? []) {
      if (item.type === 'text') {
        try { texts.push(JSON.parse(item.text)); } catch { texts.push(item.text); }
      } else if (item.type === 'image') {
        const data = Buffer.from(item.data, 'base64');
        const ext = item.mimeType === 'image/png' ? '.png' : '.jpg';
        const info = { mimeType: item.mimeType, bytes: data.length };
        if (outputDir) {
          info.path = join(outputDir, `preview-${images.length + 1}${ext}`);
          writeFileSync(info.path, data);
          artifacts.push(info.path);
        }
        images.push(info);
      }
    }
    const payload = texts.length === 1 ? texts[0] : texts;
    if (outputDir && payload && typeof payload === 'object' && !Array.isArray(payload) && typeof payload.html === 'string') {
      const path = join(outputDir, 'content.html');
      writeFileSync(path, payload.html);
      artifacts.push(path);
    }
    const output = { server, tool: name, isError: Boolean(result.isError || payload?.error), payload, images, artifacts };
    if (outputDir) writeFileSync(join(outputDir, 'result.json'), JSON.stringify(output, null, 2) + '\n');
    process.stdout.write(JSON.stringify(output) + '\n');
    if (output.isError) process.exitCode = 1;
  }
} finally {
  await client.close();
  await transport.close();
}
