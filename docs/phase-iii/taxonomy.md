# Taxonomy validity and a proposed alternative

The historical six labels are **not a mutually exclusive classification of
scientific states under their current meanings**. They mix justification type
(formal, computational, empirical), evidential verdict (refuted, insufficient)
and the social/research status of a question (disputed/unresolved). A precedence
rule could force one label, but would define an operational coding convention,
not prove that the categories form natural disjoint scientific classes. This
critique does not rewrite historical labels, qualification gates or scores.

## Counterexamples to exclusivity and completeness

| Example | Legitimately overlapping descriptions | Why the distinction matters |
|---|---|---|
| FS04N: two displayed neopentane values both equal 2.51 kcal/mol | Source-supported recorded observation, computational equality, provenance fact; deductively trivial under exact displayed-value assumptions | Rounded-field equality is not zero physical model discrepancy or universal-temperature validation |
| SL02N: every recorded pair has nonnegative difference | Empirical description of archived measurements and finite computation over the table | This excludes no future patient outcome and does not identify measurement reliability |
| A finite rational mean proved by exact arithmetic | Computationally established and formally derivable from the supplied numbers and arithmetic axioms | Computation and deduction are related methods, not exclusive epistemic outcomes |
| A certified program computes a counterexample to a claim | Correct computation/proof artifact and refutation of the target | The artifact's correctness must be separated from the target's verdict |
| An unsettled mechanism with competing studies | Documented dispute may coexist with supporting evidence, opposing evidence or insufficient evidence under a specified envelope | Dispute is not synonymous with absence of evidence; lack of evidence in one packet is not a literature-wide open question |
| An unsupported causal conclusion from correct observed growth | Computational component correct; target inference unsupported | Checking 205−42=163 does not identify the chick's no-diet counterfactual |

Refuted and insufficient can also become ambiguous if the target conflates “X
is true” with “this evidence establishes X.” Failure of a particular argument
can refute its claimed entailment without establishing the falsity of X. A
compound claim may have true, false and unassessed components. The target must
be made atomic or the ambiguity retained. Historical `disputed_or_unresolved`
also joins social disagreement and unsettled knowledge, neither universally
observable from a small evidence packet.

## Established frameworks and their limits

A targeted inspection of seven official/authoritative resources is recorded with
retrieval hashes and inspected sections in `references/phase3_registry.json`.
This is not a systematic review or independent expert validation.

| Framework | Relevant separation | Limit for SVB |
|---|---|---|
| [Lean, Axioms and Computation](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/) | Exact propositions, axioms, proof checking and computational behavior | A checked proof is conditional on its statement/axioms/trust base; it does not establish empirical adequacy |
| [Evidence and Conclusion Ontology](https://www.evidenceontology.org/) | Evidence type and assertion method, supporting biological annotation provenance | Evidence method is not an exclusive global truth label or universal strength ranking |
| [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | Entities, activities, agents and derivation/primary-source relations | Traceable origin enables examination; it does not entail validity |
| [GRADE handbook](https://gdt.gradepro.org/app/handbook/handbook.html), sections 1.2 and 5 | Outcome-specific confidence/quality of a body of evidence versus recommendation strength | Clinical effect-evidence grading should not be transferred without justification to a table lookup, proof or isolated biochemical value |
| [IPCC uncertainty guidance](https://www.ipcc.ch/site/assets/uploads/2018/05/uncertainty-guidance-note.pdf), introduction and guidance 2–6 | Evidence/agreement-based qualitative confidence versus probabilistic uncertainty; independent judgments before discussion | Reviewer agreement is not a calibrated probability of truth, and framing/anchoring can distort assessments |
| [Many-Valued Logic](https://plato.stanford.edu/entries/logic-manyvalued/), section 2.3 | Established support for representing gaps and gluts; Belnap–Dunn four-valued logic | Our two flags are a record of admitted arguments, not an implementation of the full calculus or a new theory |
| [Scientific Method](https://plato.stanford.edu/entries/scientific-method/), introduction and reasoning discussion | Deductive/inductive methods and context-sensitive scientific practice | No single method list yields a universally complete mutually exclusive taxonomy of scientific conclusions |

The existing SciFact, FEVER, attribution, scientific-agent and selective-prediction
comparisons remain in the Phase II literature review. Evidence relations,
provenance, argument structure and uncertainty already have extensive prior work.
The proposed schema makes no novelty or superiority claim.

## Proposed data/protocol 0.4.0 dimensions

`schemas/v0.4.0/evidence_assessment.schema.json` defines a candidate representation;
`svb.taxonomy.validate_assessment` checks structural and cross-field invariants.
These are author-proposed semantics for external criticism, not validated gold.

- **Target:** exact claim and explicit population/system, conditions and quantifier.
- **Evidence envelope:** supplied document identities and disclosed assumptions.
- **Evidence relation:** separate support and opposition flags, plus whether the
  relation has been assessed. Neither is distinct from not assessed.
- **Justification types:** a set of deductive, computational, observational,
  experimental, statistical and provenance methods; multiple types may apply.
- **Computational check:** outcome, method, whether a machine check was executed,
  what it establishes and what it does not establish. This describes an artifact
  or component, not automatic acceptance of the entire scientific target.
- **Empirical support:** recorded facts versus support/opposition for the target,
  with experimental design and limitations explicit.
- **Evidence strength:** named domain rubric and value, or both null. No invented
  common ordinal scale equates a proof, an assay and a clinical evidence body.
- **Uncertainty:** separate measurement, statistical, model and reviewer accounts.
  These text fields are not a new uncertainty calculus or probability vector.
  Quantitative estimates need separately justified units, interval type, method
  and coverage/credible-level interpretation before a future schema extension.
- **Missing assumptions** and **documented research dispute** remain separate.
  A documented dispute needs a supplied source; ignorance is not documentation.

Examples in `data/v0.4.0/taxonomy_examples.json` express three existing cases as
provisional illustrations. They do not create new scored items, new reviews or
replacement historical references.

## Explicit semantics and logical limits

Let a target be T=(φ,S,C,Q), comprising proposition, population/system, conditions
and quantifier, with evidence envelope E and explicit assumptions A. Let R be a
stated scientific assessment policy and let J_R(E,A,T) be the set of arguments
admitted by that policy **at that exact target scope**. Define

s(T)=1 iff an admitted argument supports φ;
o(T)=1 iff an admitted argument opposes φ.

Then assessed relation values are:

| (s,o) | Record meaning |
|---|---|
| (0,0) | Neither supporting nor opposing argument admitted within the assessed envelope |
| (1,0) | Support only |
| (0,1) | Opposition only |
| (1,1) | Both; retain incompatible/contested arguments and their assumptions |

“Unassessed” has a separate flag and cannot assert either bit. Neither is a
statement about a bounded assessment, not an omniscient proof that no evidence
exists. Both does not license explosion or assert that physical reality is
literally contradictory. In a consistent classical deductive system soundly
checking one shared premise set, both would not be admitted; scientific evidence
collections can contain contested methods, incompatible assumptions or unresolved
measurement conflict. Those differences must remain explicit.

For deductive justification, the relevant claim is A ⊢ φ under a declared proof
system and trusted checker. For an exact finite calculation it is f(x)=y for
specified x, arithmetic and implementation. For an empirical claim, admitting
support depends on measurement/design/scope judgments; a generic JSON validator
cannot supply them. In particular,

`computational_check.status = passed` **does not entail** `relation.support = true`.

No automatic scope-subsumption algorithm is implemented: scope fields are
reviewable text, not a machine-proved causal bridge. Likewise, a supplied ID or
exact quotation establishes literal consistency, not entailment or source quality.
There is no automatic aggregation of evidence strength, proof and measurement
uncertainty. The familiar four information states and typed records are not new
mathematical contributions. Adding evidence need not monotonically improve an
empirical verdict because new evidence may defeat a previously admitted argument.

## Relation to historical scoring

No invertible migration exists from a single historical label to all these
fields. Old labels lack the information needed to reconstruct scope, methods,
strength and uncertainty. No historical output is expanded into an invented
multidimensional response, and no old score is recalculated as a new primary
result. Future models would need a separately frozen task/rubric and independently
adjudicated references.

For an admitted historical prediction p and a nonempty set L of defensible
reference labels, define indicator bounds:

FA_min(p,L)=min over l in L of 1[p is accepting and l is nonaccepting];
FA_max(p,L)=max over l in L of the same indicator.

If L lies entirely within one acceptance group, both bounds coincide. Therefore
allowing computational/formal/empirical co-categories for a supported table fact
cannot by itself change historical false acceptance. If L crosses the acceptance
boundary, an accepting prediction has bounds [0,1]. An empty L is unresolved,
not a correct answer or zero-risk case. These are indicator bounds on fixed
items, not rates with arbitrarily changing denominators. Definite/ambiguous
reference strata and missing outputs should be reported before any future rate.
The implementation exhaustively tests invariance over the six-label subsets.

## What would establish an improvement

The new representation removes known category collisions **by construction**;
that is a representational benefit, not evidence that humans or models can use
it reliably. It can increase annotation burden, produce vacuous checklists,
shift ambiguity into the support policy or invite unjustified strength ratings.
The pilot should test whether domain reviewers understand the axes, preserve
scientific distinctions and finish a manageable form. Record time, unassessable
fields, alternative proposals and disagreements. No superiority conclusion can
be made before those actual observations and comparisons exist.
