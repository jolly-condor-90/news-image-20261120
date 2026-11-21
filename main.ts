// make.fun news-image-20261120 — "The World Today", Friday 20 November 2026.
// The rendered front page is stored as entry.png. This program validates that
// asset and copies its exact bytes to the path the grader reads. It makes no
// network calls and produces identical bytes on every run.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outputDir, 'entry.png');

const image: Buffer = readFileSync(source);
const PNG_SIGNATURE = '89504e470d0a1a0a';

if (image.length < 24 || image.subarray(0, 8).toString('hex') !== PNG_SIGNATURE) {
  throw new Error(`${source} is not a whole PNG`);
}

const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width !== 1024 || height !== 1024 || image.length > 1048576) {
  throw new Error(`image ${width}x${height}, ${image.length} bytes, exceeds the gate`);
}

// A complete PNG ends with the IEND chunk and its CRC. Checking it here keeps a
// truncated or padded file from reaching the judge.
const IEND = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);
if (!image.subarray(-12).equals(IEND)) {
  throw new Error(`${source} has no IEND chunk`);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(target, image);
console.log(`wrote ${target} (${width}x${height}, ${image.length} bytes)`);
