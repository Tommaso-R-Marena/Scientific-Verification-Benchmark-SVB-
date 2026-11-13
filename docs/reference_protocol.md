# Reference-answer protocol, SVB 0.1.0

This is an authored, internally reviewed research pilot. Model subagents challenged labels and implementation, but their agreement is not independent empirical evidence or external expert adjudication. The term independent refers to the separation of references from evaluated PCS/FoldBounds outputs. It does not mean an independent human lab has qualified the labels.

Each task records question, target claim, assumptions, source IDs, a deterministic checker or explicit alternative-world judgment, correctness criterion, uncertainty, expected response and adjudication limitation. Six categories are allowed. In this release no item is labelled empirically_supported: archived descriptive data and model coordinates establish computational facts about supplied bytes, not population/physical validation. Formally_established denotes a complete small mathematical derivation checked by exact enumeration/arithmetic here, not a Lean proof artifact. No new machine-checked theorem is claimed.

Refuted means sufficient evidence contradicts the particular target. For M02 the target is proof validity; the true conclusion is deliberately retained. For the missing-bridge items the target is the scientific proposition's justification, not validity of an entailment. Insufficient evidence leaves the proposition unresolved; it does not say an intervention is ineffective or a model is false. U01 is an unscored open-ended research question, not a scored factual label or an assertion of documented controversy.

Reference methods:

* Exact Fraction arithmetic for finite mathematical/numerical questions, with independent Decimal checks for archived data and hand-reviewed witnesses.
* Explicit finite countermodels (quantifier swap, zero cancellation, stationary minimum, covariance).
* UCI iris.data variant: 150 rows, mean first column 1753/300 cm. The archive also includes bezdekIris.data; historical discrepancies are disclosed in iris.names. We preserve one named variant and never claim it is the exact Fisher original.
* PDB 1CRN: chain A CA atoms in deposited ATOM coordinate decimals, residues 1 and 2, squared distance 1439353/100000 angstrom squared. This does not bound coordinate measurement uncertainty or imply ligand binding. Source registry gives CC0 license policy.
* Alternative worlds exhibit a missing evidential bridge. These require scientific judgment; the checker only validates annotation consistency. It cannot mechanically adjudicate general empirical sufficiency. The observational causal example has two SCMs, one X=U,Y=X and one X=U,Y=U, with identical observations and different do(X) outcomes.
* SHA-256 checks establish byte identity relative to an admitted registry hash, never truth of measurements. Structured input checks reject duplicate keys and nonstandard NaN.

Before core baseline scoring, correct known split overlaps, run reference tests, write the protocol and freeze tasks, source bytes, registry, protocol and evaluator code hashes. Do not regenerate authoring inputs during evaluation. Semantic label mutation must be rejected independently of hashes. Corruption must fail source admission. Whole checker/reasoning annotations can still share a human conceptual mistake: external domain review remains necessary.

Development/evaluation grouping uses family IDs and checks exact duplicates. Known nM/uM and two-state pairs are grouped entirely in development after review. This is not a proof of absence of semantic leakage; the evaluation remains public and author-designed. There is no hidden set, blind adjudication, training experiment, or credible population-sampling model.

Malformed submission fails admission as a whole (CLI exit 2). Missing, unsupported and execution_error remain separate rows in all-task denominators; they are never silently dropped. Probability vectors are six-class finite normalized distributions with an argmax-consistent label. Explanations are inert data and are not graded for free-text reasoning quality. Scope claims outside the declared justified scope count separately even if a categorical label happens to match. This is a deliberately coarse annotation scheme, not automated proof of scope.

Core labels were fixed before first baseline run. Adapter protocols are separate, capability-specific and exploratory. In PCS an initial negative-control expectation was found incorrect after execution; original protocol/result are retained with reference_error, excluded from eligible-system denominator and reported explicitly. This qualification prevents presenting the PCS experiment as untouched preregistration.
