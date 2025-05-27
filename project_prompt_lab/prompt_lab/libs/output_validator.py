import json

def validate_output(output: dict, expected: dict, strict=False) -> dict:
    """
    Compare output dict to expected dict. Report missing fields, mismatches, and (if strict) unexpected fields.
    Returns a dict with status, missing_fields, mismatches, unexpected_fields, full_match.
    """
    missing_fields = []
    mismatches = []
    unexpected_fields = []
    for key, exp_val in expected.items():
        if key not in output:
            missing_fields.append(key)
        elif output[key] != exp_val:
            mismatches.append({"field": key, "expected": exp_val, "actual": output[key]})
    if strict:
        for key in output:
            if key not in expected:
                unexpected_fields.append(key)
    full_match = not missing_fields and not mismatches and (not unexpected_fields if strict else True)
    return {
        "status": "passed" if full_match else "failed",
        "missing_fields": missing_fields,
        "mismatches": mismatches,
        "unexpected_fields": unexpected_fields,
        "full_match": full_match
    }

def validate_llm_reply(reply: dict, expected_fields: dict, strict=False) -> dict:
    """
    Validate a raw LLM reply (e.g., OpenAI JSON). Checks for 'choices', extracts content, parses as JSON, then calls validate_output.
    Returns a dict with status, text_output, parsed_output, parsing_error, output_validation.
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
    output_validation = validate_output(parsed_output, expected_fields, strict=strict)
    status = "passed" if output_validation["full_match"] else "failed"
    return {
        "status": status,
        "text_output": text_output,
        "parsed_output": parsed_output,
        "parsing_error": None,
        "output_validation": output_validation
    } 