/- Independent scope policy, no PCS imports. This is an elementary typed-inference
   invariant, not a theorem about interpretation, measurements or Python. -/
inductive Scope where
  | mathematical | binding | scientific

inductive Authorized (mathChecked bindingChecked empiricalAdmitted : Bool) : Scope → Prop where
  | mathematical (h : mathChecked = true) : Authorized mathChecked bindingChecked empiricalAdmitted .mathematical
  | binding (h : bindingChecked = true) : Authorized mathChecked bindingChecked empiricalAdmitted .binding
  | scientific (h : empiricalAdmitted = true) : Authorized mathChecked bindingChecked empiricalAdmitted .scientific

theorem scientific_requires_admission {m b e : Bool}
    (h : Authorized m b e .scientific) : e = true := by
  cases h with
  | scientific h => exact h

theorem computation_cannot_escalate (m b : Bool) :
    ¬ Authorized m b false .scientific := by
  intro h
  have impossible := scientific_requires_admission h
  cases impossible
#print axioms scientific_requires_admission
#print axioms computation_cannot_escalate
