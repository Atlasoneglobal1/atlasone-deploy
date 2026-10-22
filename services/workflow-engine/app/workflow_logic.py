def handle_pos_failure(payload):
    return {
        "workflow": "POS_FAILURE_FALLBACK",
        "received": payload,
        "status": "fallback_triggered"
    }

def handle_ce_title_mortgage(payload):
    return {
        "workflow": "CE_TITLE_MORTGAGE",
        "received": payload,
        "status": "workflow_started"
    }
