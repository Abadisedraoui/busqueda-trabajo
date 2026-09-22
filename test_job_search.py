import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_all_companies as m


class JobSearchTests(unittest.TestCase):
    def test_title_variants(self):
        positives = [
            "Product Designer", "Senior Product Designer", "UX Designer", "UI Designer",
            "UX/UI Designer", "UI/UX Designer", "Web Designer", "Visual Designer",
            "Digital Designer", "User Experience Designer", "Interaction Designer",
            "Design Systems Designer", "Diseñadora UX", "Diseñador Web",
        ]
        for title in positives:
            self.assertTrue(m.is_design_title(title), title)

    def test_non_digital_false_positives(self):
        for title in ["Product Design Engineer", "Industrial Designer", "Mechanical Product Design Engineer", "Interior Designer"]:
            self.assertFalse(m.is_design_title(title), title)

    def test_canonical_url_keeps_job_identity(self):
        url = "https://example.com/jobs?jobId=123&utm_source=linkedin&source=foo"
        self.assertEqual(m.canonicalize_url(url), "https://example.com/jobs?jobId=123")

    def test_custom_domain_ats_detection(self):
        html = '<script src="https://cdn.teamtailor.com/app.js"></script>'
        self.assertEqual(m.detect_platform_from_html(html, "https://careers.example.com"), "teamtailor")

    def test_jsonld_and_job_links(self):
        payload = {
            "@context": "https://schema.org",
            "@type": "JobPosting",
            "title": "UX Designer",
            "url": "https://example.com/jobs/ux-designer",
            "description": "A" * 150,
        }
        html = f'<script type="application/ld+json">{json.dumps(payload)}</script><a href="/jobs/backend-engineer">Backend Engineer</a>'
        jobs = m.generic_jobs_from_html("Example", html, "https://example.com/careers")
        self.assertEqual({j.title for j in jobs}, {"UX Designer", "Backend Engineer"})

    def test_content_fingerprint_deduplicates_requisitions(self):
        desc = "Product design role with research, systems and collaboration. " * 5
        a = m.Job("Acme", "Product Designer", "https://jobs.test/a", "ashby", "Remote", desc, "A")
        b = m.Job("Acme", "Product Designer", "https://jobs.test/b", "ashby", "Remote", desc, "B")
        self.assertNotEqual(a.signature, b.signature)
        self.assertEqual(a.content_fingerprint, b.content_fingerprint)

    def test_session_builds(self):
        session = m.build_session()
        try:
            self.assertIsNotNone(session)
        finally:
            session.close()


if __name__ == "__main__":
    unittest.main()
