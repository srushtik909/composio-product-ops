from pydantic import BaseModel, Field
from typing import List, Optional


class Evidence(BaseModel):
    claim: str
    url: str
    source_type: str


class AppResearch(BaseModel):
    app: str
    category: str
    description: str

    auth_methods: List[str]

    access_model: str

    api_type: List[str]
    api_breadth: str

    mcp_availability: str

    buildability: str
    main_blocker: Optional[str] = None

    evidence: List[Evidence]

    confidence: float = Field(
        ge=0,
        le=1
    )

    notes: Optional[str] = None