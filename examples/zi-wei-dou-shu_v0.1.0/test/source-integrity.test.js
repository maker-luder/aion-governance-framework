import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const manifest = JSON.parse(await readFile(new URL("sources/SOURCE_FETCH_MANIFEST.json", root), "utf8"));
const register = JSON.parse(await readFile(new URL("docs/SOURCE_REGISTER.json", root), "utf8"));

test("every retained source snapshot matches its fetch-manifest digest", async () => {
  assert.equal(manifest.source_count, 7);
  assert.equal(manifest.network_required_at_runtime, false);
  assert.ok(manifest.sources.every((source) => source.download_status === "PASS"));
  for (const source of manifest.sources.filter((item) => item.repository_path)) {
    const relative = source.repository_path.split("/sources/")[1];
    const payload = await readFile(new URL(`sources/${relative}`, root));
    const digest = createHash("sha256").update(payload).digest("hex");
    assert.equal(digest, source.repository_sha256, source.source_id);
  }
});

test("the source register and package lock pin the same modern algorithm release", async () => {
  const iztro = register.sources.find((source) => source.id === "IZTRO_2_6_0");
  assert.equal(iztro.version, "2.6.0");
  assert.equal(iztro.tag_commit, "80dcedfdeab8df9130d1088db4510f43c0cf2d78");
  assert.equal(iztro.npm_sha256, "df7013db5260d548ed1359f5173089eab6a925d90e15b327235b10a1e0b0abb9");
  const lock = await readFile(new URL("pnpm-lock.yaml", root), "utf8");
  assert.match(lock, /iztro@2\.6\.0:/);
  assert.match(lock, /sha512-0zN7j\+z2UX642yEbraFNILRU/);
});
