import os
import numbers
from widgetware_sdr import context_builder

EXPECTED_ACCOUNT = context_builder.load_yaml_config(
    os.path.join('.', 'tests', 'scenarios', 'qualified_account.yaml')
)
EXPECTED_OBJECTIVE = "test"
ACTUAL_CONTEXT = context_builder.build_context(
    account=EXPECTED_ACCOUNT, 
    objective=EXPECTED_OBJECTIVE, 
    evidence=[], 
    state=None
)


def test_input_parameters() -> None:
    assert ACTUAL_CONTEXT['task_context']['objective'] == EXPECTED_OBJECTIVE
    assert ACTUAL_CONTEXT['task_context']['account']['company_name'] == EXPECTED_ACCOUNT['company_name']
    assert len(ACTUAL_CONTEXT['task_context']['account']['buying_signals']) == len(EXPECTED_ACCOUNT['buying_signals'])
    assert ACTUAL_CONTEXT['state']=={}


def test_three_yaml_files() -> None:
    assert ACTUAL_CONTEXT['business_context']['products'] is not None
    assert ACTUAL_CONTEXT['business_context']['icp'] is not None
    assert ACTUAL_CONTEXT['business_context']['policies'] is not None


def test_top_level_keys() -> None:
    assert ACTUAL_CONTEXT['system_instructions'] is not None
    assert ACTUAL_CONTEXT['business_context'] is not None
    assert ACTUAL_CONTEXT['task_context'] is not None
    assert ACTUAL_CONTEXT['retrieved_evidence'] == []
    assert ACTUAL_CONTEXT['state'] == {}


def test_employee_threshold_is_numeric() -> None:
    assert isinstance(ACTUAL_CONTEXT['task_context']['account']['employee_count'], numbers.Number)


def test_evidence_categories() -> None:
    actual_evidence_categories = ACTUAL_CONTEXT['business_context']['policies']['evidence_categories']
    assert len(actual_evidence_categories) == 5
    assert 'verified_fact' in actual_evidence_categories
    assert 'derived_fact' in actual_evidence_categories
    assert 'inference' in actual_evidence_categories
    assert 'unknown' in actual_evidence_categories
    assert 'conflict' in actual_evidence_categories


def test_message_sending_is_prohibited() -> None:
    actual_prohibited_actions = ACTUAL_CONTEXT['business_context']['policies']['prohibited_actions']
    assert 'send_email' in actual_prohibited_actions
    assert 'send_social_message' in actual_prohibited_actions


def test_crm_modifications_are_prohibited() -> None:
    assert 'modify_crm' in ACTUAL_CONTEXT['business_context']['policies']['prohibited_actions']


def test_outreach_requires_human_approval() -> None:
    actual_requires_human_approval = ACTUAL_CONTEXT['business_context']['policies']['requires_human_approval']
    assert 'external_outreach' in actual_requires_human_approval
    assert 'pricing_statement' in actual_requires_human_approval
    assert 'contractual_statement' in actual_requires_human_approval

