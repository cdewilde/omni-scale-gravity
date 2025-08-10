# GitHub Launch Checklist — OmniScale Gravity (OSG)

**Date:** 2025-08-10

1) **Create repo**: `omni-scale-gravity` (public), initialize with README.
2) **License**: add MIT (code) + CC BY 4.0 (text/figures). Replace placeholders.
3) **CITATION**: verify `CITATION.cff` (names, year).
4) **CI**: ensure `.github/workflows/ci.yml` present; protect `main`.
5) **Push**:
   ```bash
   git init
   git add .
   git commit -m "OSG v1b: PN seeding + GPU N-body + CI"
   git branch -M main
   git remote add origin <YOUR_URL>
   git push -u origin main
   git tag v1b && git push origin v1b
   ```
6) **Release assets**: attach teasers/explainer PDFs, preprint build, and (optional) microsite zip.
7) **Repro**: notebooks run top-to-bottom; consider Zenodo DOI.
