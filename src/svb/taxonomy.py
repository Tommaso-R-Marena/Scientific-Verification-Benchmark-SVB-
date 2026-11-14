"""Proposed evidence dimensions, not an empirical truth oracle or new logic."""
from __future__ import annotations
from copy import deepcopy
from .core import Invalid, LABELS, ACCEPT

VERSION = '0.4.0-proposal'
KINDS = ('deductive', 'computational', 'observational', 'experimental', 'statistical', 'provenance')
FIELDS = {'schema_version', 'target', 'evidence', 'relation', 'justification_types',
          'computational_check', 'empirical_support', 'evidence_strength',
          'uncertainty', 'missing_assumptions', 'research_dispute', 'rationale'}


def obj(x, keys, name):
    if not isinstance(x, dict) or set(x) != set(keys):
        raise Invalid(name + ': exact object fields required')


def text(x, name):
    if not isinstance(x, str) or not x.strip() or len(x) > 20000:
        raise Invalid(name + ': nonempty bounded text required')


def strings(x, name, allowed=None):
    if not isinstance(x, list) or len(x) > 100 or any(not isinstance(v, str) or not v.strip() or len(v)>20000 for v in x) or len(set(x)) != len(x):
        raise Invalid(name + ': unique textual list required')
    if allowed is not None and not set(x) <= set(allowed):
        raise Invalid(name + ': unknown value')


def relation_name(relation):
    obj(relation, {'support', 'opposition', 'assessed'}, 'relation')
    if any(type(x) is not bool for x in relation.values()):
        raise Invalid('relation flags must be booleans')
    if not relation['assessed']:
        if relation['support'] or relation['opposition']:
            raise Invalid('unassessed relation cannot assert supporting/opposing argument')
        return 'unassessed'
    return {(False, False): 'neither', (True, False): 'support_only',
            (False, True): 'opposition_only', (True, True): 'both'}[(relation['support'], relation['opposition'])]


def validate_assessment(record):
    obj(record, FIELDS, 'assessment')
    if record['schema_version'] != VERSION:
        raise Invalid('wrong proposed schema version')
    target = record['target']; obj(target, {'claim', 'scope'}, 'target'); text(target['claim'], 'claim')
    obj(target['scope'], {'population_or_system', 'conditions', 'quantifier'}, 'scope')
    for x in target['scope'].values(): text(x, 'scope component')
    envelope = record['evidence']; obj(envelope, {'document_ids', 'assumptions'}, 'evidence')
    strings(envelope['document_ids'], 'document IDs'); strings(envelope['assumptions'], 'assumptions')
    relation_name(record['relation'])
    strings(record['justification_types'], 'justification types', KINDS)
    comp = record['computational_check']; obj(comp, {'status', 'method', 'machine_checked', 'establishes', 'does_not_establish'}, 'computational check')
    if comp['status'] not in ('not_checked', 'not_applicable', 'passed', 'failed') or type(comp['machine_checked']) is not bool:
        raise Invalid('invalid computational status')
    if comp['machine_checked'] and comp['status'] not in ('passed', 'failed'):
        raise Invalid('machine check must have an outcome')
    text(comp['method'], 'computational method')
    strings(comp['establishes'], 'computational scope'); strings(comp['does_not_establish'], 'computational exclusions')
    emp = record['empirical_support']; obj(emp, {'status', 'design_and_limitations'}, 'empirical support')
    if emp['status'] not in ('not_assessed', 'not_applicable', 'record_only', 'supports_target', 'opposes_target', 'mixed'):
        raise Invalid('unknown empirical status')
    text(emp['design_and_limitations'], 'empirical design')
    strength = record['evidence_strength']; obj(strength, {'rubric', 'value', 'rationale'}, 'evidence strength')
    if (strength['rubric'] is None) != (strength['value'] is None):
        raise Invalid('domain evidence rating requires both rubric and value')
    if strength['rubric'] is not None:
        text(strength['rubric'], 'strength rubric'); text(strength['value'], 'strength value')
    text(strength['rationale'], 'strength rationale')
    obj(record['uncertainty'], {'measurement', 'statistical', 'model', 'reviewer'}, 'uncertainty')
    for x in record['uncertainty'].values(): text(x, 'uncertainty component')
    strings(record['missing_assumptions'], 'missing assumptions')
    dispute = record['research_dispute']; obj(dispute, {'status', 'documentation_ids'}, 'research dispute')
    if dispute['status'] not in ('not_assessed', 'documented', 'not_documented'):
        raise Invalid('unknown dispute status')
    strings(dispute['documentation_ids'], 'dispute documentation', envelope['document_ids'])
    if dispute['status'] == 'documented' and not dispute['documentation_ids']:
        raise Invalid('documented dispute needs supplied documentation')
    text(record['rationale'], 'rationale')
    return deepcopy(record)


def false_acceptance_bounds(prediction, defensible_labels):
    """Bounds on the historical *indicator*, not a rate with a moving denominator.

    No labels is an unresolved reference, not a free pass. A missing/malformed
    prediction is outside this admitted-verdict sensitivity calculation.
    """
    if prediction not in LABELS: raise Invalid('admitted historical category required')
    strings(defensible_labels, 'defensible labels', LABELS)
    if not defensible_labels: return {'lower': None, 'upper': None, 'reference_unresolved': True}
    errors = [int(prediction in ACCEPT and label not in ACCEPT) for label in defensible_labels]
    return {'lower': min(errors), 'upper': max(errors), 'reference_unresolved': False}
