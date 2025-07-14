"""
Struct command for Sandbox CLI

Test structured replies from OpenRouter
"""

from typing import Any

import click
from typing_extensions import override

from ..command_interface import BaseCommand, GlobalConfig
from ..util import console
from ..util.ai import get_openai_client


class StructCommand(BaseCommand):
    """Minimal struct command"""

    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        """Register the struct command with the CLI group"""

        @cli_group.command()
        @click.option(
            "--word", required=True, help="The word to find better alternatives for"
        )
        @click.option(
            "--context", help="The sentence or context where the word appears"
        )
        @click.pass_context
        def struct(ctx: click.Context, word: str, context: str | None = None) -> None:  # type: ignore
            """
            📝 A structured output command for word suggestions

            Find better alternatives for a given word using AI with structured JSON output.
            Provide context (like a sentence) to get more accurate word replacements.
            """
            config = StructCommand.get_config_from_context(ctx)
            StructCommand.execute(config, word, context)

    @staticmethod
    def execute(config: GlobalConfig, word: str, context: str | None = None) -> None:
        """
        Execute the struct command

        Args:
            config: Global configuration object
            word: The word to find better alternatives for
            context: The sentence or context where the word appears
        """
        if StructCommand.should_skip_output(config):
            return

        # CODE BEGINS HERE

        client = get_openai_client(enable_caching=False)

        if config.verbose:
            console.print("Creating structured output example with JSON schema...")

        # Define a JSON schema for word suggestions
        word_suggestions_schema: dict[str, Any] = {
            "type": "object",
            "properties": {
                "original_word": {
                    "type": "string",
                    "description": "The original word that was provided",
                },
                "suggestions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": {
                                "type": "string",
                                "description": "The suggested alternative word",
                            }
                        },
                        "required": ["word"],
                        "additionalProperties": False,
                    },
                    "description": "5 word suggestions, ordered from best to least recommended",
                    "minItems": 5,
                    "maxItems": 5,
                },
            },
            "required": ["original_word", "suggestions"],
            "additionalProperties": False,
        }

        try:
            # Build the user message
            if context:
                user_message = f"In the sentence or context: '{context}', find 5 better alternatives for the word '{word}' that would fit naturally in this context."
            else:
                user_message = f"Find 5 better alternatives for the word '{word}'"

            if config.verbose:
                console.print(f"🔍 Analyzing word: '{word}'")
                if context:
                    console.print(f"📝 Context: {context}")

            # Make an API call with structured output using strict mode
            response = client.chat.completions.create(
                model="openai/gpt-4o",  # Using a model that supports structured outputs
                messages=[
                    {
                        "role": "system",
                        "content": "You are a vocabulary expert. When given a word and its context, provide 5 better alternatives that would fit naturally in that specific context. If no context is provided, give general alternatives. Order suggestions from best to least recommended. For each suggestion, explain why it's better in that context and provide an example of how it would work in the original sentence or a similar context.",
                    },
                    {"role": "user", "content": user_message},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "word_suggestions",
                        "strict": True,  # Enable strict mode for exact schema compliance
                        "schema": word_suggestions_schema,
                    },
                },
            )

            # Parse the structured response
            suggestions_data = response.choices[0].message.content

            console.print("✅ Structured Output Response:")
            console.print(suggestions_data)

            if config.debug:
                console.print(f"\n🔍 Raw response object: {response}")
                console.print(f"📊 Usage: {response.usage}")

        except Exception as e:
            console.print(f"❌ Error making structured API call: {e}")
            if config.debug:
                import traceback

                console.print(f"🐛 Full traceback: {traceback.format_exc()}")
