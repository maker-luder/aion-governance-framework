import { readFile } from "node:fs/promises";
import { buildFactProfile } from "./index.js";

const path = process.argv[2];
if (!path) throw new Error("usage: node src/cli.js INPUT.json");
const input = JSON.parse(await readFile(path, "utf8"));
process.stdout.write(`${JSON.stringify(buildFactProfile(input), null, 2)}\n`);
