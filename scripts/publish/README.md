Publish helper scripts

Files:

- `prepare_zenodo_package.sh` — creates a zip of launch materials, research docs, data, and analysis scripts. Run with `./scripts/publish/prepare_zenodo_package.sh /tmp/luminai-genesis-zenodo.zip`.
- `upload_to_zenodo.py` — uploads the prepared zip to Zenodo. Requires `ZENODO_TOKEN` env var.
- `zenodo_description.md` — default description used when creating the deposition.

Example workflow:

```bash
# create package
./scripts/publish/prepare_zenodo_package.sh /tmp/luminai-genesis-zenodo.zip

# set your Zenodo token (get from your Zenodo account settings)
export ZENODO_TOKEN=abcd1234

# upload (sandbox recommended for testing)
python3 scripts/publish/upload_to_zenodo.py --file /tmp/luminai-genesis-zenodo.zip --title "LuminAI Genesis: Witness dataset + analysis" --description-file scripts/publish/zenodo_description.md --sandbox

# After upload, visit the deposition in Zenodo, review metadata/files, and click Publish to obtain a DOI.
```
