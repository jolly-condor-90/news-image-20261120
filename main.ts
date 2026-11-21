import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

// Deterministic copier: the committed image is the entry. The grader mounts the
// repository read-only at /bot and gives us a writable /output.
const repo = process.env.MAKEFUN_BOT_DIR ?? (process.env.MAKEFUN_OUTPUT_DIR ? process.cwd() : "/bot");
const dest = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(dest, { recursive: true });

const png = readFileSync(join(repo, "entry.png"));
if (png.subarray(1, 4).toString() !== "PNG") {
  throw new Error("entry.png must be a PNG");
}
if (png.length > 1048576) {
  throw new Error("entry.png exceeds 1 MiB");
}
writeFileSync(join(dest, "entry.png"), png);
console.log("wrote entry.png", png.length, "bytes");
