# Private repository publication steps

The project is fully implemented and committed locally on main. The available GitHub integration authenticated successfully for reads but rejected `createRepository` with `Resource not accessible by integration`. No remote repository was created or pushed. This is an integration permission limitation, not missing local work. Do not grant broader access or send credentials in chat to work around it.

To publish privately using your own authorized GitHub session:

1. Create an **empty private** `Tommaso-R-Marena/scientific-verification-benchmark` repository in GitHub. Do not initialize a README/license or grant collaborators access yet.
2. From the existing independent checkout, run:

```sh
cd /workspace/scientific-verification-benchmark
git status --short
git remote add origin https://github.com/Tommaso-R-Marena/scientific-verification-benchmark.git
git push -u origin main
```

Alternatively, in a separately authenticated GitHub CLI session with permission to create private repositories:

```sh
cd /workspace/scientific-verification-benchmark
gh repo create Tommaso-R-Marena/scientific-verification-benchmark --private --source . --remote origin --push
```

Choose one route; preserve any already-created remote rather than overwriting it. Do not run these commands against any of the three subject repositories. The standalone CI workflow is manual-dispatch only; a push does not automatically consume hosted build minutes. Local test results are evidence; a hosted CI execution is not claimed.

Before any future **public** release, arrange external adjudication, review subject capability-assessment confidentiality, verify dataset attribution and complete a scientific claims review. The manuscript is a draft, and this session does not authorize publishing a paper or public scientific claim on the user's behalf.

`results/local/` is intentionally excluded: it contains raw adapter logs and local subject fingerprints. All files necessary for the dependency-free independent core and its recorded numerical results are tracked. Optional subject adapters require separately authorized checkouts and do not bundle private subject code.
