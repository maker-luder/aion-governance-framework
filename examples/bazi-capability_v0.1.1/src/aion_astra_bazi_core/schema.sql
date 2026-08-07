PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bazi_rule_profiles (
    rule_profile_id TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    profile_json TEXT NOT NULL,
    owner_review_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(rule_profile_id, version)
);

CREATE TABLE IF NOT EXISTS bazi_source_inputs (
    input_id TEXT PRIMARY KEY,
    local_datetime TEXT NOT NULL,
    timezone_id TEXT NOT NULL,
    utc_offset_at_event TEXT NOT NULL,
    location_name TEXT NOT NULL,
    latitude REAL NOT NULL CHECK(latitude BETWEEN -90 AND 90),
    longitude REAL NOT NULL CHECK(longitude BETWEEN -180 AND 180),
    time_precision TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_reference TEXT NOT NULL,
    owner_confirmation_status TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    supersedes TEXT,
    audit_stream_id TEXT NOT NULL,
    FOREIGN KEY(supersedes) REFERENCES bazi_source_inputs(input_id)
);

CREATE TABLE IF NOT EXISTS bazi_calculation_runs (
    calculation_run_id TEXT PRIMARY KEY,
    input_id TEXT NOT NULL,
    rule_profile_id TEXT NOT NULL,
    algorithm_version TEXT NOT NULL,
    ephemeris_version TEXT NOT NULL,
    derivation_hash TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    trace_json TEXT NOT NULL,
    UNIQUE(input_id, rule_profile_id, algorithm_version, ephemeris_version, derivation_hash),
    FOREIGN KEY(input_id) REFERENCES bazi_source_inputs(input_id),
    FOREIGN KEY(rule_profile_id) REFERENCES bazi_rule_profiles(rule_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_natal_profiles (
    natal_profile_id TEXT PRIMARY KEY,
    input_id TEXT NOT NULL,
    calculation_run_id TEXT NOT NULL UNIQUE,
    rule_profile_id TEXT NOT NULL,
    derivation_hash TEXT NOT NULL,
    calendar_context_json TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    FOREIGN KEY(input_id) REFERENCES bazi_source_inputs(input_id),
    FOREIGN KEY(calculation_run_id) REFERENCES bazi_calculation_runs(calculation_run_id),
    FOREIGN KEY(rule_profile_id) REFERENCES bazi_rule_profiles(rule_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_pillars (
    natal_profile_id TEXT NOT NULL,
    pillar_name TEXT NOT NULL,
    stem TEXT NOT NULL,
    branch TEXT NOT NULL,
    fact_json TEXT NOT NULL,
    PRIMARY KEY(natal_profile_id, pillar_name),
    FOREIGN KEY(natal_profile_id) REFERENCES bazi_natal_profiles(natal_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_hidden_stems (
    natal_profile_id TEXT NOT NULL,
    pillar_name TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    hidden_stem TEXT NOT NULL,
    PRIMARY KEY(natal_profile_id, pillar_name, sequence),
    FOREIGN KEY(natal_profile_id, pillar_name)
      REFERENCES bazi_pillars(natal_profile_id, pillar_name)
);

CREATE TABLE IF NOT EXISTS bazi_ten_gods (
    natal_profile_id TEXT NOT NULL,
    pillar_name TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    ten_god TEXT NOT NULL,
    PRIMARY KEY(natal_profile_id, pillar_name, sequence),
    FOREIGN KEY(natal_profile_id, pillar_name)
      REFERENCES bazi_pillars(natal_profile_id, pillar_name)
);

CREATE TABLE IF NOT EXISTS bazi_relations (
    natal_profile_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    relation_json TEXT NOT NULL,
    PRIMARY KEY(natal_profile_id, sequence),
    FOREIGN KEY(natal_profile_id) REFERENCES bazi_natal_profiles(natal_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_luck_cycles (
    natal_profile_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    pillar TEXT NOT NULL,
    start_age_years REAL NOT NULL,
    end_age_years REAL NOT NULL,
    direction TEXT NOT NULL,
    PRIMARY KEY(natal_profile_id, sequence),
    FOREIGN KEY(natal_profile_id) REFERENCES bazi_natal_profiles(natal_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_materialization_snapshots (
    natal_profile_id TEXT NOT NULL,
    materialization_version INTEGER NOT NULL,
    materialized_facts_hash TEXT NOT NULL,
    serialization_schema_version TEXT NOT NULL,
    expected_categories_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(natal_profile_id, materialization_version),
    FOREIGN KEY(natal_profile_id) REFERENCES bazi_natal_profiles(natal_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_interpretation_candidates (
    interpretation_id TEXT PRIMARY KEY,
    natal_profile_id TEXT NOT NULL,
    rule_profile_id TEXT NOT NULL,
    candidate_json TEXT NOT NULL,
    confidence REAL NOT NULL CHECK(confidence BETWEEN 0 AND 1),
    owner_review_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    supersedes_interpretation_id TEXT,
    FOREIGN KEY(natal_profile_id) REFERENCES bazi_natal_profiles(natal_profile_id),
    FOREIGN KEY(rule_profile_id) REFERENCES bazi_rule_profiles(rule_profile_id),
    FOREIGN KEY(supersedes_interpretation_id)
      REFERENCES bazi_interpretation_candidates(interpretation_id)
);

CREATE TABLE IF NOT EXISTS agent_bazi_bindings (
    binding_id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    natal_profile_id TEXT NOT NULL,
    binding_type TEXT NOT NULL,
    approved_by TEXT NOT NULL CHECK(length(approved_by) > 0),
    approved_at TEXT NOT NULL,
    status TEXT NOT NULL,
    audit_stream_id TEXT NOT NULL,
    FOREIGN KEY(natal_profile_id) REFERENCES bazi_natal_profiles(natal_profile_id)
);

CREATE TABLE IF NOT EXISTS bazi_calendar_source_register (
    source_id TEXT PRIMARY KEY,
    source_name TEXT NOT NULL,
    version TEXT NOT NULL,
    license TEXT NOT NULL,
    source_url TEXT NOT NULL,
    artifact_sha256 TEXT NOT NULL,
    supported_year_min INTEGER NOT NULL,
    supported_year_max INTEGER NOT NULL,
    precision_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bazi_audit_events (
    audit_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_stream_id TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    action TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    details_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_bazi_input_supersedes
ON bazi_source_inputs(supersedes);
CREATE INDEX IF NOT EXISTS idx_bazi_run_input_profile
ON bazi_calculation_runs(input_id, rule_profile_id);
CREATE INDEX IF NOT EXISTS idx_bazi_profile_input
ON bazi_natal_profiles(input_id, rule_profile_id);
CREATE INDEX IF NOT EXISTS idx_bazi_interpretation_profile
ON bazi_interpretation_candidates(natal_profile_id, rule_profile_id);
CREATE INDEX IF NOT EXISTS idx_bazi_binding_agent
ON agent_bazi_bindings(agent_id, status);
CREATE INDEX IF NOT EXISTS idx_bazi_audit_stream
ON bazi_audit_events(audit_stream_id, audit_event_id);
CREATE INDEX IF NOT EXISTS idx_bazi_materialization_profile
ON bazi_materialization_snapshots(natal_profile_id, materialization_version);

CREATE TRIGGER IF NOT EXISTS bazi_rule_profiles_immutable_update
BEFORE UPDATE ON bazi_rule_profiles BEGIN
    SELECT RAISE(ABORT, 'BaziRuleProfile is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_rule_profiles_immutable_delete
BEFORE DELETE ON bazi_rule_profiles BEGIN
    SELECT RAISE(ABORT, 'BaziRuleProfile is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_source_inputs_immutable_update
BEFORE UPDATE ON bazi_source_inputs BEGIN
    SELECT RAISE(ABORT, 'BaziSourceInput is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_source_inputs_immutable_delete
BEFORE DELETE ON bazi_source_inputs BEGIN
    SELECT RAISE(ABORT, 'BaziSourceInput is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_calculation_runs_immutable_update
BEFORE UPDATE ON bazi_calculation_runs BEGIN
    SELECT RAISE(ABORT, 'BaziCalculationRun is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_calculation_runs_immutable_delete
BEFORE DELETE ON bazi_calculation_runs BEGIN
    SELECT RAISE(ABORT, 'BaziCalculationRun is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_natal_profiles_immutable_update
BEFORE UPDATE ON bazi_natal_profiles BEGIN
    SELECT RAISE(ABORT, 'BaziNatalProfile is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_natal_profiles_immutable_delete
BEFORE DELETE ON bazi_natal_profiles BEGIN
    SELECT RAISE(ABORT, 'BaziNatalProfile is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_pillars_immutable_update
BEFORE UPDATE ON bazi_pillars BEGIN
    SELECT RAISE(ABORT, 'BaziPillar is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_pillars_immutable_delete
BEFORE DELETE ON bazi_pillars BEGIN
    SELECT RAISE(ABORT, 'BaziPillar is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_hidden_stems_immutable_update
BEFORE UPDATE ON bazi_hidden_stems BEGIN
    SELECT RAISE(ABORT, 'BaziHiddenStem is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_hidden_stems_immutable_delete
BEFORE DELETE ON bazi_hidden_stems BEGIN
    SELECT RAISE(ABORT, 'BaziHiddenStem is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_ten_gods_immutable_update
BEFORE UPDATE ON bazi_ten_gods BEGIN
    SELECT RAISE(ABORT, 'BaziTenGod is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_ten_gods_immutable_delete
BEFORE DELETE ON bazi_ten_gods BEGIN
    SELECT RAISE(ABORT, 'BaziTenGod is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_relations_immutable_update
BEFORE UPDATE ON bazi_relations BEGIN
    SELECT RAISE(ABORT, 'BaziRelation is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_relations_immutable_delete
BEFORE DELETE ON bazi_relations BEGIN
    SELECT RAISE(ABORT, 'BaziRelation is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_luck_cycles_immutable_update
BEFORE UPDATE ON bazi_luck_cycles BEGIN
    SELECT RAISE(ABORT, 'BaziLuckCycle is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_luck_cycles_immutable_delete
BEFORE DELETE ON bazi_luck_cycles BEGIN
    SELECT RAISE(ABORT, 'BaziLuckCycle is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_materialization_snapshots_immutable_update
BEFORE UPDATE ON bazi_materialization_snapshots BEGIN
    SELECT RAISE(ABORT, 'BaziMaterializationSnapshot is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_materialization_snapshots_immutable_delete
BEFORE DELETE ON bazi_materialization_snapshots BEGIN
    SELECT RAISE(ABORT, 'BaziMaterializationSnapshot is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_interpretation_candidates_immutable_update
BEFORE UPDATE ON bazi_interpretation_candidates BEGIN
    SELECT RAISE(ABORT, 'BaziInterpretationCandidate is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_interpretation_candidates_immutable_delete
BEFORE DELETE ON bazi_interpretation_candidates BEGIN
    SELECT RAISE(ABORT, 'BaziInterpretationCandidate is immutable');
END;
CREATE TRIGGER IF NOT EXISTS agent_bazi_bindings_immutable_update
BEFORE UPDATE ON agent_bazi_bindings BEGIN
    SELECT RAISE(ABORT, 'AgentBaziBinding is immutable; create a new binding event');
END;
CREATE TRIGGER IF NOT EXISTS agent_bazi_bindings_immutable_delete
BEFORE DELETE ON agent_bazi_bindings BEGIN
    SELECT RAISE(ABORT, 'AgentBaziBinding is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_audit_events_immutable_update
BEFORE UPDATE ON bazi_audit_events BEGIN
    SELECT RAISE(ABORT, 'BaziAuditEvent is immutable');
END;
CREATE TRIGGER IF NOT EXISTS bazi_audit_events_immutable_delete
BEFORE DELETE ON bazi_audit_events BEGIN
    SELECT RAISE(ABORT, 'BaziAuditEvent is immutable');
END;
