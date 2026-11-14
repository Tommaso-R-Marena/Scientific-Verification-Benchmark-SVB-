# Repository delivery and reproduction

The user supplied and authorized uploading this project to:

https://github.com/Tommaso-R-Marena/Scientific-Verification-Benchmark-SVB-

The destination is public. Its existing initial Apache-2.0 license commit is preserved through a merge with the independent project's history; no force push or history replacement is needed. The destination's original LICENSE file is retained. The draft manuscript and reports retain their pilot limitations, reference-error disclosure and lack of external expert qualification. Repository availability is not publication of a peer-reviewed scientific result or evidence of general AI reliability.

## Delivery history

The initial attempt to create a private repository through the integration failed with `Resource not accessible by integration` for `createRepository`. All work was committed locally. The user subsequently created the destination above and explicitly requested uploading the project there. The earlier creation failure recorded in the historical evidence ledger describes that initial attempt, not the current delivery destination.

Only committed project artifacts are uploaded. `results/local/` remains excluded: it contains raw adapter logs, temporary reproduction checkouts and local subject fingerprints. No credentials, private subject source code, signed subject-fixture copies or private datasets are included. The capability assessment references inspected subject paths and commits, and the retained system results contain sanitized measurements and source identities. The three subject repositories are not edited or pushed.

## Reproduce from GitHub

```sh
git clone https://github.com/Tommaso-R-Marena/Scientific-Verification-Benchmark-SVB-.git
cd Scientific-Verification-Benchmark-SVB-
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -m svb.cli validate
python3 -m unittest discover -s tests -v
python3 -m svb.cli experiment --output results/local/my-run
```

Python 3.12.14 was used for the retained measurements. The core requires no external Python package or subject checkout. Optional subject adapters require separately authorized checkouts and the existing compiled PCS authority. See the README and system evaluation report for their exact scope.

The standalone GitHub Actions workflow is manual-dispatch only. An initial push does not request a hosted test run. Local tests and reproduction artifacts are the validation evidence; no hosted CI execution is claimed.
