
assistant_tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "save_value",
                            "description": "Validate and save the identified key values",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "values": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "The list of key values identified in the user's message. Values must be in Russian. The value starts with capital letter"
                                    }
                                },
                                "required": ["values"]
                            }
                        }
                    }
                ]


valid_tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "is_life_value",
                        "description": "Check if the value is a key life value in Russian",
                        "parameters": {
                            "type": "boolean",
                            "properties": {
                                "is_value": {
                                    "type": "string",
                                    "description": """
                                            Contains only 'true' or 'false' string.                             
                                            This string represents the answer to the user's question is whether the
                                            provided value is a valid life value or contains nonsense.
                                            Contains 'true' means values are defined correctly, do not contain nonsense. 
                                            Contains 'false' — the value is determined incorrectly or the string is empty
                                            """,
                                }
                            },
                            "required": ["is_value"],
                        },
                    }
                }
            ]