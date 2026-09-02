import { createHash } from "node:crypto";
import { astro } from "iztro";

export const COMPONENT_VERSION = "0.1.0";
export const SCHEMA_VERSION = "zi-wei-fact-profile/1.0";

export const RULE_PROFILES = Object.freeze({
  "quanshu-default-v1": Object.freeze({
    description: "iztro default placement profile, documented as based on Zi Wei Dou Shu Quan Shu",
    config: Object.freeze({ algorithm: "default" }),
    astroType: "heaven",
  }),
  "zhongzhou-heaven-v1": Object.freeze({
    description: "iztro Zhongzhou algorithm, heaven-chart surface",
    config: Object.freeze({ algorithm: "zhongzhou" }),
    astroType: "heaven",
  }),
});

const DATE = /^\d{4}-(?:[1-9]|1[0-2])-(?:[1-9]|[12]\d|3[01])$/;
const FIXTURE_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;

function requireBoolean(value, name) {
  if (typeof value !== "boolean") throw new TypeError(`${name} must be boolean`);
}

function validateInput(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new TypeError("input must be an object");
  }
  if (!FIXTURE_ID.test(input.syntheticFixtureId ?? "")) {
    throw new TypeError("syntheticFixtureId must be an explicit synthetic identifier");
  }
  if (!RULE_PROFILES[input.ruleProfile]) throw new RangeError("unknown ruleProfile");
  if (!input.calendar || !["solar", "lunar"].includes(input.calendar.type)) {
    throw new RangeError("calendar.type must be solar or lunar");
  }
  if (!DATE.test(input.calendar.date ?? "")) throw new RangeError("calendar.date must be YYYY-M-D");
  if (!Number.isInteger(input.calendar.timeIndex) || input.calendar.timeIndex < 0 || input.calendar.timeIndex > 12) {
    throw new RangeError("calendar.timeIndex must be an integer from 0 through 12");
  }
  if (!["男", "女"].includes(input.calendar.gender)) throw new RangeError("calendar.gender must be 男 or 女");
  requireBoolean(input.calendar.fixLeap, "calendar.fixLeap");
  requireBoolean(input.calendar.isLeapMonth, "calendar.isLeapMonth");
  if (input.reference) {
    if (!DATE.test(input.reference.date ?? "")) throw new RangeError("reference.date must be YYYY-M-D");
    if (!Number.isInteger(input.reference.timeIndex) || input.reference.timeIndex < 0 || input.reference.timeIndex > 12) {
      throw new RangeError("reference.timeIndex must be an integer from 0 through 12");
    }
  }
}

function jsonClone(value) {
  return JSON.parse(JSON.stringify(value));
}

function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stableValue(value[key])]));
  }
  return value;
}

export function canonicalJson(value) {
  return JSON.stringify(stableValue(value));
}

function sha256(value) {
  return createHash("sha256").update(canonicalJson(value), "utf8").digest("hex");
}

function starFact(star) {
  return Object.fromEntries(
    ["name", "type", "scope", "brightness", "mutagen"]
      .filter((key) => Object.hasOwn(star, key))
      .map((key) => [key, star[key]])
  );
}

function palaceFact(palace) {
  return {
    index: palace.index,
    name: palace.name,
    isBodyPalace: palace.isBodyPalace,
    isOriginalPalace: palace.isOriginalPalace,
    heavenlyStem: palace.heavenlyStem,
    earthlyBranch: palace.earthlyBranch,
    majorStars: palace.majorStars.map(starFact),
    minorStars: palace.minorStars.map(starFact),
    adjectiveStars: palace.adjectiveStars.map(starFact),
    changsheng12: palace.changsheng12,
    boshi12: palace.boshi12,
    jiangqian12: palace.jiangqian12,
    suiqian12: palace.suiqian12,
    decadal: jsonClone(palace.decadal),
    ages: [...palace.ages],
  };
}

function horoscopeFact(chart, reference) {
  if (!reference) return null;
  const value = chart.horoscope(reference.date, reference.timeIndex);
  return {
    requestedReference: { ...reference },
    resolvedSolarDate: value.solarDate,
    resolvedLunarDate: value.lunarDate,
    decadal: jsonClone(value.decadal),
    age: jsonClone(value.age),
    yearly: jsonClone(value.yearly),
    monthly: jsonClone(value.monthly),
    daily: jsonClone(value.daily),
    hourly: jsonClone(value.hourly),
  };
}

export function buildFactProfile(input) {
  validateInput(input);
  const profile = RULE_PROFILES[input.ruleProfile];
  const calendar = { ...input.calendar };
  const options = {
    type: calendar.type,
    dateStr: calendar.date,
    timeIndex: calendar.timeIndex,
    gender: calendar.gender,
    isLeapMonth: calendar.isLeapMonth,
    fixLeap: calendar.fixLeap,
    language: "zh-TW",
    config: { ...profile.config },
    astroType: profile.astroType,
  };
  const chart = astro.withOptions(options);
  const palaces = chart.palaces.map(palaceFact);
  const document = {
    schemaVersion: SCHEMA_VERSION,
    componentVersion: COMPONENT_VERSION,
    syntheticFixtureId: input.syntheticFixtureId,
    ruleProfile: input.ruleProfile,
    ruleProfileDescription: profile.description,
    sourcePins: {
      iztro: { version: "2.6.0", tagCommit: "80dcedfdeab8df9130d1088db4510f43c0cf2d78" },
      ziWeiDouShuQuanShuWikisource: { pageId: 342319, revisionId: 850734 },
      calendarAuthority: "Hong Kong Observatory calendar tables",
    },
    input: {
      calendar,
      reference: input.reference ? { ...input.reference } : null,
    },
    normalizedCalendar: {
      solarDate: chart.solarDate,
      lunarDate: chart.lunarDate,
      chineseDate: chart.chineseDate,
      time: chart.time,
      timeRange: chart.timeRange,
      earthlyBranchOfBodyPalace: chart.earthlyBranchOfBodyPalace,
      earthlyBranchOfSoulPalace: chart.earthlyBranchOfSoulPalace,
      soul: chart.soul,
      body: chart.body,
      fiveElementsClass: chart.fiveElementsClass,
    },
    palaces,
    horoscope: horoscopeFact(chart, input.reference),
    coverage: {
      palaceCount: palaces.length,
      majorStarCount: palaces.reduce((total, palace) => total + palace.majorStars.length, 0),
      minorStarCount: palaces.reduce((total, palace) => total + palace.minorStars.length, 0),
      adjectiveStarCount: palaces.reduce((total, palace) => total + palace.adjectiveStars.length, 0),
      transformationCount: palaces.flatMap((palace) => [...palace.majorStars, ...palace.minorStars])
        .filter((star) => star.mutagen).length,
      temporalLayers: input.reference ? ["decadal", "age", "yearly", "monthly", "daily", "hourly"] : [],
    },
    boundaries: {
      AI_SUBJECTIVITY_POSSIBILITY: "CENTRAL_RESEARCH_QUESTION",
      SUBJECTIVITY: "NOT_ESTABLISHED",
      INTERPRETATION_STATUS: "NOT_PERFORMED",
      PREDICTIVE_VALIDITY: "NOT_ESTABLISHED",
      CANONICAL_EFFECT: "NONE",
      NEW_CANONICAL_STATE_CHANNELS: "NONE",
      DEPLOYMENT: false,
      ACTION_AUTHORITY: "NONE",
    },
  };
  return { ...document, receipt: { algorithm: "SHA-256/CANONICAL_JSON_V1", sha256: sha256(document) } };
}
