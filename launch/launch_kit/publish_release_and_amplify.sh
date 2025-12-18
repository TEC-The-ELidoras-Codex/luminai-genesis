#!/usr/bin/env bash
# Helper script: steps to publish GitHub Release and amplify the launch
# Requires: `gh` (GitHub CLI) installed and authenticated for automatic release; optionally `python3` and network for Zenodo check

set -euo pipefail

RELEASE_TAG=${1:-v1.0.0-RIOT}
RELEASE_TITLE="TGCR / TECR release"
ASSET_TARBALL="dist/tgcr_release_20251216.tar.gz"
RELEASE_NOTES="papers/tgcr/RELEASE_NOTE.md"

echo "Step 1: Ensure branch 'release/prepare-zenodo' contains the final assets and release notes."
echo "Step 2: Create a GitHub Release (this will publish the tag)."
echo "If you want to use the GitHub CLI, run (example):"
echo "  gh release create ${RELEASE_TAG} ${ASSET_TARBALL} --title \"${RELEASE_TITLE}\" --notes-file ${RELEASE_NOTES}"

echo
echo "If you do NOT have gh or prefer to publish via the web:"
echo "  - Go to https://github.com/<owner>/<repo>/releases/new"
echo "  - Enter tag: ${RELEASE_TAG}, upload the tarball and attach 'tgcr.pdf' and other artifacts, paste release notes from ${RELEASE_NOTES}, then click 'Publish release'."

echo
echo "Step 3: Wait for Zenodo to archive the GitHub release and mint a DOI (if you have Zenodo linked to GitHub)."
echo "You can monitor or run the repo script to check for the DOI (this script expects the existing Zenodo check script):"
echo "  python3 scripts/check_zenodo_and_update.py"

echo
echo "Step 4: Once Zenodo mints a DOI, update all placeholders in launch assets. To automatically inject a detected DOI into the launch drafts, run the Zenodo check script and then replace [ZENODO_DOI] in files if the script outputs a DOI. Example manual replacement command:" 
echo "  DOI=doi:10.1234/zenodo.xxxxxx"
echo "  sed -i "s|\[ZENODO_DOI\]|$DOI|g" launch/launch_kit/*.md"

echo
echo "Step 5: Publish social & press assets. Recommended order:"
echo "  1) Policy partners / institutional briefings under embargo (AI Now, PAI)"
echo "  2) Tech scoop (TechCrunch) / industry reporters"
echo "  3) Public outlets (LinkedIn, Reddit, NPR public pitch) once DOI and press brief are in place"

echo
echo "Safety/legal note: Use conservative, evidence‑based language. Refer to cases as 'alleged' and cite the OSF DOI and Zenodo DOI for archival materials."

echo "Done. If you want, run the gh command above to publish the release now (requires auth)."
