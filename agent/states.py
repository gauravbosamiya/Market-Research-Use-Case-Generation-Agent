from pydantic import BaseModel, Field

class CompanyResearch(BaseModel):
    Company: str = Field(description="The name of the company being researched")
    Industry: str = Field(description="The industry or industries the company operates in, e.g., 'Automotive', 'Finance', 'Healthcare'")
    Segment: str = Field(description="The primary segment or focus area of the company, e.g., 'Electric Vehicles', 'Retail'")
    Key_Offerings: list[str] = Field(description="A list of the company's main products, services, or offerings")
    Strategic_Focus_Areas: list[str] = Field(description="A list of the company's strategic focus areas, e.g., 'Operations', 'Customer Experience', 'Sustainability'")
    Vision: str = Field(description="The company's vision or mission statement")
