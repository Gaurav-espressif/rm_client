from typing import List, Dict, Optional
from pydantic import BaseModel

class NodeMetadataUpdate(BaseModel):
    tags: Optional[List[str]] = None
    metadata: Optional[Dict] = None

class NodeTagsDelete(BaseModel):
    tags: List[str]

class NodeFilterParams(BaseModel):
    node_id: Optional[str] = None
    node_type: Optional[str] = None
    model: Optional[str] = None
    # ... include all other filter fields