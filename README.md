# Transfer Script

## Included files and usage (if applicable):
- `.env` : environment file for various database links and variables
- `ckan.sh` : bash script for running ckan commands (at http://docs.ckan.org/en/2.9/maintaining/cli.html) a little bit more easily (QoL, nondevelopmental).  Also good reference for running commands within the docker image correctly.
- `ckanAPI.py` : Helpful commandline interface for ckan API calls.  Use -h flag for information on its usage.
- `purge.py` : Python script for cleaning datasets out of the database. CKAN's built in clean wipes the whole database including users, groups, and organizations, which I think is unwanted, so this clears just the datasets and tag vocabularies in case it needs to be cleared. Boolean toggle at the top of the file to point it toward govcloud or inprem instances of CKAN.  Note that hardcoded vocabulary IDs in the backend will need to be updated after running
- `uploadScript.py` : Grabs all artifacts from the previous backend API through the ANZO link in the `.env` file.  Uploads each artifact as its own dataset.  Boolean toggle at the top of the file to point it toward govcloud or inprem instances of CKAN.  Further Boolean flags allow for directing which groups artifacts are added to in GovCloud (prod or dev)


Approved for Public Release; Distribution Unlimited. Public Release Case Number 22-3969

The author's affiliation with The MITRE Corporation is provided for identification purposes only, and is not intended to convey or imply MITRE's concurrence with, or support for, the positions, opinions, or viewpoints expressed by the author. ©2022 The MITRE Corporation. ALL RIGHTS RESERVED.