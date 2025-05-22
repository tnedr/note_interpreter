import unittest
from note_interpreter.prompt_builder import PromptBuilder

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        # Minimal config (inline, nem file-ból)
        self.config = {
            "sections": [
                {"name": "intro", "enabled": True, "custom_text": "# Agent: {agent_name}\n{agent_description}"},
                {"name": "goals", "enabled": True, "custom_text": "## Goals: {goal}"},
                {"name": "output_schema_and_meanings", "enabled": True},
                {"name": "missing_section", "enabled": True}
            ]
        }
        # Register a dynamic section for testing
        @PromptBuilder.register_section('output_schema_and_meanings')
        def output_schema_and_meanings_section(params, context):
            return f"Fields: {', '.join(context.get('fields', []))}"

    def test_placeholder_substitution(self):
        context = {
            "agent_name": "TestAgent",
            "agent_description": "This is a test agent.",
            "goal": "Test goal",
            "fields": ["foo", "bar"]
        }
        # Patch config loading to use inline config
        def fake_open(*args, **kwargs):
            from io import StringIO
            import yaml
            return StringIO(yaml.dump(self.config))
        import builtins
        orig_open = builtins.open
        builtins.open = fake_open
        try:
            prompt = PromptBuilder.build(context, config_path="dummy.yaml")
        finally:
            builtins.open = orig_open
        self.assertIn("# Agent: TestAgent", prompt)
        self.assertIn("This is a test agent.", prompt)
        self.assertIn("## Goals: Test goal", prompt)
        self.assertIn("Fields: foo, bar", prompt)
        self.assertIn("[WARNING: section 'missing_section' not found in registry]", prompt)

    def test_serialize_value(self):
        self.assertEqual(PromptBuilder.serialize_value([1,2]), "- 1\n- 2")
        self.assertIn('"a": 1', PromptBuilder.serialize_value({"a": 1}))
        self.assertEqual(PromptBuilder.serialize_value(None), "(none)")
        self.assertEqual(PromptBuilder.serialize_value("x"), "x")

if __name__ == "__main__":
    unittest.main() 