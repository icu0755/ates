schema = {
    "type": "object",
    "properties": {
        "event": {"const": "TasksAssigned"},
        "version": {"const": 1},
        "payload": {
            "type": "object",
            "properties": {
                "public_id": {"type": "string"},
                "assignee_id": {"type": "string"},
            },
            "required": ["public_id", "assignee_id"],
        },
    },
    "required": ["event", "version", "payload"],
}
