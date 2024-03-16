schema = {
    "type": "object",
    "properties": {
        "event": {"const": "TasksAdded"},
        "version": {"const": 1},
        "payload": {
            "type": "object",
            "properties": {
                "public_id": {"type": "string"},
                "assignee_id": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["public_id", "assignee_id", "description"],
        },
    },
    "required": ["event", "version", "payload"],
}
