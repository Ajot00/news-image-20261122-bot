import { copyFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
await mkdir(destination, { recursive: true });
await copyFile(resolve(scriptDir, 'entry.png'), resolve(destination, 'entry.png'));
