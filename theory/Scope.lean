/- Independent SVB elementary closure theorem. No subject imports or Mathlib.
   It states only a conditional syntactic invariant, not empirical soundness. -/
universe u
namespace SVB
variable {K : Type u}
inductive Justified (seed : K → Prop) (rule : K → K → Prop) : K → Prop where
  | source {k} : seed k → Justified seed rule k
  | applyRule {a b} : Justified seed rule a → rule a b → Justified seed rule b

theorem scope_preservation {seed allowed : K → Prop} {rule : K → K → Prop}
    (hseed : ∀ k, seed k → allowed k)
    (hrule : ∀ a b, allowed a → rule a b → allowed b)
    {k : K} (h : Justified seed rule k) : allowed k := by
  induction h with
  | source hs => exact hseed _ hs
  | applyRule _ hr ih => exact hrule _ _ ih hr

-- Excluding empirical evidence from source and rule closure excludes its derivation.
theorem excluded_type {seed allowed : K → Prop} {rule : K → K → Prop}
    (hseed : ∀ k, seed k → allowed k)
    (hrule : ∀ a b, allowed a → rule a b → allowed b)
    {empirical : K} (excluded : ¬ allowed empirical) :
    ¬ Justified seed rule empirical := by
  intro proof
  exact excluded (scope_preservation hseed hrule proof)
#print axioms scope_preservation
#print axioms excluded_type
end SVB
