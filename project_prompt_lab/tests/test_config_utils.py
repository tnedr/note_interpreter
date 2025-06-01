from prompt_lab.libs.config_utils import get_llm_model_from_config

def test_get_llm_model_from_config():
    model = get_llm_model_from_config()
    assert isinstance(model, str)
    assert model == "gpt-4.1-mini" 