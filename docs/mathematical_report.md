# Scope-preserving justification: definitions, proofs, and limits

This report gives a small mathematical specification for evaluating verification
claims. The results below have complete written proofs, conditional on their stated
assumptions. A narrower unary rule-closure result has additionally been checked by
Lean 4.28.0, as described in Section 9; the general multi-premise DAG soundness
argument and probability calculations are written proofs, not machine-checked
results. These are familiar consequences of typed inference and probability
theory; SVB claims no new theorem.

## 1. Judgments are typed, not arranged on a strength ladder

Let a scientific claim be a tuple `(p, τ, A, M, D, I)`: proposition `p`,
justification type `τ`, explicit assumptions `A`, model `M`, evidence/data identity
`D`, and intended interpretation/application scope `I`. Types include logical,
computational, numerical, statistical, model-adequacy, empirical, provenance, and
epistemic-sufficiency judgments. These are distinct sorts. There is no default
ordering in which a computational certificate is automatically below an empirical
certificate and can be promoted by accumulating more computation.

For example, `P(contact≥1 | finite HP lattice model)=4/11` and `this protein
has the corresponding experimental population` are different propositions with
different models and applicability scopes. A proof of the first is not a proof
of the second. A sample mean, a causal effect, an observed association, and a
population parameter likewise cannot be substituted for one another.

A judgment `Γ ⊢ (τ,p)` means that an admitted derivation supports `p` at type `τ`
under assumptions/evidence `Γ`. It does not mean that all premises in `Γ` are true
in the physical world. Distinct source identities and model assumptions must be
retained as part of the judgment; a hash identifies bytes and does not certify
their scientific authenticity.

## 2. Typed dependency graphs

A justification DAG is a finite directed acyclic graph. Each node is either an
admitted premise or an inference-rule application, and carries a complete typed
judgment. Rule schemas declare their premise and conclusion types, proposition
conditions, assumptions, data identities, and scope. A rule may be used only when
all its conditions have been established. Renaming a conclusion's type is not an
inference rule.

An ordinary rule preserves an existing premise type (for every instantiation its
conclusion type equals the type of at least one premise). A bridge rule may
introduce a distinct type. An example of a possible bridge is an independently
reviewed calibration/validation study connecting predictions from a particular
model and parameter range to an experimentally measured quantity in a stated
population. Declaring such a bridge is not establishing its soundness; validating
it remains a scientific task. A nullary ordinary rule is disallowed. Any nullary
rule must be separately admitted as a premise, preventing a hidden source of
empirical evidence.

The minimal executable policy need not inspect arbitrary natural-language proofs.
It can reject a *declared* inference whose required evidence types are absent.
This catches missing evidence only to the extent that evidence types and claims
were represented faithfully. It does not solve extraction, fabrication detection,
model adequacy, causal identification, or scientific interpretation in general.

## 3. Scope non-escalation theorem

**Theorem (type-source closure).** Let `S` be a set of types. Consider a finite
justification DAG in which (i) every admitted premise has type in `S`, (ii) each
ordinary rule's conclusion type equals one of its premise types, and (iii) every
admitted bridge has its conclusion type in `S`. Then every derived node has type
in `S`.

**Proof.** Choose a topological ordering of the finite DAG. Proceed by induction
over this ordering. A premise node has type in `S` by (i). At an ordinary-rule
node, every premise occurs earlier and thus has type in `S` by the induction
hypothesis. Its conclusion type equals a premise type by (ii), hence is in `S`.
At a bridge-rule node, its conclusion type is in `S` by (iii). These exhaust the
node forms, so all nodes have type in `S`. ∎

**Corollary.** If no admitted premise has empirical type and no admitted bridge
has empirical conclusion type, no derivation in this calculus yields an empirical
judgment, however many mathematical or computational nodes it contains.

This is a syntactic closure result. It says nothing about whether a forged node
was admitted incorrectly, a rule schema was scientifically appropriate, a
software parser matched the calculus, or the declarations describe the actual
calculation. An implementation needs its own correspondence argument.

## 4. Conditional soundness of composition

Choose a semantics assigning each typed proposition a truth condition. For a
fixed interpretation of all models, assumptions, source identities, and scopes,
assume (i) every admitted premise is true and (ii) every instantiated admitted rule
preserves truth from all its premises to its conclusion.

**Theorem (conditional DAG soundness).** Every conclusion of a finite admitted
justification DAG is true in that interpretation.

**Proof.** In a topological ordering, premise nodes are true by (i). For an
inference node, all premises are true by induction; its conclusion is true by
(ii). Induction proves the claim. ∎

The difficult scientific work is often exactly premise truth and bridge-rule
soundness. The theorem does not discharge those assumptions. Treating a model
prediction as a direct experimental measurement would violate the rule-soundness
assumption rather than produce an empirical theorem for free. This is standard
compositional proof reasoning, not a general solution to scientific verification.

## 5. Two countermodels separate invalid reasoning from false claims

1. The proposition `∀x∈ℝ, x²≥0` is true. The supplied argument “because every
   real number is nonnegative” is invalid: its premise fails at `x=-1`. A response
   may reject the justification while retaining the theorem with a valid proof
   (e.g. ordered-field square nonnegativity). A single `valid/invalid` bit would
   conflate these two judgments.
2. Suppose `Y=X` is observed. Model A has `X=U, Y=X`, while model B has
   `X=U, Y=U`, with nondegenerate unobserved `U`. They generate the same
   observational distribution. Under `do(X=x)`, model A has `Y=x` whereas model B
   retains `Y=U`. Thus observations alone do not identify the causal effect for
   this model class. The appropriate reference label is insufficient evidence
   for the causal claim, not proof that the effect is zero. The claim is compatible
   with one model and incompatible with the other.

These examples establish logical distinctions. Their presence in a benchmark
does not establish their prevalence in deployed systems.

## 6. Uncertainty requires dependence information

For square-integrable random variables,

`Var(X+Y) = Var(X)+Var(Y)+2 Cov(X,Y)`.

To verify it, write `X'=X-E[X]` and `Y'=Y-E[Y]`; expand
`E[(X'+Y')²]` and use linearity of expectation. Replacing this expression with
the sum of variances needs zero covariance. Independence is sufficient but is
not necessary.

Take a symmetric Rademacher variable `Z` (`P(Z=1)=P(Z=-1)=1/2`). If `X=Y=Z`,
each variance is 1, yet the sum variance is 4 rather than 2. If `X=Z, Y=-Z`,
it is 0 rather than 2. Marginal uncertainties alone therefore do not identify the
sum uncertainty. These examples use exact finite distributions, no numerical
approximation and no evaluated-system output.

For hard intervals, `X∈[a,b]` and `Y∈[c,d]` imply
`X+Y∈[a+c,b+d]` without independence. If the intervals instead cover random
quantities with marginal probabilities at least `1-α` and `1-β`, the joint
coverage is at least `max(0,1-α-β)` by the union bound. Multiplying coverage
probabilities requires an independence assumption; treating confidence intervals
as deterministic bounds changes the proposition.

If `f` is Lipschitz with constant `L` on the entire uncertainty domain and
`|x-x̂|≤ε`, then `|f(x)-f(x̂)|≤Lε` directly by the Lipschitz condition. This
does not include model discrepancy, parameter uncertainty, or measurement error
unless those are included explicitly in the domain/error model.

## 7. Scoring: use established rules and explicit denominators

Use a finite vector of reference categories, not a binary truth surrogate. For
probability vector `p` and one-hot reference vector `e_y`, the multiclass Brier
loss is `Σ_k(p_k-e_y,k)²`. If reference outcome distribution is `q`, its expected
loss is `Σ_k(p_k-q_k)² + 1-Σ_k q_k²`. To prove this, expand each square and use
`E[e_y,k]=q_k` and `e_y,k²=e_y,k`. The unique minimum over the probability
simplex is at `p=q`. This is a standard strictly proper scoring result.

The proof presupposes correctly adjudicated categories and a stated sampling
distribution. It does not prove that a benchmark's labels are true. Single fixed
items cannot establish calibration of a system in deployment. Probabilities that
omit categories, contain nonfinite values, or fail to sum to one are malformed,
not valid confident predictions.

Report coverage (answered/supported) and conditional risk with their denominator.
A rule that always abstains has zero answered coverage; an undefined risk at
zero coverage must remain undefined, not be displayed as zero error. “Insufficient
evidence” can be a substantive scientific answer; an unsupported adapter is a
capability outcome and must be reported separately. Failed executions belong in
the total run count. Report false acceptance of refuted/insufficient claims
separately, alongside the full confusion matrix. Severity weights and aggregation
choices are policy decisions; show sensitivity rather than asserting a unique
scientific loss function.

## 8. Open questions and nonclaims

- No proof is provided that a finite evidence-type taxonomy is complete.
- No theorem makes natural-language evidence declarations trustworthy.
- No physical applicability, protein-binding discovery, or general AI safety
  guarantee follows from these definitions.
- The implemented benchmark's soundness requires reference-oracle, serialization,
  scoring, adapter, and operating-system validation in addition to this report.
- Independent expert adjudication and an access-controlled external evaluation
  are necessary before claiming research-grade ground truth or hidden-test
  generalization. A public frozen set is not a secret held-out set.

The immediate contribution is an auditable separation of known ideas and their
assumptions. Whether this separation improves real scientific AI evaluation is an
experimental question, not a theorem asserted here.

## 9. Executed Lean check: unary scope closure only

[`theory/Scope.lean`](../theory/Scope.lean) defines `Justified seed rule k` as
the least inductive closure of a seed predicate under a *unary* binary relation
`rule : K → K → Prop`. Its two constructors admit a source or apply one rule to
one previously justified object. `K` is arbitrary; its elements can represent
types or judgments, but the file does not encode the scientific taxonomy or
natural-language claims.

`SVB.scope_preservation` states that if every seed is in `allowed` and every
rule preserves `allowed`, then every justified object is in `allowed`. The proof
uses induction on the justification derivation. `SVB.excluded_type` follows by
contradiction: an object outside `allowed` cannot be justified under those
assumptions. The file imports neither the evaluated subjects nor Mathlib.

The command

```sh
/workspace/.setup/lean/bin/lean theory/Scope.lean
```

was executed with Lean 4.28.0. The retained
[`results/lean_scope.log`](../results/lean_scope.log) reports:

```text
'SVB.scope_preservation' does not depend on any axioms
'SVB.excluded_type' does not depend on any axioms
```

These are actual Lean kernel checks under the usual trust in the installed
toolchain and host. They establish the encoded unary closure theorem, not a
verified SVB executable or an empirical scientific claim. The multi-premise
topological-induction theorems in Sections 3–4 remain complete written arguments;
this file is not a mechanization of all their premises, graph structure, rule
soundness, scientific interpretation, or evidence admission. Generalizing the
Lean representation to explicit multi-premise hyperedges and proving
implementation correspondence are future tasks. No novelty is claimed for the
unary result or the written generalization.
