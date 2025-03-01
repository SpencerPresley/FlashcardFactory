from __future__ import annotations

from typing import TYPE_CHECKING

import json
from chain_composer import ChainComposer
from backend.prompts import FLASHCARDER_SYSTEM_PROMPT, FLASHCARDER_HUMAN_PROMPT
from backend.models import FlashcarderOutput

if TYPE_CHECKING:
    from backend.models import UserFormReg

class FlashcarderChain:
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
            system_prompt=FLASHCARDER_SYSTEM_PROMPT,
            human_prompt=FLASHCARDER_HUMAN_PROMPT,
            parser_type="json",
            pydantic_output_model=FlashcarderOutput,
            output_passthrough_key_name="flashcards",
        )
        
    def run(self, user_form: UserFormReg) -> FlashcarderOutput:
        print(f"Running flashcarder chain with user form: {user_form}")
        res = self.cp.run({"course_name": user_form.course_name,
                           "difficulty": user_form.difficulty,
                           "school_level": user_form.school_level,
                           "subject": user_form.subject,
                           "rules": user_form.rules,
                           "subject_material": user_form.subject_material,
                           "num_flash_cards": user_form.num_flash_cards})
        print(f"Flashcarder chain result:\n{json.dumps(res, indent=4)}")
        return res