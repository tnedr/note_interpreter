"""
USAGE: Advanced Output Validation for Prompt Lab

validate_output(
    output: dict,
    expected: dict,
    strict: bool = False,
    partial: bool = False,
    ignore_fields: list = None,
    type_check: bool = False,
    custom_comparators: dict = None
) -> dict

Parameters:
- output: dict – The actual output to validate.
- expected: dict – The expected output (fields and values).
- strict: bool – If True, unexpected fields in output will cause failure.
- partial: bool – If True, only check that expected fields are present and match; extra fields and mismatches are ignored.
- ignore_fields: list – List of field names to ignore during validation.
- type_check: bool – If True, also check that types match for each field.
- custom_comparators: dict – Dict of field names to custom comparison functions: func(actual, expected) -> bool.

Returns:
- dict with keys: status, missing_fields, mismatches, unexpected_fields, full_match

Example:
validate_output(
    output={"clarity_score": 55, "clarification_question": "Mit kérdezel?"},
    expected={"clarity_score": 60, "clarification_question": "Mit kérdezel?"},
    strict=True,
    partial=False,
    ignore_fields=["clarification_question"],
    type_check=True,
    custom_comparators={"clarity_score": lambda a, e: abs(a-e) <= 10}
)

Future: ValidationProfile support (YAML-serializable rule set)
"""
import json

def validate_output(
    output: dict,
    expected: dict,
    strict=False,
    partial=False,
    ignore_fields=None,
    type_check=False,
    custom_comparators=None
) -> dict:
    """
    Rugalmas dict összehasonlító, részleges egyezés, típusellenőrzés, ignore lista, custom comparator támogatással.
    """
    ignore_fields = ignore_fields or []
    custom_comparators = custom_comparators or {}
    missing_fields = []
    mismatches = []
    unexpected_fields = []
    for key, exp_val in expected.items():
        if key in ignore_fields:
            continue
        if key not in output:
            missing_fields.append(key)
        else:
            actual = output[key]
            # Custom comparator
            if key in custom_comparators:
                if not custom_comparators[key](actual, exp_val):
                    mismatches.append({"field": key, "expected": exp_val, "actual": actual, "reason": "custom comparator failed"})
            # Type check
            elif type_check and type(actual) != type(exp_val):
                mismatches.append({"field": key, "expected_type": type(exp_val).__name__, "actual_type": type(actual).__name__})
            # Value check
            elif actual != exp_val and not partial:
                mismatches.append({"field": key, "expected": exp_val, "actual": actual})
    if strict:
        for key in output:
            if key not in expected and key not in ignore_fields:
                unexpected_fields.append(key)
    full_match = not missing_fields and not mismatches and (not unexpected_fields if strict else True)
    return {
        "status": "passed" if full_match else "failed",
        "missing_fields": missing_fields,
        "mismatches": mismatches,
        "unexpected_fields": unexpected_fields,
        "full_match": full_match
    }

def validate_llm_reply(reply: dict, expected_fields: dict, strict=False, **kwargs) -> dict:
    """
    Validate a raw LLM reply (e.g., OpenAI JSON). Checks for 'choices', extracts content, parses as JSON, then calls validate_output.
    Returns a dict with status, text_output, parsed_output, parsing_error, output_validation.
    Extra kwargs are passed to validate_output.
    """
    text_output = None
    parsed_output = None
    parsing_error = None
    output_validation = None
    # Check for choices
    if not isinstance(reply, dict) or "choices" not in reply or not reply["choices"]:
        return {
            "status": "failed",
            "text_output": None,
            "parsed_output": None,
            "parsing_error": "Missing or empty 'choices' in reply",
            "output_validation": None
        }
    # Extract content
    try:
        text_output = reply["choices"][0]["message"]["content"]
    except Exception as e:
        return {
            "status": "failed",
            "text_output": None,
            "parsed_output": None,
            "parsing_error": f"Failed to extract content: {e}",
            "output_validation": None
        }
    # Try to parse as JSON
    try:
        parsed_output = json.loads(text_output)
    except Exception as e:
        parsing_error = f"JSON parsing error: {e}"
        return {
            "status": "failed",
            "text_output": text_output,
            "parsed_output": None,
            "parsing_error": parsing_error,
            "output_validation": None
        }
    # Validate output
    output_validation = validate_output(parsed_output, expected_fields, strict=strict, **kwargs)
    status = "passed" if output_validation["full_match"] else "failed"
    return {
        "status": status,
        "text_output": text_output,
        "parsed_output": parsed_output,
        "parsing_error": None,
        "output_validation": output_validation
    } 