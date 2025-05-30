# megerteni a custom toolt es a @tool t
# https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/


from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Dict, List, Optional, Any, Union
import logging
from dataclasses import dataclass
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from datetime import datetime
from abc import ABC, abstractmethod
import threading
import yaml
from project_prompt_lab.prompt_lab.libs.user_output import user_print, CYAN, YELLOW, MAGENTA, BLUE, GREEN, RED, WHITE, BOLD
import json

StateType = TypeVar('StateType', bound=BaseModel)
ResponseType = TypeVar('ResponseType', bound=BaseModel)


class BaseSharedContext(BaseModel):
    """Shared context model for managing shared data."""
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def __init__(self, **data):
        super().__init__(**data)
        self._lock = threading.Lock()
        self._dynamic_fields = {}
        self._export_path = None

    def update_fields(self, debug: bool = False, **fields) -> None:
        """Update or add fields to the shared context"""
        with self._lock:
            for key, value in fields.items():
                setattr(self, key, value)
                self._dynamic_fields[key] = value
            
            # Mindig megjelenő informatív üzenet
            self.printer(f"\n✓ Shared context updated with fields: {', '.join(fields.keys())}")
            
            # Debug információk csak debug módban
            if debug:
                self.logger.debug(f"[DEBUG] Updated fields: {fields}")
                self.logger.debug(f"[DEBUG] Current dynamic fields: {self._dynamic_fields}")

    def save_context(self, system_prompt_name: str, use_case: str, llm: Any, description: str) -> str:
        """Save shared context to a YAML file"""
        # Update metadata
        metadata = {
            'system_prompt_name': system_prompt_name,
            'use_case': use_case,
            'llm': str(llm),
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'type': 'shared_context'
        }
        self.metadata.update(metadata)
        
        # Prepare hierarchical structure
        yaml_data = {
            'metadata': self.metadata,
            'content': {
                k: v for k, v in self.model_dump().items() 
                if k not in {'metadata', 'model_computed_fields', 'model_config', 'model_extra', 'model_fields', 'model_fields_set'}
            }
        }   
        
        # Generate filename
        if isinstance(llm, ChatOpenAI):
            llm_name = llm.model_name
        elif isinstance(llm, ChatAnthropic):
            llm_name = llm.model
        elif hasattr(llm, 'model_name'):
            llm_name = llm.model_name
        elif isinstance(llm, str):
            llm_name = llm
        else:
            llm_name = str(llm)

        filename = f"resources/sharedcontexts/exported_{system_prompt_name}_{use_case}_{llm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        
        # Save to file with metadata first
        with open(filename, 'w', encoding='utf-8') as f:
            # Write metadata first
            f.write("metadata:\n")
            for line in yaml.dump(self.metadata, default_flow_style=False).splitlines():
                f.write("  " + line + "\n")
            # Then write content
            f.write("content:\n")
            for line in yaml.dump(yaml_data['content'], default_flow_style=False).splitlines():
                f.write("  " + line + "\n")
        
        self._export_path = filename
        return filename

    def get_export_path(self) -> str:
        """Returns the path where the context was last exported"""
        if not self._export_path:
            raise ValueError("Context has not been exported yet")
        return self._export_path

    def print_fields(self) -> None:
        """Print all fields including dynamic ones"""
        self.printer("\nShared Context Fields:")
        self.printer("-" * 20)
        
        # Get all model fields
        model_data = self.model_dump()
        
        # Print static fields first
        self.printer("Static Fields:")
        self.printer(f"metadata: {self.metadata}")
        
        # Print dynamic fields
        self.printer("\nDynamic Fields:")
        internal_fields = {
            'metadata', 
            'model_computed_fields', 
            'model_config', 
            'model_extra', 
            'model_fields', 
            'model_fields_set'
        }
        
        for field_name, value in model_data.items():
            if field_name not in internal_fields:
                self.printer(f"{field_name}: {value}")
        
        self.printer("-" * 20)

    @classmethod
    def load_context(cls, filename: str, debug: bool = False) -> 'BaseSharedContext':
        """Load shared context from a YAML file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Create instance with metadata
            instance = cls(metadata=data.get('metadata', {}))
            
            # Add content fields as dynamic fields
            content = data.get('content', {})
            instance._dynamic_fields = content
            for key, value in content.items():
                setattr(instance, key, value)
            
            if debug:
                logging.getLogger("note_interpreter").debug(f"[DEBUG] Loaded context with dynamic fields: {instance._dynamic_fields}")
            
            return instance
            
        except Exception as e:
            if debug:
                logging.getLogger("note_interpreter").debug(f"[ERROR] Failed to load context: {str(e)}")
            return cls()

    def get_content_fields(self) -> Dict[str, Any]:
        """Get metadata and all content fields"""
        # Start with metadata
        result = {'metadata': self.metadata}
        
        # Add content fields
        model_data = self.model_dump()
        internal_fields = {
            'metadata', 
            'model_computed_fields', 
            'model_config', 
            'model_extra', 
            'model_fields', 
            'model_fields_set'
        }
        
        content_fields = {
            field_name: value 
            for field_name, value in model_data.items() 
            if field_name not in internal_fields
        }
        
        result.update(content_fields)
        return result



@dataclass
class ToolDefinition:
    """Structured definition of a tool"""
    name: str
    description: str
    schema: Dict
    function: Optional[callable] = None
    external_params: Optional[Dict[str, Any]] = None
    # todo delete this


class ToolProvider(ABC):
    @abstractmethod
    def prepare_tool_call(self, tool: ToolDefinition) -> Dict:
        """Provider-specific tool format"""
        pass
    
    def bind_tools(self, llm: Any, tools: List[ToolDefinition]) -> Any:
        """Common bind logic with provider-specific parts"""
        # 1. Provider-specific tool definitions
        tool_dicts = [self.prepare_tool_call(tool) for tool in tools]
        
        # 2. Provider-specific binding
        bound_llm = self._bind_to_llm(llm, tool_dicts)
        return bound_llm
    
    @abstractmethod
    def _bind_to_llm(self, llm: Any, tool_dicts: List[Dict]) -> Any:
        """Provider-specific binding implementation"""
        pass


class OpenAIToolProvider(ToolProvider):
    def prepare_tool_call(self, tool: ToolDefinition) -> Dict:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.schema
            }
        }
    
    def _bind_to_llm(self, llm: Any, tool_dicts: List[Dict]) -> Any:
        return llm.bind_tools(tool_dicts)


class AnthropicToolProvider(ToolProvider):
    def prepare_tool_call(self, tool: ToolDefinition) -> Dict:
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.schema
        }
    
    def _bind_to_llm(self, llm: Any, tool_dicts: List[Dict]) -> Any:
        return llm.bind(tools=tool_dicts)


class AgentState(BaseModel):
    """Base state model for agents"""
    conversation_history: List[Dict] = Field(default_factory=list)
    tool_outputs: List[Dict] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)
    last_response: Optional[Dict] = Field(default=None)
    last_tool_call: Optional[Dict] = Field(default=None)
    tool_results: List[Dict] = Field(default_factory=list)

# todo kell ez nekunk?
class MessageType:
    """Enum-like class for message types"""
    CONVERSATION = "conversation"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"

class AgentCoreV2(Generic[StateType, ResponseType]):
    """
    Core agent implementation with interactive capabilities.
    :param logger: Logger instance to use for logging (default: standard logging.getLogger(__name__))
    :param printer: User-facing output function (default: user_print)
    """
    def __init__(
        self,
        llm: BaseChatModel,
        tools: List['ToolDefinition'],
        system_prompt: str,
        shared_context: Optional[Dict[str, Any]] = None,
        context_usage: Optional[Dict[str, List[str]]] = None,
        tool_provider: Optional['ToolProvider'] = None, #todo delete this, llm bol kitalalja
        should_initiate: bool = True,
        debug_mode: bool = False,
        logger=None,
        printer=None
    ):
        self.debug_mode = debug_mode
        self.llm = llm
        self.tools = tools
        self.shared_context = shared_context or {}
        self.context_usage = context_usage or {}
        self.printer = printer or user_print
        
        # Prompt injection ha van shared context és usage konfig
        if shared_context and context_usage and context_usage.get('inject_to_system_prompt'):
            system_prompt = self._inject_prompt_variables(system_prompt)
            if self.debug_mode:
                if logger:
                    logger.debug(f"\n[DEBUG] System prompt after injection: {system_prompt}")
                else:
                    self.logger.debug(f"[DEBUG] System prompt after injection: {system_prompt}")
        
        self.system_prompt = system_prompt
        
        # Tool provider inicializálás
        self.tool_provider = tool_provider or self._get_default_tool_provider()
        self.bound_llm = self.tool_provider.bind_tools(self.llm, tools) if tools else self.llm
        
        self.logger = logger or logging.getLogger(__name__)
        
        # State inicializálás
        self.state = AgentState()
        self.state.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
        
        # Kezdeti beszélgetés
        if should_initiate:
            try:
                response = self.handle_user_message("Hello")
                self.state.conversation_history.append({
                    "role": "assistant",
                    "content": response["display_message"],
                    "timestamp": datetime.now().isoformat()
                })
                self.print_agent_message(response["display_message"])
            except Exception as e:
                self.logger.error(f"Initialization error: {str(e)}")
                self.print_agent_message("Error during initialization. Please try again.")

    def build_full_response_object(self, llm_response, parsed_response, validated_output=None):
        return {
            "type": MessageType.TOOL_CALL if parsed_response.get("tool_used") else MessageType.CONVERSATION,
            "display_message": parsed_response.get("message"),
            "tool_details": {
                "name": parsed_response.get("tool_name"),
                "args": parsed_response.get("tool_args")
            } if parsed_response.get("tool_used") else None,
            "raw_response": llm_response,
            "parsed_response": parsed_response,
            "validated_output": validated_output
        }

    def handle_user_message(self, message: str) -> Dict:
        """Process a user message and return structured response"""
        try:
            self._add_to_conversation_history({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            try:
                self.logger.debug("[DEBUG] Conversation history sent to LLM:\n" + json.dumps(self.state.conversation_history, indent=2, ensure_ascii=False))
            except Exception as e:
                self.logger.debug(f"[DEBUG] Could not serialize conversation history: {e}")
            llm_response = self.bound_llm.invoke(self.state.conversation_history)
            parsed_response = self._extract_llm_response(llm_response)
            # Optionally, validated_output = self.validate_output(parsed_response)  # Not implemented yet
            validated_output = None
            if parsed_response.get('tool_used'):
                tool_result = self.execute_tool_function(parsed_response)
                self.state.tool_outputs.append({
                    "tool_name": parsed_response['tool_name'],
                    "tool_args": parsed_response['tool_args'],
                    "result": tool_result,
                    "timestamp": datetime.now().isoformat()
                })
                history_entry = {
                    "role": "assistant",
                    "type": MessageType.TOOL_CALL,
                    "content": parsed_response['message'],
                    "timestamp": datetime.now().isoformat(),
                    "tool_name": parsed_response['tool_name'],
                    "tool_args": parsed_response['tool_args'],
                    "tool_result": tool_result
                }
            else:
                history_entry = {
                    "role": "assistant",
                    "type": MessageType.CONVERSATION,
                    "content": parsed_response['message'],
                    "timestamp": datetime.now().isoformat()
                }
            self._add_to_conversation_history(history_entry)
            return self.build_full_response_object(llm_response, parsed_response, validated_output)
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.logger.error(error_msg)
            self._add_to_conversation_history({
                "role": "system",
                "type": MessageType.ERROR,
                "content": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            return {
                "type": MessageType.ERROR,
                "display_message": f"An error occurred: {str(e)}",
                "error_details": error_msg,
                "raw_response": None,
                "parsed_response": None,
                "validated_output": None
            }

    def execute_tool_function(self, response_data: Dict) -> Any:
        """Execute a tool function with given arguments and shared context."""
        tool_name = response_data['tool_name']
        tool_args = response_data['tool_args']

        tool_definition = next((tool for tool in self.tools if tool.name == tool_name), None)
        if tool_definition and tool_definition.function:
            # Egyszerűen meghívjuk a függvényt a tool_args-szal és shared_context-tel
            result = tool_definition.function(
                **tool_args,
                shared_context=self.shared_context
            )
            return result

        return None



    def run_interactive_session(self) -> List[Dict]:
        """Run an interactive session with the agent"""
        while True:
            user_input = input("\033[92mUser: \033[0m")
            if user_input.lower() == 'exit':
                break
            
            try:
                response = self.handle_user_message(user_input)
                
                if response["type"] == MessageType.ERROR:
                    self.print_agent_message(f"Error: {response['display_message']}")
                elif response["type"] == MessageType.TOOL_CALL:
                    self.print_agent_message(f"Using {response['tool_details']['name']} tool...")
                    self.print_agent_message(response["display_message"])
                    
                    # Record tool usage in state
                    self.state.tool_outputs.append({
                        "tool_name": response['tool_details']['name'],
                        "tool_args": response['tool_details']['args'],
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    self.print_agent_message(response["display_message"])
                    
            except Exception as e:
                error_details = f"Session error: {str(e)}"
                self.logger.error(error_details)
                self.print_agent_message(
                    "I encountered an error processing your message.\n"
                    f"Details: {error_details}\n"
                    "Please try again or rephrase your request."
                )
        
        return self.state.conversation_history

    def _extract_llm_response(self, response: Any) -> Dict:
        """Extract structured response from LLM output"""
        try:
            if hasattr(response, 'tool_calls') and response.tool_calls:
                tool_result = {
                    'tool_used': True,
                    'tool_name': response.tool_calls[0].get('name'),
                    'tool_args': response.tool_calls[0].get('args', {}),
                    'message': response.content if hasattr(response, 'content') else "Using tool to analyze..."
                }
                return tool_result
            else:
                return {
                    'tool_used': False,
                    'tool_name': None,
                    'tool_args': None,
                    'message': response.content
                }
        except Exception as e:
            self.logger.error(f"Error extracting response: {str(e)}")
            raise

    def _add_to_conversation_history(self, message: Dict):
        """Helper method to add messages to conversation history"""
        self.state.conversation_history.append(message)
        if self.debug_mode:
            self.logger.debug(f"[DEBUG] Adding to history: {message}")

    def get_state(self) -> AgentState:
        """Get current state"""
        # Return a deep copy of the state
        return AgentState(
            conversation_history=self.state.conversation_history.copy(),
            tool_outputs=self.state.tool_outputs.copy(),
            errors=self.state.errors.copy(),
            metadata=self.state.metadata.copy()
        )

    def _get_default_tool_provider(self) -> "ToolProvider":
        """Get default tool provider based on LLM type"""
        if isinstance(self.llm, ChatAnthropic):
            return AnthropicToolProvider()
        elif isinstance(self.llm, ChatOpenAI):
            return OpenAIToolProvider()
        else:
            raise ValueError(f"No default tool provider for LLM type: {type(self.llm)}")

    def _format_response_for_display(self, response_data: Dict) -> str:
        """Format the response data into a human-readable string"""
        if response_data['type'] == 'conversation':
            return response_data['content']
        elif response_data['type'] == 'tool_response':
            tool_args = response_data['content']['tool_args']
            # Általános tool output formázás
            output_lines = [f"Here's the {response_data['content']['tool_name']} result:"]
            for key, value in tool_args.items():
                output_lines.append(f"{key}: {value}")
            return "\n".join(output_lines)
        else:
            return f"Sorry, there was an error: {response_data['content']}"

    def get_last_response(self) -> Optional[Dict]:
        """Az utolsó strukturált válasz lekérése"""
        return self.state.last_response

    @staticmethod
    def print_user_message(message: str, printer=user_print):
        """Prints the user message using the provided printer."""
        printer(f"User: {message}")

    @staticmethod
    def print_agent_message(message: str, printer=user_print):
        """Prints the agent message using the provided printer."""
        printer(f"Assistant: {message}")

    def _inject_prompt_variables(self, prompt: str) -> str:
        """Inject shared context values into prompt template"""
        prompt_vars = {}
        for field in self.context_usage.get('inject_to_system_prompt', []):
            # Check if the field exists using hasattr
            if hasattr(self.shared_context, field):
                prompt_vars[field] = getattr(self.shared_context, field)
            elif self.debug_mode:
                self.logger.debug(f"[DEBUG] Warning: Field {field} not found in shared context")
        
        try:
            return prompt.format(**prompt_vars)
        except KeyError as e:
            if self.debug_mode:
                self.logger.debug(f"[DEBUG] Error formatting prompt: {e}")
            return prompt

    def invoke_with_message_list(self, messages: List[Dict]) -> Dict:
        """Invoke the LLM with a list of messages and return a full response object"""
        try:
            llm_response = self.bound_llm.invoke(messages)
            parsed_response = self._extract_llm_response(llm_response)
            validated_output = None  # Optionally, call self.validate_output(parsed_response)
            return self.build_full_response_object(llm_response, parsed_response, validated_output)
        except Exception as e:
            error_msg = f"Error invoking LLM: {str(e)}"
            self.logger.error(error_msg)
            return {
                "type": MessageType.ERROR,
                "display_message": f"An error occurred: {str(e)}",
                "error_details": error_msg,
                "raw_response": None,
                "parsed_response": None,
                "validated_output": None
            }