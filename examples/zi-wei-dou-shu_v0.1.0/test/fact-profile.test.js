import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { buildFactProfile, canonicalJson, RULE_PROFILES } from "../src/index.js";

const fixture = JSON.parse(await readFile(new URL("../fixtures/synthetic-lunar.json", import.meta.url), "utf8"));

test("builds a complete deterministic natal fact surface", () => {
  const first = buildFactProfile(fixture);
  const second = buildFactProfile(JSON.parse(JSON.stringify(fixture)));
  assert.deepEqual(second, first);
  assert.equal(first.coverage.palaceCount, 12);
  assert.equal(first.coverage.majorStarCount, 14);
  assert.equal(first.coverage.transformationCount, 4);
  assert.deepEqual(first.coverage.temporalLayers, ["decadal", "age", "yearly", "monthly", "daily", "hourly"]);
  assert.equal(first.normalizedCalendar.solarDate, "2000-8-16");
  assert.equal(first.horoscope.resolvedSolarDate, "2026-9-2");
  assert.equal(first.receipt.sha256, "f01bd61eb313cd99ec86dc79aca437291801cf060e77e8050ed6bc4fd5f5cabf");
});

test("contains the 12 named palaces and all 14 primary stars once", () => {
  const result = buildFactProfile(fixture);
  const palaceNames = result.palaces.map((palace) => palace.name);
  const majorStars = result.palaces.flatMap((palace) => palace.majorStars.map((star) => star.name));
  assert.equal(new Set(palaceNames).size, 12);
  assert.deepEqual([...majorStars].sort(), ["七殺", "天同", "天府", "天梁", "天機", "天相", "太陽", "太陰", "廉貞", "巨門", "武曲", "破軍", "紫微", "貪狼"].sort());
});

test("makes school and leap-month choices explicit", () => {
  assert.deepEqual(Object.keys(RULE_PROFILES).sort(), ["quanshu-default-v1", "zhongzhou-heaven-v1"]);
  const zhongzhou = buildFactProfile({ ...fixture, ruleProfile: "zhongzhou-heaven-v1" });
  assert.equal(zhongzhou.ruleProfile, "zhongzhou-heaven-v1");
  assert.equal(zhongzhou.input.calendar.fixLeap, true);
  assert.equal(zhongzhou.input.calendar.isLeapMonth, false);
});

test("requires a synthetic fixture identifier and explicit bounded inputs", () => {
  assert.throws(() => buildFactProfile({ ...fixture, syntheticFixtureId: "" }), /syntheticFixtureId/);
  assert.throws(() => buildFactProfile({ ...fixture, calendar: { ...fixture.calendar, timeIndex: 13 } }), /timeIndex/);
  assert.throws(() => buildFactProfile({ ...fixture, ruleProfile: "unspecified" }), /ruleProfile/);
});

test("does not expose free-form prediction or subjectivity promotion", () => {
  const result = buildFactProfile(fixture);
  const text = canonicalJson(result);
  assert.equal(Object.hasOwn(result, "interpretation"), false);
  assert.equal(result.boundaries.INTERPRETATION_STATUS, "NOT_PERFORMED");
  assert.equal(result.boundaries.PREDICTIVE_VALIDITY, "NOT_ESTABLISHED");
  assert.equal(result.boundaries.SUBJECTIVITY, "NOT_ESTABLISHED");
  assert.equal(result.boundaries.NEW_CANONICAL_STATE_CHANNELS, "NONE");
  assert.equal(text.includes("freeTextPrediction"), false);
});

test("omits time-varying layers unless an explicit reference is supplied", () => {
  const { reference, ...withoutReference } = fixture;
  const result = buildFactProfile(withoutReference);
  assert.equal(result.horoscope, null);
  assert.deepEqual(result.coverage.temporalLayers, []);
});
