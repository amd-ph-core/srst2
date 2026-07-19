#!/usr/bin/env python

import os
import sys
import tempfile
import unittest

from unittest.mock import MagicMock, patch
from io import StringIO

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
)

import srst2


class TestGetSamtoolsExec(unittest.TestCase):
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_samtools_with_overide(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {"SRST2_SAMTOOLS": "/usr/bin/samtools"}
        env_mock.get.side_effect = fake_env_variables.get
        samtools_exec = srst2.get_samtools_exec()
        self.assertEqual(samtools_exec, "/usr/bin/samtools")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_samtools_with_default(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {}
        env_mock.get.side_effect = fake_env_variables.get
        samtools_exec = srst2.get_samtools_exec()
        self.assertEqual(samtools_exec, "samtools")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_samtools_with_missing(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {"SRST2_SAMTOOLS": "/missing/samtools"}
        env_mock.get.side_effect = fake_env_variables.get
        samtools_exec = srst2.get_samtools_exec()
        self.assertEqual(samtools_exec, "samtools")


class TestGetBowtieExecs(unittest.TestCase):
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_with_overides(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {
            "SRST2_BOWTIE2": "/usr/bin/bowtie2",
            "SRST2_BOWTIE2_BUILD": "/usr/bin/bowtie2-build",
        }
        env_mock.get.side_effect = fake_env_variables.get
        bowtie_exec, bowtie_build_exec = srst2.get_bowtie_execs()
        self.assertEqual(bowtie_exec, "/usr/bin/bowtie2")
        self.assertEqual(bowtie_build_exec, "/usr/bin/bowtie2-build")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_with_defaults(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {}
        env_mock.get.side_effect = fake_env_variables.get
        bowtie_exec, bowtie_build_exec = srst2.get_bowtie_execs()
        self.assertEqual(bowtie_exec, "bowtie2")
        self.assertEqual(bowtie_build_exec, "bowtie2-build")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_with_mixture(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {"SRST2_BOWTIE2": "/usr/bin/bowtie2"}
        env_mock.get.side_effect = fake_env_variables.get
        bowtie_exec, bowtie_build_exec = srst2.get_bowtie_execs()
        self.assertEqual(bowtie_exec, "/usr/bin/bowtie2")
        self.assertEqual(bowtie_build_exec, "/usr/bin/bowtie2-build")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_with_other_mixture(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {"SRST2_BOWTIE2_BUILD": "/usr/bin/bowtie2-build"}
        env_mock.get.side_effect = fake_env_variables.get
        bowtie_exec, bowtie_build_exec = srst2.get_bowtie_execs()
        self.assertEqual(bowtie_exec, "bowtie2")
        self.assertEqual(bowtie_build_exec, "/usr/bin/bowtie2-build")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_with_missing(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {
            "SRST2_BOWTIE2": "/missing/bowtie2",
            "SRST2_BOWTIE2_BUILD": "/usr/bin/bowtie2-build",
        }
        env_mock.get.side_effect = fake_env_variables.get
        bowtie_exec, bowtie_build_exec = srst2.get_bowtie_execs()
        self.assertEqual(bowtie_exec, "bowtie2")
        self.assertEqual(bowtie_build_exec, "/usr/bin/bowtie2-build")

    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_with_other_missing(self, env_mock, path_mock):
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {
            "SRST2_BOWTIE2": "/usr/bin/bowtie2",
            "SRST2_BOWTIE2_BUILD": "/missing/bowtie2-build",
        }
        env_mock.get.side_effect = fake_env_variables.get
        bowtie_exec, bowtie_build_exec = srst2.get_bowtie_execs()
        self.assertEqual(bowtie_exec, "/usr/bin/bowtie2")
        self.assertEqual(bowtie_build_exec, "/usr/bin/bowtie2-build")


class TestBowtieIndex(unittest.TestCase):
    @patch("srst2.logging")
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_index_with_overides(
        self, env_mock, path_mock, run_mock, version_mock, logging_mock
    ):
        path_mock.exists.return_value = False
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {
            "SRST2_BOWTIE2": "/usr/bin/bowtie2",
            "SRST2_BOWTIE2_BUILD": "/usr/bin/bowtie2-build",
        }
        env_mock.get.side_effect = fake_env_variables.get
        srst2.bowtie_index(["foo"])
        self.assertEqual(version_mock.call_count, 1)
        self.assertEqual(
            version_mock.call_args_list[0][0][0], ["/usr/bin/bowtie2", "--version"]
        )
        self.assertEqual(run_mock.call_count, 1)
        run_mock.assert_called_once_with(["/usr/bin/bowtie2-build", "foo", "foo"])

    @patch("srst2.logging")
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_bowtie_index_with_defaults(
        self, env_mock, path_mock, run_mock, version_mock, logging_mock
    ):
        path_mock.exists.return_value = False
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fake_env_variables = {}
        env_mock.get.side_effect = fake_env_variables.get
        srst2.bowtie_index(["foo"])
        self.assertEqual(version_mock.call_count, 1)
        self.assertEqual(version_mock.call_args_list[0][0][0], ["bowtie2", "--version"])
        self.assertEqual(run_mock.call_count, 1)
        run_mock.assert_called_once_with(["bowtie2-build", "foo", "foo"])


class TestRunBowtie(unittest.TestCase):
    @patch("srst2.logging")
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_run_bowtie_with_overide(
        self, env_mock, path_mock, run_mock, version_mock, logging_mock
    ):
        fake_env_variables = {
            "SRST2_SAMTOOLS": "/usr/bin/samtools",
            "SRST2_BOWTIE2": "/usr/bin/bowtie2",
            "SRST2_BOWTIE2_BUILD": "/usr/bin/bowtie2-build",
        }
        env_mock.get.side_effect = fake_env_variables.get
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        arg_mock = MagicMock()
        arg_mock.read_type = "foo"
        arg_mock.stop_after = False
        arg_mock.other = False
        arg_mock.threads = 1
        arg_mock.use_existing_bowtie2_sam = False
        actual_sam = srst2.run_bowtie(
            "mapping_file", "sample", ["fastq"], arg_mock, "db_name", "db_path"
        )
        self.assertEqual(actual_sam, "mapping_file.sam")
        self.assertEqual(version_mock.call_count, 2)
        self.assertEqual(
            version_mock.call_args_list[0][0][0], ["/usr/bin/bowtie2", "--version"]
        )
        self.assertEqual(version_mock.call_args_list[1][0][0], ["/usr/bin/samtools"])
        expected_bowtie2_command = [
            "/usr/bin/bowtie2",
            "-U",
            "fastq",
            "-S",
            "mapping_file.sam",
            "-foo",
            "--very-sensitive-local",
            "--no-unal",
            "-a",
            "-x",
            "db_path",
        ]
        run_mock.assert_called_once_with(expected_bowtie2_command)

    @patch("srst2.logging")
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_run_bowtie_with_defaults(
        self, env_mock, path_mock, run_mock, version_mock, logging_mock
    ):
        fake_env_variables = {}
        env_mock.get.side_effect = fake_env_variables.get
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        arg_mock = MagicMock()
        arg_mock.read_type = "foo"
        arg_mock.stop_after = False
        arg_mock.other = False
        arg_mock.threads = 1
        arg_mock.use_existing_bowtie2_sam = False
        actual_sam = srst2.run_bowtie(
            "mapping_file", "sample", ["fastq"], arg_mock, "db_name", "db_path"
        )
        self.assertEqual(actual_sam, "mapping_file.sam")
        self.assertEqual(version_mock.call_count, 2)
        self.assertEqual(version_mock.call_args_list[0][0][0], ["bowtie2", "--version"])
        self.assertEqual(version_mock.call_args_list[1][0][0], ["samtools"])
        expected_bowtie2_command = [
            "bowtie2",
            "-U",
            "fastq",
            "-S",
            "mapping_file.sam",
            "-foo",
            "--very-sensitive-local",
            "--no-unal",
            "-a",
            "-x",
            "db_path",
        ]
        run_mock.assert_called_once_with(expected_bowtie2_command)


class TestMPileup(unittest.TestCase):
    @patch("srst2.open", create=True)
    @patch("srst2.logging")
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_get_pileup_with_overides(
        self, env_mock, path_mock, run_mock, version_mock, logging_mock, open_mock
    ):
        fake_env_variables = {
            "SRST2_SAMTOOLS": "/usr/bin/samtools",
            "SRST2_BOWTIE2": "/usr/bin/bowtie2",
            "SRST2_BOWTIE2_BUILD": "/usr/bin/bowtie2-build",
        }
        env_mock.get.side_effect = fake_env_variables.get
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        arg_mock = MagicMock()
        arg_mock.mapq = 30
        arg_mock.baseq = 40
        arg_mock.samtools_args = []
        arg_mock.threads = 1
        arg_mock.keep_interim_alignment = True  # They're not actually created
        fake_file = MagicMock()
        fake_open_context = MagicMock(**{"__enter__.return_value": fake_file})
        open_mock.return_value = fake_open_context
        srst2.get_pileup(
            arg_mock,
            "mapping_file",
            "raw_bowtie_sam",
            "bowtie_sam_mod",
            "fasta",
            "pileup",
        )

        expected_samtools_view_command = [
            "/usr/bin/samtools",
            "view",
            "-b",
            "-o",
            "mapping_file.unsorted.bam",
            "-q",
            "30",
            "-S",
            "bowtie_sam_mod",
        ]
        run_mock.assert_any_call(expected_samtools_view_command)

        expected_samtools_sort_command = [
            "/usr/bin/samtools",
            "sort",
            "mapping_file.unsorted.bam",
            "mapping_file.sorted",
        ]
        run_mock.assert_any_call(expected_samtools_sort_command)

        expected_mpileup_command = [
            "/usr/bin/samtools",
            "mpileup",
            "-f",
            "fasta",
            "-Q",
            "40",
            "-q",
            "30",
            "-B",
            "mapping_file.sorted.bam",
        ]
        run_mock.assert_any_call(expected_mpileup_command, stdout=fake_file)

    @patch("srst2.open", create=True)
    @patch("srst2.logging")
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_get_pileup_with_defaults(
        self, env_mock, path_mock, run_mock, version_mock, logging_mock, open_mock
    ):
        fake_env_variables = {}
        env_mock.get.side_effect = fake_env_variables.get
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        arg_mock = MagicMock()
        arg_mock.mapq = 30
        arg_mock.baseq = 40
        arg_mock.samtools_args = []
        arg_mock.threads = 1
        arg_mock.keep_interim_alignment = True  # They're not actually created
        fake_file = MagicMock()
        fake_open_context = MagicMock(**{"__enter__.return_value": fake_file})
        open_mock.return_value = fake_open_context
        srst2.get_pileup(
            arg_mock,
            "mapping_file",
            "raw_bowtie_sam",
            "bowtie_sam_mod",
            "fasta",
            "pileup",
        )

        expected_samtools_view_command = [
            "samtools",
            "view",
            "-b",
            "-o",
            "mapping_file.unsorted.bam",
            "-q",
            "30",
            "-S",
            "bowtie_sam_mod",
        ]
        run_mock.assert_any_call(expected_samtools_view_command)

        expected_samtools_sort_command = [
            "samtools",
            "sort",
            "mapping_file.unsorted.bam",
            "mapping_file.sorted",
        ]
        run_mock.assert_any_call(expected_samtools_sort_command)

        expected_mpileup_command = [
            "samtools",
            "mpileup",
            "-f",
            "fasta",
            "-Q",
            "40",
            "-q",
            "30",
            "-B",
            "mapping_file.sorted.bam",
        ]
        run_mock.assert_any_call(expected_mpileup_command, stdout=fake_file)


class TestSamtoolsIndex(unittest.TestCase):
    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_samtools_index_with_overides(
        self, env_mock, path_mock, run_mock, version_mock
    ):
        fake_env_variables = {"SRST2_SAMTOOLS": "/usr/bin/samtools"}
        path_mock.exists.return_value = False
        env_mock.get.side_effect = fake_env_variables.get
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fai_file = srst2.samtools_index("fasta")

        self.assertEqual(version_mock.call_count, 1)
        self.assertEqual(version_mock.call_args_list[0][0][0], ["/usr/bin/samtools"])
        expected_samtools_command = ["/usr/bin/samtools", "faidx", "fasta"]
        run_mock.assert_called_once_with(expected_samtools_command)

    @patch("srst2.require_min_version")
    @patch("srst2.run_command")
    @patch("srst2.os.path")
    @patch("srst2.os.environ")
    def test_samtools_index_with_defaults(
        self, env_mock, path_mock, run_mock, version_mock
    ):
        fake_env_variables = {}
        path_mock.exists.return_value = False
        env_mock.get.side_effect = fake_env_variables.get
        path_mock.isfile.side_effect = lambda f: "missing" not in f
        fai_file = srst2.samtools_index("fasta")

        self.assertEqual(version_mock.call_count, 1)
        self.assertEqual(version_mock.call_args_list[0][0][0], ["samtools"])
        expected_samtools_command = ["samtools", "faidx", "fasta"]
        run_mock.assert_called_once_with(expected_samtools_command)


class TestReadPileupData(unittest.TestCase):
    def test_multidigit_indel_not_miscounted(self):
        # Regression test for issue #44: an mpileup indel length can be multiple
        # digits (e.g. +12ACGT...). The parser must consume ALL digits after
        # +/- and skip that many bases; otherwise the inserted bases are
        # mis-counted as SNPs and corrupt the consensus.
        #
        # Position 2 (ref C) has one read matching the reference plus a 12 bp
        # insertion (.+12GGGGGGGGGGGG). The consensus base there must stay the
        # reference C. The old single-digit parse read int("1"), advanced 3, and
        # counted the twelve Gs as SNPs, flipping the consensus base to G
        # (consensus "AGG" instead of "ACG").
        pileup_lines = [
            "testallele\t1\tA\t1\t.\tI",
            "testallele\t2\tC\t1\t.+12GGGGGGGGGGGG\tI",
            "testallele\t3\tG\t1\t.\tI",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            pileup_path = os.path.join(tmp, "test__sampleX.testdb.pileup")
            with open(pileup_path, "w") as fh:
                fh.write("\n".join(pileup_lines) + "\n")
            consensus_path = os.path.join(tmp, "out.all_consensus_alleles.fasta")

            srst2.read_pileup_data(
                pileup_path,
                {"testallele": 3},
                0.01,
                consensus_file=consensus_path,
            )

            with open(consensus_path) as fh:
                lines = fh.read().splitlines()

        # lines[0] is the FASTA header, lines[1] the consensus sequence.
        self.assertEqual(lines[1], "ACG")


class TestParseScoresTies(unittest.TestCase):
    # Regression tests for issue #46: all alleles tied at the top score must be
    # reported (deterministically), not a single arbitrary winner decided by
    # dict iteration order.
    def _args(self, **overrides):
        import types

        defaults = dict(
            min_coverage=90,
            min_edge_depth=2,
            min_depth=5,
            mlst_delimiter="-",
            max_divergence=10,
            truncation_score_tolerance=0.1,
            report_new_consensus=False,
            report_all_consensus=False,
            prob_err=0.01,
            output="out",
        )
        defaults.update(overrides)
        return types.SimpleNamespace(**defaults)

    def _hashes(self, alleles, size=100, depth=50):
        return dict(
            hash_edge_depth={a: (depth, depth) for a in alleles},
            avg_depth_allele={a: depth for a in alleles},
            coverage_allele={a: 100.0 for a in alleles},
            mismatch_allele={a: 0 for a in alleles},
            indel_allele={a: 0 for a in alleles},
            missing_allele={a: 0 for a in alleles},
            size_allele={a: size for a in alleles},
            next_to_del_depth_allele={a: "NA" for a in alleles},
        )

    def _run(self, scores):
        alleles = list(scores)
        h = self._hashes(alleles)
        return srst2.parse_scores(
            "genes",
            self._args(),
            scores,
            h["hash_edge_depth"],
            h["avg_depth_allele"],
            h["coverage_allele"],
            h["mismatch_allele"],
            h["indel_allele"],
            h["missing_allele"],
            h["size_allele"],
            h["next_to_del_depth_allele"],
            True,  # unique_cluster_symbols
            True,  # unique_allele_symbols
            "",  # pileup_file (consensus reporting off)
        )

    def test_all_tied_top_alleles_reported(self):
        # Two alleles in the same cluster (500) with identical scores: BOTH must
        # be reported, ordered deterministically by allele name.
        a1 = "500__geneT__alleleA__7001"
        a2 = "500__geneT__alleleB__7002"
        results = self._run({a2: -10.0, a1: -10.0})  # insertion order reversed
        self.assertIn("500", results)
        reported = [call[0] for call in results["500"]]
        self.assertEqual(reported, [a1, a2])

    def test_single_top_allele_only_one_reported(self):
        # A clear single winner (smaller score is better) is reported alone.
        a1 = "500__geneT__alleleA__7001"
        a2 = "500__geneT__alleleB__7002"
        results = self._run({a1: -10.0, a2: -5.0})
        reported = [call[0] for call in results["500"]]
        self.assertEqual(reported, [a1])


if __name__ == "__main__":
    unittest.main()
