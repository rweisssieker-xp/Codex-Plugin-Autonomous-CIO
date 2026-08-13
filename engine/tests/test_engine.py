import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from decision_intelligence_engine import (  # noqa: E402
    analyze_risk_graph,
    action_governance,
    adapt_connector_export,
    build_autopilot_review,
    build_autopilot_review_from_file,
    build_decision_assurance,
    build_audit_trail,
    build_decision_packet,
    build_decision_packet_from_file,
    build_executive_decision_defense,
    build_llm_extraction_contract,
    benchmark_decision_quality,
    connector_profile_catalog,
    detect_connector_profile,
    compare_packet_trend,
    compare_with_memory,
    export_decision_package,
    export_office_package,
    export_review_artifact,
    evaluate_golden_examples,
    extract_evidence_graph,
    extract_semantic_model,
    generate_dashboard_data,
    generate_dashboard_data_from_file,
    generate_operating_rhythm,
    ingest_connector_signals,
    ingest_source_directory,
    inspect_memory_store,
    import_context_file,
    load_memory_store,
    map_risk_chain,
    refresh_dashboard_data,
    propose_memory_updates,
    run_skill_orchestrator,
    score_decision_readiness,
    save_packet_to_memory,
    scan_privacy,
    simulate_scenarios,
)
from action_drafting import draft_actions  # noqa: E402
from decision_behavior import build_board_memory, build_decision_dna, build_risk_appetite_twin  # noqa: E402
from decision_twin import run_decision_twin  # noqa: E402
from enterprise_operating_intelligence import build_accountability_graph, build_executive_weekly_brief, build_weekly_operating_autopilot, detect_decision_collisions, detect_strategic_contradictions, score_organizational_friction  # noqa: E402
from eval_runner import run_evals  # noqa: E402
from evidence_quality import score_evidence_quality  # noqa: E402
from executive_autonomy_innovation import allocate_executive_attention, backtest_vendor_promises, build_autonomy_contract_engine, build_benefit_realization_memory, build_control_debt_ledger, build_decision_chain_of_custody, build_enterprise_contradiction_memory, build_enterprise_operating_twin, build_kill_criteria_sentinel, build_operating_rhythm_autopilot_v2, detect_strategic_drift_early_warning, forecast_evidence_decay, map_cio_replacement_surface, measure_decision_latency_cost, simulate_synthetic_executive_committee  # noqa: E402
from governed_execution_intelligence import build_delegation_planner, build_enterprise_decision_ledger, detect_narrative_integrity, run_decision_simulation_arena, score_vendor_truth, shadow_cost_of_inaction, trace_control_to_decision  # noqa: E402
from learning_loop import board_question_memory, calibrate_scores, learn_patterns, learning_digest, recommendation_backtest, record_feedback, record_outcome, record_skill_chain_feedback, source_reputation  # noqa: E402
from memory_store import init_memory_db, memory_aging, query_memory_db, save_review_to_db, sla_monitor  # noqa: E402
from office_export import build_board_pack  # noqa: E402
from policy_engine import approval_gates, evaluate_policy, governance_readiness  # noqa: E402
from product_hardening import build_llm_extraction_pipeline, build_release_package, list_memory_update_queue, queue_memory_updates, review_memory_update, run_hardening_evals, skill_suite_map, validate_output_schema  # noqa: E402
from source_connectors import discover_sources, ingest_source_bundle  # noqa: E402
from user_profile import apply_profile, init_profile  # noqa: E402


EXAMPLES = [
    "board_prep.json",
    "crisis.json",
    "ai_governance.json",
    "transformation_value.json",
]


class DecisionIntelligenceEngineTests(unittest.TestCase):
    def load_example(self, name):
        with (ENGINE / "examples" / name).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def assert_invariants(self, output):
        for key in ("facts", "assumptions", "hypotheses", "missing_evidence", "confidence", "recommended_action", "guardrails"):
            self.assertIn(key, output)
        guardrails = " ".join(output["guardrails"]).lower()
        self.assertIn("does not claim live system access", guardrails)
        self.assertIn("does not persist memory automatically", guardrails)
        self.assertIn("does not execute external actions", guardrails)

    def test_decision_packet_for_all_examples(self):
        for example in EXAMPLES:
            with self.subTest(example=example):
                output = build_decision_packet(self.load_example(example))
                self.assertEqual(output["artifact"], "Executive Decision Packet")
                self.assert_invariants(output)
                self.assertIn("semantic_model", output)
                self.assertIn("graph_metrics", output)
                self.assertIn("scenario_simulation", output)
                self.assertIn("board_personas", output)
                self.assertIn("audit_trail", output)
                for score in output["scorecard"].values():
                    self.assertGreaterEqual(score["value"], 0)
                    self.assertLessEqual(score["value"], 100)
                    self.assertTrue(score["reasons"])

    def test_specific_outputs(self):
        board = build_decision_packet(self.load_example("board_prep.json"))
        self.assertIn("Board", board["request_type"])
        self.assertTrue(board["risk_chain"])

        crisis = map_risk_chain(self.load_example("crisis.json"))
        self.assertTrue(crisis["risk_chain"])
        self.assert_invariants(crisis)

        ai = extract_evidence_graph(self.load_example("ai_governance.json"))
        self.assertTrue(ai["evidence_graph"]["nodes"])
        self.assert_invariants(ai)

        score = score_decision_readiness(self.load_example("transformation_value.json"))
        self.assertIn("value_leakage", score["scorecard"])
        self.assert_invariants(score)

    def test_innovation_outputs(self):
        context = self.load_example("board_prep.json")

        semantic = extract_semantic_model(context)
        self.assertTrue(semantic["semantic_model"]["entities"])
        self.assertTrue(semantic["semantic_model"]["claims"])
        self.assert_invariants(semantic)

        scenarios = simulate_scenarios(context)
        self.assertEqual(len(scenarios["scenario_simulation"]), 3)
        self.assert_invariants(scenarios)

        audit = build_audit_trail(context)
        self.assertIn("score_drivers", audit["audit_trail"])
        self.assert_invariants(audit)

        dashboard = generate_dashboard_data(context)
        self.assertIn("scores", dashboard)
        self.assertIn("graph_metrics", dashboard)
        self.assertIn("scenario_simulation", dashboard)
        self.assertIn("audit_trail", dashboard)
        self.assert_invariants(dashboard)

    def test_operating_rhythm_benchmark_and_signal_ingestion(self):
        context = self.load_example("board_prep.json")
        rhythm = generate_operating_rhythm(context)
        self.assertIn("operating_rhythm", rhythm)
        self.assertIn("weekly_decision_debt_review", rhythm["operating_rhythm"])
        self.assert_invariants(rhythm)

        benchmark = benchmark_decision_quality(context)
        self.assertIn("decision_quality_benchmark", benchmark)
        self.assertIn("before_after", benchmark["decision_quality_benchmark"])
        self.assert_invariants(benchmark)

        signals = self.load_example("connector_signals.json")
        ingestion = ingest_connector_signals(signals)
        self.assertTrue(ingestion["normalized_signals"])
        self.assertIn("source_summary", ingestion)
        self.assertIn("decision_packet", ingestion)
        self.assert_invariants(ingestion)

    def test_risk_graph_trend_and_export(self):
        context = self.load_example("board_prep.json")
        graph = analyze_risk_graph(context)
        self.assertIn("risk_graph", graph)
        self.assertTrue(graph["risk_graph"]["centrality"])
        self.assertTrue(graph["risk_graph"]["propagation_paths"])
        self.assert_invariants(graph)

        context["prior_packet"] = {
            "decision_needed": "Proceed with ERP go-live",
            "scorecard": {
                "decision_readiness": {"value": 70},
                "board_risk": {"value": 50},
                "evidence_confidence": {"value": 80},
                "value_leakage": {"value": 30},
                "autonomy_readiness": {"value": 60}
            },
            "weak_signals": ["Old vendor concern"]
        }
        trend = compare_packet_trend(context)
        self.assertTrue(trend["trend_delta"]["available"])
        self.assertIn("score_delta", trend["trend_delta"])
        self.assert_invariants(trend)

        export = export_review_artifact(context)
        self.assertEqual(export["format"], "markdown")
        self.assertIn("# Executive Decision Packet", export["content"])
        self.assert_invariants(export)

    def test_memory_comparison(self):
        context = self.load_example("transformation_value.json")
        memory = self.load_example("memory.json")
        output = compare_with_memory(context, memory)
        self.assertIn("overdue_actions", output)
        self.assert_invariants(output)

    def test_privacy_governance_import_memory_and_evaluation(self):
        context = self.load_example("ai_governance.json")
        context["context"].append("Contact owner jane.doe@example.com and token: sk-test-1234567890abcdef")
        privacy = scan_privacy(context)
        self.assertTrue(privacy["findings"])
        self.assertIn("[REDACTED_EMAIL]", " ".join(privacy["redacted_context"]))
        self.assert_invariants(privacy)

        governance = action_governance(context)
        self.assertTrue(governance["action_governance"])
        self.assertIn("automation_allowed", governance["action_governance"][0])
        self.assert_invariants(governance)

        imported = import_context_file(str(ENGINE / "examples" / "board_prep.json"))
        self.assertIn("input_context", imported)

        packet_from_file = build_decision_packet_from_file(str(ENGINE / "examples" / "sample_import.csv"))
        self.assertEqual(packet_from_file["artifact"], "Executive Decision Packet")
        self.assertIn("source_file", packet_from_file)
        self.assert_invariants(packet_from_file)

        dashboard_from_file = generate_dashboard_data_from_file(str(ENGINE / "examples" / "sample_import.csv"))
        self.assertEqual(dashboard_from_file["artifact"], "Visual Command Center Data")
        self.assertIn("source_file", dashboard_from_file)
        self.assert_invariants(dashboard_from_file)

        directory_ingestion = ingest_source_directory(str(ENGINE / "examples"))
        self.assertGreaterEqual(directory_ingestion["files_ingested"], 4)
        self.assertIn("decision_packet", directory_ingestion)
        self.assert_invariants(directory_ingestion)

        with tempfile.TemporaryDirectory() as tmp:
            memory_path = Path(tmp) / "memory.json"
            saved = save_packet_to_memory(self.load_example("board_prep.json"), str(memory_path))
            self.assertTrue(memory_path.exists())
            self.assertIn("packet_id", saved)
            store = load_memory_store(str(memory_path))
            self.assertTrue(store["decision_packets"])
            self.assert_invariants(saved)

            dashboard_path = Path(tmp) / "dashboard.json"
            refreshed = refresh_dashboard_data(str(ENGINE / "examples" / "board_prep.json"), str(dashboard_path))
            self.assertTrue(dashboard_path.exists())
            self.assertEqual(refreshed["artifact"], "Dashboard Data Refresh")
            self.assert_invariants(refreshed)

        evaluation = evaluate_golden_examples(str(ENGINE / "examples"))
        self.assertTrue(evaluation["passed"])
        self.assertEqual(len(evaluation["results"]), 4)
        self.assert_invariants(evaluation)

    def test_executive_decision_assurance(self):
        assurance = build_decision_assurance(self.load_example("board_prep.json"))
        expected = [
            "llm_extraction_layer",
            "entity_resolution",
            "causal_decision_graph",
            "counterfactual_simulation",
            "decision_twin",
            "board_question_coverage",
            "narrative_risk_detector",
            "decision_anti_patterns",
            "red_team_blue_team",
            "executive_attention_budget",
            "decision_latency_tracker",
            "value_at_risk_estimate",
            "governance_control_map",
            "meeting_to_decision_diff",
            "decision_packet_quality_grade",
        ]
        for key in expected:
            self.assertIn(key, assurance)
        self.assert_invariants(assurance)

        llm_assurance = build_decision_assurance(self.load_example("board_prep_llm_extracted.json"))
        self.assertEqual(llm_assurance["llm_extraction_layer"]["mode"], "provided_llm_output")
        self.assertTrue(llm_assurance["llm_extraction_layer"]["used"])
        self.assertIn("contradictions", llm_assurance["llm_extraction_layer"]["extraction"])
        self.assert_invariants(llm_assurance)

    def test_executive_decision_defense(self):
        defense = build_executive_decision_defense(self.load_example("board_prep.json"), self.load_example("memory.json"))
        expected = [
            "decision_liability_shield",
            "executive_blind_spot_radar",
            "commitment_integrity_score",
            "board_narrative_stress_test",
            "autonomous_decision_memory_diff",
            "value_realization_firewall",
            "risk_to_cash_translator",
            "decision_sla_monitor",
            "control_evidence_readiness",
            "executive_attention_allocator",
            "scenario_kill_switch",
            "cio_operating_system_loop",
        ]
        for key in expected:
            self.assertIn(key, defense)
        self.assertIn(defense["defense_posture"], {"Board-ready", "Defensible with gates", "Exposed"})
        self.assertGreaterEqual(defense["defense_score"], 0)
        self.assertLessEqual(defense["defense_score"], 100)
        self.assert_invariants(defense)

    def test_autopilot_review(self):
        review = build_autopilot_review(self.load_example("autopilot_review.json"), self.load_example("memory.json"))
        self.assertEqual(review["artifact"], "Autonomous CIO Autopilot Review")
        self.assertIn("decision_packet", review)
        self.assertIn("attention_budget", review)
        self.assertIn("action_ledger", review)
        self.assertIn("autonomy_gate", review)
        self.assertIn("cio_replacement_surface", review)
        self.assertIn("cio_work_autonomy_map", review)
        self.assertIn("board_objection_simulator", review)
        self.assertIn("decision_debt_ledger", review)
        self.assertIn("truth_gap_detector", review)
        self.assertIn("executive_time_saved_estimate", review)
        self.assertIn("cio_shadow_agenda", review)
        self.assertIn("autonomous_steering_pack_factory", review)
        self.assertIn("risk_chain_forecast", review)
        self.assertIn("strategic_drift_detector", review)
        self.assertIn("human_control_contract", review)
        self.assertIn("decision_sla_enforcer", review)
        self.assertIn("vendor_exit_simulator", review)
        self.assertIn("regulatory_shock_simulator", review)
        self.assertIn("cyber_business_impact_translator", review)
        self.assertIn("talent_criticality_radar", review)
        self.assertIn("capital_allocation_copilot", review)
        self.assertIn("post_decision_learning_loop", review)
        self.assertIn("cio_os_maturity_index", review)
        self.assertIn("stakeholder_alignment_matrix", review)
        self.assertIn("exception_waiver_factory", review)
        self.assertIn("policy_as_code_readiness", review)
        self.assertIn("benefits_realization_sentinel", review)
        self.assertIn("operating_rhythm_autopilot", review)
        self.assertIn("autonomous_escalation_drafts", review)
        self.assertIn("executive_decision_backlog", review)
        self.assertIn("enterprise_control_tower", review)
        self.assertIn("ma_carveout_readiness", review)
        self.assertIn("data_trust_radar", review)
        self.assertIn("architecture_runway_guardian", review)
        self.assertIn("executive_narrative_generator", review)
        self.assertIn("autonomous_due_diligence_questions", review)
        self.assertIn("resilience_continuity_planner", review)
        self.assertIn("customer_trust_impact_radar", review)
        self.assertIn("ai_portfolio_governance", review)
        self.assertIn("cost_of_delay_calculator", review)
        self.assertIn("executive_commitment_tracker", review)
        self.assertIn("decision_rights_mapper", review)
        self.assertIn("okr_strategy_fit_checker", review)
        self.assertIn("risk_acceptance_docket", review)
        self.assertIn("service_health_sentinel", review)
        self.assertIn("knowledge_continuity_planner", review)
        self.assertIn("dependency_breakpoint_analyzer", review)
        self.assertIn("transformation_kill_criteria", review)
        self.assertIn("vendor_negotiation_brief", review)
        self.assertIn("compliance_evidence_pack", review)
        self.assertIn("board_decision_simulator", review)
        self.assertIn("operating_risk_heatmap", review)
        self.assertIn("autonomous_roadmap_reprioritizer", review)
        self.assertIn("audit_finding_predictor", review)
        self.assertIn("platform_rationalization_advisor", review)
        self.assertIn("data_sovereignty_radar", review)
        self.assertIn("operating_model_debt_ledger", review)
        self.assertIn("strategic_option_portfolio", review)
        self.assertIn("executive_decision_war_room", review)
        self.assertIn("evidence_chain_of_custody", review)
        self.assertIn("decision_rollback_planner", review)
        self.assertIn("autonomy_risk_budget", review)
        self.assertIn("approval_boundary_mapper", review)
        self.assertIn("evidence_expiry_monitor", review)
        self.assertIn("residual_risk_contract", review)
        self.assertIn("autonomy_stress_test", review)
        self.assertIn("decision_consequence_ledger", review)
        self.assertIn("enterprise_friction_map", review)
        self.assertIn("strategic_optionality_engine", review)
        self.assertIn("control_debt_burndown", review)
        self.assertIn("executive_dissent_synthesizer", review)
        self.assertIn("decision_backtest_simulator", review)
        self.assertIn("governance_drift_detector", review)
        self.assertIn("budget_shock_absorber", review)
        self.assertIn("vendor_leverage_index", review)
        self.assertIn("executive_narrative_diff", review)
        self.assertIn("executive_decision_defense", review)
        self.assertIn("decision_liability_shield", review)
        self.assertIn("executive_blind_spot_radar", review)
        self.assertIn("commitment_integrity_score", review)
        self.assertIn("board_narrative_stress_test", review)
        self.assertIn("value_realization_firewall", review)
        self.assertIn("risk_to_cash_translator", review)
        self.assertIn("decision_sla_monitor", review)
        self.assertIn("control_evidence_readiness", review)
        self.assertIn("scenario_kill_switch", review)
        self.assertFalse(review["autonomy_gate"]["external_execution_allowed"])
        self.assertTrue(review["action_ledger"])
        self.assertGreaterEqual(review["cio_work_autonomy_map"]["estimated_cio_work_prepared_percent"], 0)
        self.assertTrue(review["board_objection_simulator"])
        self.assertTrue(review["decision_debt_ledger"])
        self.assertGreaterEqual(review["truth_gap_detector"]["truth_gap_count"], 0)
        self.assertGreater(review["executive_time_saved_estimate"]["estimated_hours_prepared"], 0)
        self.assertTrue(review["cio_shadow_agenda"])
        self.assertEqual(review["human_control_contract"]["execution_policy"], "draft_only_until_explicit_tool_and_user_approval_exist")
        self.assertIn(review["decision_sla_enforcer"]["recommended_decision_sla"], {"24h", "7d", "30d"})
        self.assertIn("exit_options", review["vendor_exit_simulator"])
        self.assertTrue(review["regulatory_shock_simulator"]["minimum_response_pack"])
        self.assertGreaterEqual(review["cyber_business_impact_translator"]["cyber_signal_count"], 0)
        self.assertIn("criticality", review["talent_criticality_radar"])
        self.assertTrue(review["capital_allocation_copilot"]["allocation_options"])
        self.assertTrue(review["post_decision_learning_loop"]["update_targets"])
        self.assertGreaterEqual(review["cio_os_maturity_index"]["score"], 0)
        self.assertTrue(review["stakeholder_alignment_matrix"]["matrix"])
        self.assertIn("waiver_needed", review["exception_waiver_factory"])
        self.assertTrue(review["policy_as_code_readiness"]["codifiable_controls"])
        self.assertTrue(review["benefits_realization_sentinel"]["watch_items"])
        self.assertTrue(review["operating_rhythm_autopilot"]["next_rituals"])
        self.assertTrue(review["autonomous_escalation_drafts"])
        self.assertGreaterEqual(review["executive_decision_backlog"]["backlog_count"], 1)
        self.assertTrue(review["enterprise_control_tower"]["control_panels"])
        self.assertTrue(review["ma_carveout_readiness"]["readiness_domains"])
        self.assertTrue(review["data_trust_radar"]["required_controls"])
        self.assertTrue(review["architecture_runway_guardian"]["guardrails"])
        self.assertIn("board_narrative", review["executive_narrative_generator"])
        self.assertGreaterEqual(review["autonomous_due_diligence_questions"]["question_count"], 1)
        self.assertTrue(review["resilience_continuity_planner"]["minimum_plan"])
        self.assertTrue(review["customer_trust_impact_radar"]["trust_dimensions"])
        self.assertTrue(review["ai_portfolio_governance"]["portfolio_controls"])
        self.assertTrue(review["cost_of_delay_calculator"]["delay_impacts"])
        self.assertGreaterEqual(review["executive_commitment_tracker"]["commitment_count"], 1)
        self.assertTrue(review["decision_rights_mapper"]["decision_rights"])
        self.assertTrue(review["okr_strategy_fit_checker"]["fit_questions"])
        self.assertIn("docket_required", review["risk_acceptance_docket"])
        self.assertTrue(review["service_health_sentinel"]["health_dimensions"])
        self.assertTrue(review["knowledge_continuity_planner"]["continuity_actions"])
        self.assertGreaterEqual(review["dependency_breakpoint_analyzer"]["breakpoint_count"], 1)
        self.assertTrue(review["transformation_kill_criteria"]["criteria"])
        self.assertTrue(review["vendor_negotiation_brief"]["asks"])
        self.assertTrue(review["compliance_evidence_pack"]["pack_sections"])
        self.assertTrue(review["board_decision_simulator"]["simulation"])
        self.assertTrue(review["operating_risk_heatmap"]["heatmap"])
        self.assertIn("roadmap_rule", review["autonomous_roadmap_reprioritizer"])
        self.assertIn("finding_risk", review["audit_finding_predictor"])
        self.assertTrue(review["platform_rationalization_advisor"]["candidate_actions"])
        self.assertTrue(review["data_sovereignty_radar"]["required_checks"])
        self.assertIn("debt_count", review["operating_model_debt_ledger"])
        self.assertTrue(review["strategic_option_portfolio"]["portfolio"])
        self.assertTrue(review["executive_decision_war_room"]["roles"])
        self.assertIn("custody_required", review["evidence_chain_of_custody"])
        self.assertTrue(review["decision_rollback_planner"]["rollback_triggers"])
        self.assertGreaterEqual(review["autonomy_risk_budget"]["budget_used_percent"], 0)
        self.assertGreaterEqual(review["approval_boundary_mapper"]["boundary_count"], 1)
        self.assertTrue(review["evidence_expiry_monitor"]["watched_items"])
        self.assertTrue(review["residual_risk_contract"]["minimum_contract_terms"])
        self.assertGreaterEqual(review["autonomy_stress_test"]["stress_score"], 0)
        self.assertTrue(review["decision_consequence_ledger"]["consequences"])
        self.assertTrue(review["enterprise_friction_map"]["friction_map"])
        self.assertTrue(review["strategic_optionality_engine"]["options"])
        self.assertIn("control_debt_count", review["control_debt_burndown"])
        self.assertTrue(review["executive_dissent_synthesizer"]["dissent_items"])
        self.assertTrue(review["decision_backtest_simulator"]["synthetic_backtest"])
        self.assertIn("drift_detected", review["governance_drift_detector"])
        self.assertTrue(review["budget_shock_absorber"]["absorption_moves"])
        self.assertIn("leverage_score", review["vendor_leverage_index"])
        self.assertTrue(review["executive_narrative_diff"]["reconciliation_questions"])
        for action in review["action_ledger"]:
            self.assertIn("autonomy_level", action)
            self.assertIn("required_approval", action)
        self.assert_invariants(review)

    def test_autopilot_review_from_file_and_directory(self):
        file_review = build_autopilot_review_from_file(str(ENGINE / "examples" / "autopilot_review.json"))
        self.assertEqual(file_review["artifact"], "Autonomous CIO Autopilot Review")
        self.assertIn("source_ref", file_review)
        self.assert_invariants(file_review)

        dir_review = build_autopilot_review_from_file(str(ENGINE / "examples"), str(ENGINE / "examples" / "memory.json"))
        self.assertEqual(dir_review["artifact"], "Autonomous CIO Autopilot Review")
        self.assertIn("source_ref", dir_review)
        self.assert_invariants(dir_review)

    def test_product_stage_two_features(self):
        context = self.load_example("industrial_operating_review.json")

        profiles = connector_profile_catalog()
        self.assertGreaterEqual(len(profiles["profiles"]), 19)
        profile_names = {profile["profile"] for profile in profiles["profiles"]}
        self.assertIn("outlook_email", profile_names)
        self.assertIn("slack_messages", profile_names)
        self.assertIn("gmail_workspace", profile_names)
        self.assertIn("jira_delivery", profile_names)
        self.assertIn("azure_devops_delivery", profile_names)
        self.assertIn("servicenow_service", profile_names)
        self.assertIn("cmdb_assets", profile_names)
        self.assertIn("cloud_cost", profile_names)
        self.assertIn("security_findings", profile_names)
        self.assertIn("observability_monitoring", profile_names)
        self.assertIn("erp_sap", profile_names)
        self.assertIn("confluence_knowledge", profile_names)
        self.assertIn("google_drive_documents", profile_names)
        self.assert_invariants(profiles)

        detection = detect_connector_profile(str(ENGINE / "examples" / "industrial_file_drop.csv"))
        self.assertEqual(detection["detected_profile"], "industrial_file_drop")
        self.assert_invariants(detection)

        adapted = adapt_connector_export(str(ENGINE / "examples" / "topdesk_export.csv"))
        self.assertEqual(adapted["profile"], "topdesk_service")
        self.assertGreaterEqual(adapted["signals_created"], 2)
        self.assertIn("decision_packet", adapted)
        self.assert_invariants(adapted)

        slack_detection = detect_connector_profile(str(ENGINE / "examples" / "slack_export.csv"))
        self.assertEqual(slack_detection["detected_profile"], "slack_messages")
        slack_adapted = adapt_connector_export(str(ENGINE / "examples" / "slack_export.csv"))
        self.assertEqual(slack_adapted["profile"], "slack_messages")
        self.assertGreaterEqual(slack_adapted["signals_created"], 2)
        self.assert_invariants(slack_adapted)

        outlook_detection = detect_connector_profile(str(ENGINE / "examples" / "outlook_email_export.csv"))
        self.assertEqual(outlook_detection["detected_profile"], "outlook_email")
        outlook_adapted = adapt_connector_export(str(ENGINE / "examples" / "outlook_email_export.csv"))
        self.assertEqual(outlook_adapted["profile"], "outlook_email")
        self.assertGreaterEqual(outlook_adapted["signals_created"], 2)
        self.assert_invariants(outlook_adapted)

        gmail_detection = detect_connector_profile(str(ENGINE / "examples" / "gmail_workspace_export.csv"))
        self.assertEqual(gmail_detection["detected_profile"], "gmail_workspace")
        gmail_adapted = adapt_connector_export(str(ENGINE / "examples" / "gmail_workspace_export.csv"))
        self.assertEqual(gmail_adapted["profile"], "gmail_workspace")
        self.assertGreaterEqual(gmail_adapted["signals_created"], 2)
        self.assert_invariants(gmail_adapted)

        connector_examples = {
            "jira_delivery_export.csv": "jira_delivery",
            "azure_devops_export.csv": "azure_devops_delivery",
            "servicenow_export.csv": "servicenow_service",
            "cmdb_assets_export.csv": "cmdb_assets",
            "cloud_cost_export.csv": "cloud_cost",
            "security_findings_export.csv": "security_findings",
            "observability_export.csv": "observability_monitoring",
            "erp_sap_export.csv": "erp_sap",
            "confluence_export.csv": "confluence_knowledge",
            "google_drive_export.csv": "google_drive_documents",
        }
        for file_name, expected_profile in connector_examples.items():
            with self.subTest(file_name=file_name):
                detected = detect_connector_profile(str(ENGINE / "examples" / file_name))
                self.assertEqual(detected["detected_profile"], expected_profile)
                adapted_export = adapt_connector_export(str(ENGINE / "examples" / file_name))
                self.assertEqual(adapted_export["profile"], expected_profile)
                self.assertGreaterEqual(adapted_export["signals_created"], 2)
                self.assert_invariants(adapted_export)

        contract = build_llm_extraction_contract(context)
        self.assertIn("required_output_fields", contract["contract"])
        self.assertIn("facts", contract["contract"]["required_output_fields"])
        self.assert_invariants(contract)

        orchestration = run_skill_orchestrator(context)
        chain = orchestration["orchestration"]["selected_skill_chain"]
        self.assertIn("industrial-cio-operating-system", chain)
        self.assertIn("executive-decision-packet", chain)
        self.assertIn("memory_update_proposal", orchestration)
        self.assert_invariants(orchestration)

        proposal = propose_memory_updates(context, self.load_example("memory.json"))
        self.assertTrue(proposal["memory_update_proposal"]["risk_chain_map"])
        self.assert_invariants(proposal)

        with tempfile.TemporaryDirectory() as tmp:
            package = export_decision_package(context, str(Path(tmp) / "package"))
            self.assertGreaterEqual(len(package["files"]), 6)
            for file_name in package["files"]:
                self.assertTrue(Path(file_name).exists())
            self.assert_invariants(package)

            office = export_office_package(context, str(Path(tmp) / "office"))
            self.assertEqual(len(office["files"]), 2)
            for file_name in office["files"]:
                target = Path(file_name)
                self.assertTrue(target.exists())
                self.assertGreater(target.stat().st_size, 300)
            self.assert_invariants(office)

            memory_path = Path(tmp) / "memory.json"
            save_packet_to_memory(context, str(memory_path))
            inspected = inspect_memory_store(str(memory_path))
            self.assertGreater(inspected["decision_count"], 0)
            self.assert_invariants(inspected)

    def test_cli_outputs_json(self):
        command = [
            sys.executable,
            str(ENGINE / "cli.py"),
            "build-decision-packet",
            "--input",
            str(ENGINE / "examples" / "board_prep.json"),
        ]
        proc = subprocess.run(command, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        self.assertEqual(data["artifact"], "Executive Decision Packet")

    def test_productized_cio_os_runtime(self):
        context = self.load_example("industrial_operating_review.json")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            db = tmp_path / "memory.db"
            init_out = init_memory_db(str(db))
            self.assertTrue(db.exists())
            self.assert_invariants(init_out)

            saved = save_review_to_db(context, str(db))
            self.assertIn("review_id", saved["review_saved_to_sqlite_memory"])
            self.assert_invariants(saved)

            feedback = record_feedback(self.load_example("learning_feedback.json"), str(db))
            self.assertEqual(feedback["decision_feedback_recorded"]["rating"], 5)
            self.assert_invariants(feedback)

            outcome = record_outcome(self.load_example("learning_outcome.json"), str(db))
            self.assertEqual(outcome["decision_outcome_recorded"]["score_accuracy"], 82)
            self.assert_invariants(outcome)

            chain_feedback = record_skill_chain_feedback(self.load_example("skill_chain_feedback.json"), str(db))
            self.assertEqual(chain_feedback["skill_chain_feedback_recorded"]["rating"], 5)
            self.assert_invariants(chain_feedback)

            questions = board_question_memory(self.load_example("board_questions.json"), str(db))
            self.assertEqual(questions["board_question_memory"]["stored_count"], 3)
            self.assert_invariants(questions)

            query = query_memory_db(str(db), "")
            self.assertTrue(query["sqlite_memory_query"]["results"]["decisions"])
            self.assert_invariants(query)

            aging = memory_aging(str(db))
            self.assertIn("overdue_actions", aging["memory_aging_review"])
            self.assert_invariants(aging)

            sla = sla_monitor(str(db))
            self.assertIn("breach_risk", sla["decision_sla_monitor"])
            self.assert_invariants(sla)

            calibration = calibrate_scores(str(db))
            self.assertIn("adjustments", calibration["score_calibration"])
            self.assert_invariants(calibration)

            patterns = learn_patterns(str(db))
            self.assertIn("patterns", patterns["learned_pattern_library"])
            self.assert_invariants(patterns)

            reputation = source_reputation(str(db))
            self.assertTrue(reputation["source_reputation"]["sources"])
            self.assert_invariants(reputation)

            backtest = recommendation_backtest(str(db))
            self.assertEqual(backtest["recommendation_backtest"]["outcome_count"], 1)
            self.assert_invariants(backtest)

            digest = learning_digest(str(db))
            self.assertIn("score_calibration", digest["adaptive_cio_learning_digest"])
            self.assert_invariants(digest)

            profile = tmp_path / "profile.json"
            init_profile_out = init_profile(str(profile))
            self.assertTrue(profile.exists())
            self.assert_invariants(init_profile_out)
            applied = apply_profile(context, str(profile))
            self.assertIn("user_company_profile", applied["user_company_profile_applied"]["input_context"])
            self.assert_invariants(applied)

            board_dir = tmp_path / "board"
            board_pack = build_board_pack(context, str(board_dir), "both")
            self.assertGreaterEqual(len(board_pack["files"]), 2)
            self.assert_invariants(board_pack)

        policy = evaluate_policy(context, "audit")
        self.assertIn("readiness", policy["policy_evaluation"])
        self.assert_invariants(policy)

        gates = approval_gates(context)
        self.assertTrue(gates["approval_gates"]["gates"])
        self.assert_invariants(gates)

        governance = governance_readiness(context)
        self.assertIn("score", governance["governance_readiness"])
        self.assert_invariants(governance)

        twin = run_decision_twin(context, "defer")
        self.assertIn("score_deltas", twin)
        self.assert_invariants(twin)

        evidence = score_evidence_quality(context)
        self.assertIn("average_score", evidence["evidence_quality"])
        self.assert_invariants(evidence)

        drafts = draft_actions(context, "email")
        self.assertTrue(drafts["drafts"])
        self.assertFalse(drafts["drafts"][0]["executed"])
        self.assert_invariants(drafts)

        discovery = discover_sources(str(ENGINE / "examples"))
        self.assertTrue(discovery["source_discovery"]["sources"])
        self.assert_invariants(discovery)

        bundle = ingest_source_bundle(str(ENGINE / "examples"))
        self.assertGreater(bundle["source_bundle"]["signals_created"], 0)
        self.assert_invariants(bundle)

        evals = run_evals(str(ENGINE / "evals"))
        self.assertEqual(evals["eval_report"]["case_count"], 50)
        self.assertEqual(evals["eval_report"]["failed_count"], 0)
        self.assert_invariants(evals)

    def test_adaptive_cio_os_usp_modules(self):
        context = self.load_example("industrial_operating_review.json")
        board = self.load_example("board_prep.json")
        ai = self.load_example("ai_governance.json")
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "memory.db"
            init_memory_db(str(db))
            save_review_to_db(context, str(db))
            record_feedback(self.load_example("learning_feedback.json"), str(db))
            record_outcome(self.load_example("learning_outcome.json"), str(db))
            board_question_memory(self.load_example("board_questions.json"), str(db))

            dna = build_decision_dna(str(db))
            self.assertIn("traits", dna["decision_dna"])
            self.assert_invariants(dna)

            appetite = build_risk_appetite_twin(str(db))
            self.assertGreaterEqual(appetite["cio_risk_appetite_twin"]["risk_appetite_score"], 0)
            self.assertLessEqual(appetite["cio_risk_appetite_twin"]["risk_appetite_score"], 100)
            self.assert_invariants(appetite)

            board_memory = build_board_memory(str(db))
            self.assertGreaterEqual(board_memory["board_memory"]["question_count"], 3)
            self.assert_invariants(board_memory)

            graph = build_accountability_graph(board, str(db))
            self.assertGreater(graph["executive_accountability_graph"]["edge_count"], 0)
            self.assert_invariants(graph)

            friction = score_organizational_friction(board, str(db))
            self.assertGreaterEqual(friction["organizational_friction_score"]["score"], 0)
            self.assertLessEqual(friction["organizational_friction_score"]["score"], 100)
            self.assert_invariants(friction)

            collisions = detect_decision_collisions(context, str(db))
            self.assertGreaterEqual(collisions["decision_collision_detector"]["collision_count"], 1)
            self.assert_invariants(collisions)

            strategic = detect_strategic_contradictions(context, str(db))
            self.assertIn("contradiction_count", strategic["strategic_contradiction_radar"])
            self.assert_invariants(strategic)

            weekly = build_weekly_operating_autopilot(str(db))
            self.assertTrue(weekly["cio_weekly_operating_autopilot"]["top_decisions"])
            self.assert_invariants(weekly)

            brief_dir = Path(tmp) / "weekly"
            brief = build_executive_weekly_brief(str(db), str(brief_dir), "both")
            self.assertEqual(brief["artifact"], "Executive Weekly Brief")
            self.assertIn("# Executive Weekly Brief", brief["executive_weekly_brief"]["content"])
            self.assertEqual(len(brief["executive_weekly_brief"]["files"]), 2)
            for file_name in brief["executive_weekly_brief"]["files"]:
                self.assertTrue(Path(file_name).exists())
                self.assertGreater(Path(file_name).stat().st_size, 100)
            self.assert_invariants(brief)

            ledger = build_enterprise_decision_ledger(str(db))
            self.assertTrue(ledger["enterprise_decision_ledger"]["decisions"])
            self.assert_invariants(ledger)

            control = trace_control_to_decision(ai, str(db))
            self.assertGreaterEqual(control["control_to_decision_traceability"]["link_count"], 1)
            self.assert_invariants(control)

            vendor = score_vendor_truth(context, str(db))
            self.assertGreaterEqual(vendor["vendor_truth_index"]["truth_score"], 0)
            self.assertLessEqual(vendor["vendor_truth_index"]["truth_score"], 100)
            self.assert_invariants(vendor)

        narrative = detect_narrative_integrity(board)
        self.assertTrue(narrative["narrative_integrity_detector"]["contradictions"])
        self.assert_invariants(narrative)

        arena = run_decision_simulation_arena(board)
        self.assertEqual(len(arena["decision_simulation_arena"]["scenarios"]), 6)
        self.assert_invariants(arena)

        delegation = build_delegation_planner(board)
        self.assertTrue(delegation["autonomous_delegation_planner"]["delegations"])
        self.assertFalse(delegation["autonomous_delegation_planner"]["delegations"][0]["executed"])
        self.assert_invariants(delegation)

        shadow = shadow_cost_of_inaction(board)
        self.assertGreaterEqual(shadow["shadow_cost_of_inaction"]["cost_count"], 1)
        self.assert_invariants(shadow)

    def test_executive_autonomy_innovation_modules(self):
        context = self.load_example("industrial_operating_review.json")
        board = self.load_example("board_prep.json")
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "memory.db"
            init_memory_db(str(db))
            save_review_to_db(context, str(db))
            record_outcome(self.load_example("learning_outcome.json"), str(db))
            board_question_memory(self.load_example("board_questions.json"), str(db))

            operating_twin = build_enterprise_operating_twin(context, str(db))
            self.assertIn("operating_model_completeness", operating_twin["enterprise_operating_twin"])
            self.assert_invariants(operating_twin)

            autonomy_contract = build_autonomy_contract_engine(context, str(db))
            self.assertTrue(autonomy_contract["autonomy_contract_engine"]["clauses"])
            self.assertFalse(autonomy_contract["autonomy_contract_engine"]["clauses"][0]["external_execution_allowed"])
            self.assert_invariants(autonomy_contract)

            custody = build_decision_chain_of_custody(context, str(db))
            self.assertTrue(custody["decision_chain_of_custody"]["packet_fingerprint"].startswith("local-"))
            self.assert_invariants(custody)

            attention = allocate_executive_attention(context, str(db))
            self.assertTrue(attention["executive_attention_allocator"]["allocation"])
            self.assert_invariants(attention)

            kill = build_kill_criteria_sentinel(board, str(db))
            self.assertIn(kill["kill_criteria_sentinel"]["kill_pressure"], {"Low", "Medium", "High"})
            self.assert_invariants(kill)

            benefits = build_benefit_realization_memory(str(db))
            self.assertGreaterEqual(benefits["benefit_realization_memory"]["decision_count"], 1)
            self.assert_invariants(benefits)

            drift = detect_strategic_drift_early_warning(context, str(db))
            self.assertIn("warning_level", drift["strategic_drift_early_warning"])
            self.assert_invariants(drift)

            vendor = backtest_vendor_promises(context, str(db))
            self.assertGreaterEqual(vendor["vendor_promise_backtester"]["promise_reliability_score"], 0)
            self.assertLessEqual(vendor["vendor_promise_backtester"]["promise_reliability_score"], 100)
            self.assert_invariants(vendor)

            latency = measure_decision_latency_cost(context, str(db))
            self.assertIn(latency["decision_latency_cost_meter"]["recommended_decision_sla"], {"24h", "7d", "30d"})
            self.assert_invariants(latency)

            decay = forecast_evidence_decay(context, str(db))
            self.assertTrue(decay["evidence_decay_forecast"]["evidence_items"])
            self.assert_invariants(decay)

            committee = simulate_synthetic_executive_committee(context, str(db))
            self.assertEqual(committee["synthetic_executive_committee"]["committee_size"], 6)
            self.assert_invariants(committee)

            control_debt = build_control_debt_ledger(context, str(db))
            self.assertIn("control_debt_count", control_debt["control_debt_ledger"])
            self.assert_invariants(control_debt)

            rhythm = build_operating_rhythm_autopilot_v2(str(db))
            self.assertEqual(len(rhythm["operating_rhythm_autopilot"]["cadences"]), 4)
            self.assert_invariants(rhythm)

            contradiction = build_enterprise_contradiction_memory(board, str(db))
            self.assertIn("recurrence_risk", contradiction["enterprise_contradiction_memory"])
            self.assert_invariants(contradiction)

            replacement = map_cio_replacement_surface(context, str(db))
            self.assertGreaterEqual(replacement["cio_replacement_surface_map"]["estimated_cio_work_prepared_percent"], 0)
            self.assertFalse(any(item.get("automation_level") == "external_execution_allowed" for item in replacement["cio_replacement_surface_map"]["surfaces"]))
            self.assert_invariants(replacement)

    def test_product_hardening_runtime(self):
        context = self.load_example("board_prep.json")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            db = tmp_path / "memory.db"
            init_memory_db(str(db))

            pipeline = build_llm_extraction_pipeline(context)
            self.assertIn(pipeline["llm_extraction_pipeline"]["mode"], {"heuristic_fallback", "host_llm_structured_input"})
            self.assertTrue(pipeline["llm_extraction_pipeline"]["extraction_check"]["valid"])
            self.assert_invariants(pipeline)

            validation = validate_output_schema(pipeline, "llm-extraction-pipeline.schema.json")
            self.assertTrue(validation["schema_validation"]["valid"])
            self.assert_invariants(validation)

            queued = queue_memory_updates(context, str(db))
            self.assertGreaterEqual(queued["memory_update_queue"]["queued_count"], 1)
            self.assert_invariants(queued)

            queue = list_memory_update_queue(str(db))
            self.assertTrue(queue["memory_update_queue_review"]["updates"])
            first_id = queue["memory_update_queue_review"]["updates"][0]["id"]
            reviewed = review_memory_update(str(db), first_id, "Approved", "Unit test")
            self.assertEqual(reviewed["memory_update_reviewed"]["decision"], "Approved")
            self.assert_invariants(reviewed)

            suites = skill_suite_map()
            self.assertGreaterEqual(suites["skill_suite_map"]["suite_count"], 6)
            self.assert_invariants(suites)

            hardening = run_hardening_evals(str(ENGINE / "evals"))
            self.assertTrue(hardening["hardening_eval_report"]["hardening_checks"]["minimum_case_count"])
            self.assert_invariants(hardening)

            release = build_release_package(str(tmp_path / "release"))
            self.assertTrue(Path(release["release_package"]["zip"]).exists())
            self.assertGreater(release["release_package"]["zip_size_bytes"], 1000)
            self.assert_invariants(release)

    def test_cli_autopilot_review_outputs_json_and_markdown(self):
        json_command = [
            sys.executable,
            str(ENGINE / "cli.py"),
            "autopilot-review",
            "--input",
            str(ENGINE / "examples" / "autopilot_review.json"),
            "--memory",
            str(ENGINE / "examples" / "memory.json"),
        ]
        json_proc = subprocess.run(json_command, capture_output=True, text=True, check=True)
        data = json.loads(json_proc.stdout)
        self.assertEqual(data["artifact"], "Autonomous CIO Autopilot Review")
        self.assertIn("autonomy_gate", data)

        markdown_command = [
            sys.executable,
            str(ENGINE / "cli.py"),
            "autopilot-review",
            "--input",
            str(ENGINE / "examples" / "autopilot_review.json"),
            "--format",
            "markdown",
        ]
        markdown_proc = subprocess.run(markdown_command, capture_output=True, text=True, check=True)
        markdown = json.loads(markdown_proc.stdout)
        self.assertEqual(markdown["format"], "markdown")
        self.assertIn("# Autonomous CIO Operating Review", markdown["content"])
        self.assertIn("## CIO Shadow Agenda", markdown["content"])
        self.assertIn("## Human Control Contract", markdown["content"])
        self.assertIn("## Decision SLA", markdown["content"])
        self.assertIn("## CIO OS Maturity", markdown["content"])
        self.assertIn("## Stakeholder Alignment", markdown["content"])
        self.assertIn("## Operating Rhythm Autopilot", markdown["content"])
        self.assertIn("## Escalation Drafts", markdown["content"])
        self.assertIn("## Enterprise Control Tower", markdown["content"])
        self.assertIn("## Executive Narrative", markdown["content"])
        self.assertIn("## Due Diligence Questions", markdown["content"])
        self.assertIn("## Resilience Continuity", markdown["content"])
        self.assertIn("## Cost of Delay", markdown["content"])
        self.assertIn("## Decision Rights", markdown["content"])
        self.assertIn("## Dependency Breakpoints", markdown["content"])
        self.assertIn("## Transformation Kill Criteria", markdown["content"])
        self.assertIn("## Roadmap Reprioritizer", markdown["content"])
        self.assertIn("## Audit Finding Predictor", markdown["content"])
        self.assertIn("## Decision War Room", markdown["content"])
        self.assertIn("## Evidence Chain of Custody", markdown["content"])
        self.assertIn("## Autonomy Risk Budget", markdown["content"])
        self.assertIn("## Approval Boundary Mapper", markdown["content"])
        self.assertIn("## Evidence Expiry Monitor", markdown["content"])
        self.assertIn("## Residual Risk Contract", markdown["content"])
        self.assertIn("## Autonomy Stress Test", markdown["content"])
        self.assertIn("## Decision Consequence Ledger", markdown["content"])
        self.assertIn("## Enterprise Friction Map", markdown["content"])
        self.assertIn("## Strategic Optionality Engine", markdown["content"])
        self.assertIn("## Control Debt Burndown", markdown["content"])
        self.assertIn("## Executive Dissent Synthesizer", markdown["content"])
        self.assertIn("## Decision Backtest Simulator", markdown["content"])
        self.assertIn("## Governance Drift Detector", markdown["content"])
        self.assertIn("## Budget Shock Absorber", markdown["content"])
        self.assertIn("## Vendor Leverage Index", markdown["content"])
        self.assertIn("## Executive Narrative Diff", markdown["content"])

        compact_command = [
            sys.executable,
            str(ENGINE / "cli.py"),
            "autopilot-review",
            "--input",
            str(ENGINE / "examples" / "autopilot_review.json"),
            "--format",
            "markdown",
            "--view",
            "compact",
        ]
        compact_proc = subprocess.run(compact_command, capture_output=True, text=True, check=True)
        compact = json.loads(compact_proc.stdout)
        self.assertEqual(compact["view"], "compact")
        self.assertIn("# Autonomous CIO Operating Review - Compact", compact["content"])
        self.assertIn("## Guarded Autonomy", compact["content"])
        self.assertNotIn("## Executive Dissent Synthesizer", compact["content"])

        board_command = [
            sys.executable,
            str(ENGINE / "cli.py"),
            "autopilot-review",
            "--input",
            str(ENGINE / "examples" / "autopilot_review.json"),
            "--format",
            "markdown",
            "--view",
            "board",
        ]
        board_proc = subprocess.run(board_command, capture_output=True, text=True, check=True)
        board = json.loads(board_proc.stdout)
        self.assertEqual(board["view"], "board")
        self.assertIn("# Autonomous CIO Board Pack", board["content"])
        self.assertIn("## Board Challenge Questions", board["content"])
        self.assertIn("## Human-Control Boundary", board["content"])

    def test_cli_missing_input_fails(self):
        command = [
            sys.executable,
            str(ENGINE / "cli.py"),
            "score",
            "--input",
            str(ENGINE / "examples" / "missing.json"),
        ]
        proc = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("error:", proc.stderr)


if __name__ == "__main__":
    unittest.main()
