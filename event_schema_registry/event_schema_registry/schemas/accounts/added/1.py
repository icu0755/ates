schema = {
    "type": "object",
    "properties": {
        "event": {"const": "AccountsAdded"},
        "version": {"const": 1},
        "payload": {
            "type": "object",
            "properties": {"public_id": {"type": "string"}, "role": {"type": "string"}},
            "required": ["public_id", "role"],
        },
    },
    "required": ["event", "version", "payload"],
}
