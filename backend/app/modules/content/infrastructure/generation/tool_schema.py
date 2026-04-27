from __future__ import annotations

MCQ_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string", "minLength": 1},
        "choices": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
            "minItems": 2,
            "maxItems": 5,
        },
        "correct_index": {"type": "integer", "minimum": 0, "maximum": 4},
        "rationale": {"type": "string"},
    },
    "required": ["question", "choices", "correct_index", "rationale"],
}

SHORT_ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string", "minLength": 1},
        "grading_notes": {"type": "string", "minLength": 1},
    },
    "required": ["prompt", "grading_notes"],
}

READING_BODY = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "minLength": 100, "maxLength": 4000},
        "mcq": {"type": "array", "items": MCQ_SCHEMA, "minItems": 3, "maxItems": 5},
        "short_answer": SHORT_ANSWER_SCHEMA,
    },
    "required": ["text", "mcq", "short_answer"],
}

LISTENING_BODY = {
    "type": "object",
    "properties": {
        "transcript": {"type": "string", "minLength": 1},
        "mcq": {"type": "array", "items": MCQ_SCHEMA, "minItems": 3, "maxItems": 5},
        "short_answer": SHORT_ANSWER_SCHEMA,
    },
    "required": ["transcript", "mcq", "short_answer"],
}

SPEAKING_BODY = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string", "minLength": 1},
    },
    "required": ["prompt"],
}

WRITING_BODY = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string", "minLength": 1},
        "exemplar": {"type": "string"},
    },
    "required": ["prompt"],
}

CREATE_PIECE_DRAFT_TOOL = {
    "name": "create_piece_draft",
    "description": "Return the generated piece draft fitting the requested kind/CEFR/topic.",
    # Gemini function declarations support a narrower schema subset than JSON Schema.
    # Keep the shape broad here and enforce strict validation in domain/build_body.
    "input_schema": {
        "type": "object",
        "properties": {
            "kind": {
                "type": "string",
                "enum": ["reading", "listening", "speaking", "writing"],
            },
            "slug": {"type": "string"},
            "title": {"type": "string"},
            "minutes": {"type": "integer"},
            "body": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "transcript": {"type": "string"},
                    "prompt": {"type": "string"},
                    "exemplar": {"type": "string"},
                    "mcq": {"type": "array", "items": MCQ_SCHEMA},
                    "short_answer": SHORT_ANSWER_SCHEMA,
                },
            },
        },
        "required": ["kind", "slug", "title", "minutes", "body"],
    },
}
