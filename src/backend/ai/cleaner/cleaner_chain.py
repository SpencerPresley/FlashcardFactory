from chain_composer import ChainComposer
from backend.models import CleanerOutput
from backend.prompts import CLEANER_SYSTEM_PROMPT, CLEANER_HUMAN_PROMPT
import json
print(f"CLEANER_SYSTEM_PROMPT: {CLEANER_SYSTEM_PROMPT}")
print(f"CLEANER_HUMAN_PROMPT: {CLEANER_HUMAN_PROMPT}")

class CleanerChain:
    def __init__(
        self,
        api_key: str,
        model: str | None = "gemini-2.0-flash-thinking-exp-01-21"
    ):
        self.cp = ChainComposer(
            model=model,
            api_key=api_key,
            temperature=0.0,
        )
        
        self._add_layer()
    
    def _add_layer(self) -> None:
        self.cp.add_chain_layer(
            system_prompt=CLEANER_SYSTEM_PROMPT,
            human_prompt=CLEANER_HUMAN_PROMPT,
            parser_type="json",
            pydantic_output_model=CleanerOutput,
            output_passthrough_key_name="cleaned_text",
        )
        
    def run(self, text: str) -> CleanerOutput:
        print(f"Running cleaner chain with text: {text}")
        res = self.cp.run({"text": text})
        print(f"Cleaner chain result:\n{json.dumps(res, indent=4)}")
        return res