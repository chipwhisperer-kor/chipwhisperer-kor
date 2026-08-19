import json
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stdout

import h5py
import numpy as np

from physai import artifacts, collect, conformance, demo, grok_once, paths, preprocess, profiles, report, spec
from physai.algorithms import get as get_algorithm
from physai.collectors import cw_power
from physai.tests import spa as spa_test
import sca_schema as S


class V2ContractTests(unittest.TestCase):
    def test_all_committed_experiments_are_v2_and_resolve(self):
        _, study_experiments = spec.study_experiments(paths.PROJECT / "demo" / "study.yaml")
        study_specs = {Path(item["_spec_path"]): item for _, item in study_experiments}
        for path in sorted(paths.EXP.glob("*.yaml")):
            raw = path.read_text(encoding="utf-8")
            for duplicated in ("security_level:", "effect_size_d:", "target_level:",
                               "max_acquisition_hours:", "preprocessing:"):
                self.assertNotIn(duplicated, raw)
            resolved = study_specs.get(path.resolve()) or spec.load(path)
            self.assertIn(resolved["criteria"]["security_level"], (3, 4))
            self.assertTrue(all(item["n"] > 0 for item in resolved["subsets"]))

    def test_default_study_is_l3_lab_and_physical_volume_is_332(self):
        study, experiments = spec.study_experiments(paths.PROJECT / "demo" / "study.yaml")
        self.assertEqual((study["assessment_profile"], study["campaign_stage"]),
                         ("iso-17825-l3", "cw-lab-pilot"))
        physical = [sp for _, sp in experiments if sp["collector"]["kind"] == "cw_power"]
        self.assertEqual(len(physical), 2)
        self.assertTrue(all(sum(item["n"] for item in sp["subsets"]) == 332 for sp in physical))
        self.assertTrue(all(sp["criteria"]["preprocessing"]["average_n"] == 10
                            for sp in physical))

    def test_profiles_derive_full_counts_and_have_one_statistics_definition(self):
        self.assertEqual(profiles.PROFILES["iso-17825-l3"]["effect_size_d"], 0.04)
        self.assertEqual(profiles.PROFILES["iso-17825-l4"]["effect_size_d"], 0.01)
        self.assertGreater(profiles.required_n_from_profile("iso-17825-l4"),
                           profiles.required_n_from_profile("iso-17825-l3"))
        resolved = spec.load_from_study(paths.PROJECT / "demo" / "study.yaml",
                                        "demo_l3lab_hw_tinyaes")
        self.assertEqual(resolved["criteria"]["alpha"], profiles.STATISTICS["alpha"])

    def test_preflight_contains_resolved_counts_without_install_paths(self):
        with tempfile.TemporaryDirectory() as directory, \
             mock.patch.object(demo.paths, "RUNS", Path(directory)):
            preflight = json.loads(demo.write_preflight().read_text(encoding="utf-8"))
        physical = [item["resolved_spec"] for item in preflight["experiments"]
                    if item["resolved_spec"]["collector"]["kind"] == "cw_power"]
        self.assertTrue(physical)
        self.assertTrue(all(sum(row["n"] for row in item["subsets"]) == 332
                            for item in physical))
        self.assertTrue(all(item["criteria"]["alpha"] == profiles.STATISTICS["alpha"]
                            for item in physical))
        self.assertNotIn("_spec_path", json.dumps(preflight))

    def test_failure_evidence_keeps_command_and_return_code(self):
        with tempfile.TemporaryDirectory() as directory, \
             mock.patch.object(demo.paths, "RUNS", Path(directory)):
            error = __import__("subprocess").CalledProcessError(7, ["python3", "collect.py"])
            failure = json.loads(demo.write_failure("study", error).read_text(encoding="utf-8"))
        self.assertEqual(failure["returncode"], 7)
        self.assertEqual(failure["command"], ["python3", "collect.py"])

    def test_conformance_notes_match_channel_and_verdict(self):
        base_spec = {"criteria": {"max_acquisition_hours": 6},
                     "profile_requirements": {"ta_raw_per_block": 1000}}
        emulated = conformance._annex_a_items(
            {"schema_version": "1.3", "dataset_role": "derived-analysis",
             "aggregation_n": 10, "alignment": "trigger-checked",
             "channel_type": "emulated-power"}, base_spec, {}, "A.2", 3)
        physical = conformance._annex_a_items(
            {"schema_version": "1.3", "dataset_role": "derived-analysis",
             "aggregation_n": 10, "alignment": "trigger-checked",
             "channel_type": "power"}, base_spec, {}, "A.2", 3)
        emul_average = next(row for row in emulated if row["clause"].startswith("A.2.5"))
        emul_alignment = next(row for row in emulated if row["clause"].startswith("A.2.6"))
        physical_alignment = next(row for row in physical if row["clause"].startswith("A.2.6"))
        self.assertEqual(emul_average["verdict"], "준수")
        self.assertNotIn("미준수", emul_average["note"])
        self.assertIn("sample_map", emul_alignment["note"])
        self.assertIn("20회 트리거", physical_alignment["note"])
        self.assertNotIn("에뮬레이션", physical_alignment["note"])

        procedure = conformance._procedure_items(
            {}, {}, {"tests": {}, "reference": {"cpa": {"bytes_recovered": 16}}})
        intermediate = next(row for row in procedure if "[07.11]" in row["clause"])
        self.assertEqual(intermediate["verdict"], "준수")
        self.assertIn("CPA", intermediate["evidence"])

    def test_spa_noise_floor_explanation_matches_collection_channel(self):
        physical = spa_test._noise_floor_note(False, False)
        masked_emulation = spa_test._noise_floor_note(True, True)
        plain_emulation = spa_test._noise_floor_note(True, False)
        self.assertIn("실물 전력 채널", physical)
        self.assertNotIn("0을 기대", physical)
        self.assertIn("마스크를 새로", masked_emulation)
        self.assertIn("0을 기대", plain_emulation)

    def test_capture_contract_ignores_clone_paths_but_not_experiment_values(self):
        first = {"id": "same", "value": 1, "_spec_path": "/clone/a/exp.yaml"}
        second = {"id": "same", "value": 1, "_spec_path": "/clone/b/exp.yaml"}
        self.assertEqual(artifacts.capture_contract(first, "a" * 64),
                         artifacts.capture_contract(second, "a" * 64))
        second["value"] = 2
        self.assertNotEqual(artifacts.capture_contract(first, "a" * 64),
                            artifacts.capture_contract(second, "a" * 64))

    def test_collect_cli_reuses_sealed_manifest_without_starting_collector(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            dataset = tmp / "sealed.h5"
            dataset.write_bytes(b"sealed")
            manifest_path = tmp / "capture_manifest.json"
            manifest_path.write_text("{}", encoding="utf-8")
            run = tmp / "run"
            run.mkdir()
            resolved = {"id": "sealed", "collector": {"kind": "emulation"}}
            manifest = {"capture_contract_sha256": "c" * 64}
            with mock.patch.object(collect.spec_mod, "load", return_value=resolved), \
                 mock.patch.object(collect.artifacts, "capture_manifest_path",
                                   return_value=manifest_path), \
                 mock.patch.object(collect.artifacts, "load_capture_manifest",
                                   return_value=(dataset.resolve(), manifest)), \
                 mock.patch.object(collect.paths, "run_dir", return_value=run), \
                 mock.patch.object(report, "write_plan", return_value=run / "plan.md"), \
                 mock.patch.object(collect, "collect_emulation") as collector, \
                 mock.patch.object(collect.S, "validate_dataset", return_value=[]):
                self.assertEqual(collect.main(["--spec", "unused.yaml", "--quiet"]), 0)
            collector.assert_not_called()

    def test_aes_contract_partition_is_predeclared_and_balanced_enough(self):
        algorithm = get_algorithm("aes-128-ecb")
        plaintext = np.arange(16 * 64, dtype=np.uint8).reshape(64, 16)
        key = np.zeros_like(plaintext)
        labels = algorithm.dpa_partition(plaintext, key, algorithm.DPA_TARGETS[0])
        self.assertEqual(labels.shape, (64,))
        self.assertEqual(set(labels.tolist()), {0, 1})
        with self.assertRaises(ValueError):
            algorithm.dpa_partition(plaintext, key, "post-hoc-target")

    def test_l4_alignment_recovers_shift_and_records_anchor_quality(self):
        rng = np.random.RandomState(7)
        reference = rng.normal(size=1024)
        trace = np.interp(np.arange(1024) + 3, np.arange(1024), reference,
                          left=0.0, right=0.0)
        cfg = profiles.PROFILES["iso-17825-l4"]["preprocessing"]["dynamic_alignment"]
        aligned, evidence = preprocess._align(reference, trace, 4.0, cfg)
        self.assertLessEqual(abs(evidence["static_shift"]), 8)
        self.assertEqual(len(evidence["anchor_shifts"]), 8)
        self.assertGreaterEqual(min(evidence["anchor_correlations"]), 0.8)
        self.assertTrue(np.isfinite(aligned[16:-16]).all())

    def test_l4_prepare_preserves_source_and_builds_derived_repeats(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            source = tmp / "source.h5"
            ns, repeats = 2048, 10
            x = np.arange(ns)
            base = (8000 * np.sin(2 * np.pi * 100 * x / 1000) +
                    3000 * np.exp(-((x - 700) / 35) ** 2))
            raw = np.rint(np.stack([np.roll(base, shift) for shift in range(-5, 5)])) \
                .astype(np.int16)
            with h5py.File(source, "w") as h5:
                metadata = {
                    "schema": S.SCHEMA, "schema_version": S.SCHEMA_VERSION,
                    "dataset_role": "raw-acquisition", "capture_repeats": repeats,
                    "capture_contract_sha256": "a" * 64, "acquisition_status": "complete",
                    "target_name": "synthetic", "target_device": "synthetic",
                    "target_clock_hz": 100.0, "iut_algorithm": "aes-128-ecb",
                    "iut_implementation": "tiny-AES-c", "iut_countermeasure": "none",
                    "channel_type": "power", "channel_probe": "synthetic",
                    "sample_rate_hz": 1000.0, "sample_resolution_bits": 16,
                    "samples_per_trace": ns, "sample_dtype": "int16",
                    "sample_scale": 32768.0, "sample_axis": "time",
                    "trigger_source": "synthetic", "trigger_semantics": "whole operation",
                    "alignment": "none", "acquisition_start": "2026-01-01T00:00:00",
                    "tool_chain": "unit-test", "bandwidth_hz": 200.0,
                    "bandwidth_basis": "synthetic calibrated fixture",
                    "bandwidth_is_nominal": False, "shunt_ohm": 12.0,
                    "shunt_selection_note": "synthetic fixture", "shunt_max_verified": False,
                    "platform": "synthetic", "adc_mul": 4, "firmware_sha256": "b" * 64,
                    "spec_id": "synthetic_l4", "assessment_profile": "iso-17825-l4",
                }
                for key, value in metadata.items():
                    h5.attrs[key] = value
                group = h5.create_group("spa_same")
                group.attrs.update(role="simple-analysis", n_records=repeats,
                                   n_repeat_groups=1, key_mode="fixed", pt_mode="fixed")
                group.create_dataset(S.F_TRACE, data=raw)
                for field in (S.F_KEY, S.F_PLAINTEXT, S.F_CIPHERTEXT):
                    group.create_dataset(field, data=np.zeros((repeats, 16), dtype=np.uint8))
                group.create_dataset(S.F_EXEC_TIME, data=np.ones(repeats, dtype=np.uint32))
                group.create_dataset(S.F_REPEAT_GROUP_ID,
                                     data=np.zeros(repeats, dtype=np.uint64))
                group.create_dataset(S.F_REPEAT_INDEX,
                                     data=np.arange(repeats, dtype=np.uint16))
            source_sha = artifacts.sha256_file(source)
            self.assertEqual(S.validate_dataset(source), [])
            resolved = spec.load_from_study(paths.PROJECT / "demo" / "study.yaml",
                                            "demo_l3lab_hw_tinyaes")
            resolved["id"] = "synthetic_l4"
            resolved["assessment_profile"] = "iso-17825-l4"
            resolved["criteria"]["security_level"] = 4
            resolved["criteria"]["preprocessing"] = profiles.PROFILES[
                "iso-17825-l4"]["preprocessing"]
            with mock.patch.object(preprocess.paths, "TRACES", tmp), \
                 mock.patch.object(preprocess.paths, "RUNS", tmp / "runs"):
                derived = preprocess.prepare(source, resolved)
            self.assertEqual(source.stat().st_size > 0, True)
            with h5py.File(derived, "r") as h5:
                averaged = h5["spa_same"][S.F_TRACE][:]
                self.assertLess(averaged.shape[-1], ns)
                self.assertEqual(averaged.dtype, np.float64)
                self.assertNotIn(S.F_TRACE_REPEATS, h5["spa_same"])
                self.assertNotIn(S.F_REPEAT_INDEX, h5["spa_same"])
                self.assertEqual(h5.attrs["dataset_role"], "derived-analysis")
                self.assertEqual(h5.attrs["alignment"], "static+dynamic")
            self.assertEqual(artifacts.sha256_file(source), source_sha)
            self.assertEqual(S.validate_dataset(derived), [])
            provenance = derived.with_suffix(".provenance.json")
            self.assertTrue(provenance.is_file())
            with mock.patch.object(preprocess.paths, "TRACES", tmp), \
                 mock.patch.object(preprocess.paths, "RUNS", tmp / "runs"):
                self.assertEqual(preprocess.prepare(source, resolved), derived)
            metadata = json.loads(provenance.read_text(encoding="utf-8"))
            metadata["derived_sha256"] = "0" * 64
            provenance.write_text(json.dumps(metadata), encoding="utf-8")
            with mock.patch.object(preprocess.paths, "TRACES", tmp), \
                 mock.patch.object(preprocess.paths, "RUNS", tmp / "runs"), \
                 self.assertRaisesRegex(preprocess.PreprocessError, "계약 또는 SHA-256"):
                preprocess.prepare(source, resolved)

    def test_raw_append_keeps_every_execution_and_float_mean_is_derived(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.h5"
            traces = np.array([[0, 1], [1, 2], [2, 3]], dtype=np.int16)
            with h5py.File(path, "w") as h5:
                group = cw_power._new_group(
                    h5, {"name": "attack", "role": "attack", "key_mode": "fixed",
                         "pt_mode": "fixed"}, 2, 3, False)
                cw_power._append_record(group, np.zeros(16, dtype=np.uint8),
                                        np.ones(16, dtype=np.uint8), bytes(16), traces,
                                        np.array([4, 5, 6], dtype=np.uint32))
                self.assertTrue(np.array_equal(group[S.F_TRACE][:], traces))
                self.assertEqual(group[S.F_REPEAT_GROUP_ID][:].tolist(), [0, 0, 0])
                self.assertEqual(group[S.F_REPEAT_INDEX][:].tolist(), [0, 1, 2])
                self.assertEqual(group.attrs["n_records"], 3)

    def test_html_is_standalone_and_embeds_svg(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            (tmp / "plot.svg").write_text(
                "<svg xmlns='http://www.w3.org/2000/svg'><circle r='2'/></svg>", encoding="utf-8")
            md = tmp / "report.md"
            md.write_text("# Report\n\n| A | B |\n|---|---|\n| pass | value |\n\n![plot](plot.svg)\n",
                          encoding="utf-8")
            text = report.write_html(md).read_text(encoding="utf-8")
            self.assertIn("data:image/svg+xml;base64,", text)
            self.assertIn("@media print", text)
            self.assertNotIn("https://", text)

    def test_host_grok_one_shot_records_relative_hashes_and_rejects_stale_input(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            (tmp / "runs").mkdir()
            source = tmp / "evidence.json"
            source.write_text('{"verdict":"inconclusive"}', encoding="utf-8")
            fake = tmp / "grok"
            payload = {"structuredOutput": {"ok": True, "overview": "x" * 50,
                       "findings": [{"finding": "f", "evidence": ["e"], "judgment": "j"}],
                       "limitations": ["limited"]}}
            fake.write_text("#!/bin/sh\nprintf '%s\\n' '" + json.dumps(payload) + "'\n",
                            encoding="utf-8")
            fake.chmod(0o755)
            request = grok_once.create_request(tmp, "study", "publish", [source])
            self.assertEqual(request["inputs"][0]["path"], "evidence.json")
            audit_path = grok_once.run_once(tmp, fake)
            with mock.patch.object(demo.paths, "PROJECT", tmp):
                self.assertTrue(demo.validate_grok_audit(audit_path)["review"]["ok"])
            source.write_text('{"verdict":"pass"}', encoding="utf-8")
            with mock.patch.object(demo.paths, "PROJECT", tmp), \
                 self.assertRaisesRegex(ValueError, "stale"):
                demo.validate_grok_audit(audit_path)

    def test_host_grok_failure_writes_matching_error_and_exits(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            (tmp / "runs").mkdir()
            source = tmp / "spec.yaml"
            source.write_text("id: study\n", encoding="utf-8")
            fake = tmp / "grok"
            fake.write_text("#!/bin/sh\nprintf 'failed\\n' >&2\nexit 7\n", encoding="utf-8")
            fake.chmod(0o755)
            request = grok_once.create_request(tmp, "study", "assist-pre-collection", [source])
            with self.assertRaisesRegex(RuntimeError, "rc=7"):
                grok_once.run_once(tmp, fake)
            response = json.loads(grok_once.response_path(
                tmp, "study", "assist-pre-collection").read_text(encoding="utf-8"))
            self.assertEqual(response["request_id"], request["request_id"])
            self.assertIn("rc=7", response["error"])

    def test_notebook_checkpoint_prints_the_canonical_host_command(self):
        with tempfile.TemporaryDirectory() as directory:
            response_path = Path(directory) / "response.json"
            request = {"request_id": "a" * 64}
            response_path.write_text(json.dumps({"request_id": request["request_id"]}),
                                     encoding="utf-8")
            output = io.StringIO()
            with mock.patch.object(grok_once, "create_request", return_value=request), \
                 mock.patch.object(grok_once, "response_path", return_value=response_path), \
                 mock.patch.object(grok_once, "validate_response", return_value={"ok": True}), \
                 redirect_stdout(output):
                self.assertEqual(demo._grok_checkpoint("study", "publish", []), response_path)
            self.assertIn(grok_once.HOST_COMMAND, output.getvalue())

    def test_study_pipeline_gates_iut_on_reference_positive_control(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            study = {"id": "study", "title": "study", "assessment_profile": "iso-17825-l3",
                     "campaign_stage": "cw-lab-pilot", "algorithm": "aes-128-ecb"}
            experiments = [
                ({"role": "positive-control"},
                 {"id": "control", "scope": {"channels": ["power"]},
                  "iut": {"name": "plain"}}),
                ({"role": "iut", "compare_with": "control"},
                 {"id": "masked", "scope": {"channels": ["power"]},
                  "iut": {"name": "masked"}}),
            ]
            for run_id, control in (("control", "fail"), ("masked", "pass")):
                run = tmp / run_id
                run.mkdir(parents=True)
                result = {"tests": {}, "reference": {},
                          "overall": {"preassessment_verdict": "inconclusive",
                                      "human_review": {"spa": "pending"},
                                      "positive_control": control}}
                (run / "results.json").write_text(json.dumps(result), encoding="utf-8")
            with mock.patch.object(demo, "_study_context",
                                   return_value=(study, experiments, ["control", "masked"])), \
                 mock.patch.object(demo.paths, "RUNS", tmp), \
                 mock.patch.object(demo.verify, "verify", return_value={"ok": True}):
                summary = json.loads(demo.write_summary("unused").read_text(encoding="utf-8"))
            self.assertFalse(summary["pre_grok_ok"])
            self.assertFalse(summary["requirements"]["control"]["pipeline_ok"])
            self.assertFalse(summary["requirements"]["masked"]["reference_positive_control_ok"])

    def test_demo_notebook_is_valid_json_and_has_no_embedded_results(self):
        notebook = json.loads((paths.PROJECT / "demo" / "0.1.Demo_without_TraceWhisperer.ipynb")
                              .read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertTrue(code)
        self.assertTrue(all(cell["execution_count"] is None and not cell["outputs"] for cell in code))
        all_source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
        self.assertNotIn("--n-perm", all_source)
        self.assertNotIn("사전 자문 실패(비권위적 단계이므로 실행은 계속)", all_source)
        self.assertNotIn("shutil.which('grok')", all_source)
        self.assertIn("정확한 Python 한 줄", all_source)


if __name__ == "__main__":
    unittest.main()
