from typing import Optional

def _build_conversation_filter(conversation_id: Optional[str]):
    if conversation_id is not None:
        return {"conversation_id": conversation_id}
    else:
        return {}