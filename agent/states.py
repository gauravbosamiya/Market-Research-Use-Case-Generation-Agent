from pydantic import BaseModel, Field
from typing import List

class CompanyResearch(BaseModel):
    Company: str = Field(description="The name of the company being researched")
    Industry: str = Field(description="The industry or industries the company operates in, e.g., 'Automotive', 'Finance', 'Healthcare'")
    Segment: str = Field(description="The primary segment or focus area of the company, e.g., 'Electric Vehicles', 'Retail'")
    Key_Offerings: list[str] = Field(description="A list of the company's main products, services, or offerings")
    Strategic_Focus_Areas: list[str] = Field(description="A list of the company's strategic focus areas, e.g., 'Operations', 'Customer Experience', 'Sustainability'")
    Vision: str = Field(description="The company's vision or mission statement")


class UseCase(BaseModel):
    title: str = Field(description="Title of the use case")
    problem_statement: str = Field(description="Business problem this solves")
    ai_ml_solution: str = Field(description="Specific AI/ML technology to be used")
    expected_benefits: List[str] = Field(description="List of expected benefits")
    implementation_complexity: str = Field(description="High/Medium/Low complexity assessment")
    category: str = Field(description="Category: Operations, Customer Experience, Supply Chain, etc.")


class MarketAnalysis(BaseModel):
    industry_trends: List[str] = Field(description="Current AI/ML trends in the industry")
    industry_standards: List[str] = Field(description="Industry standards for AI adoption")
    competitor_analysis: List[str] = Field(description="What competitors are doing with AI")
    market_opportunities: List[str] = Field(description="Market opportunities for AI adoption")
    
class UseCases(BaseModel):
    use_cases: List[UseCase] = Field(description="List of generated use cases")
    priority_ranking: List[str] = Field(description="Top 5 priority use cases")
    

# task 3
# class ResourceLink(BaseModel):
#     title: str = Field(description="Title of the resource")
#     url: str = Field(description="URL link to the resource")
#     description: str = Field(description="Brief description of what this resource provides")

# class ImplementationPhase(BaseModel):
#     phase_name: str = Field(description="Name of the implementation phase")
#     timeline: str = Field(description="Timeline for this phase")
#     priority: str = Field(description="Priority level: High/Medium/Low")
#     use_cases: List[str] = Field(description="Use cases in this phase")
#     key_resources: List[str] = Field(description="Key resources for this phase")

# class PlatformSummary(BaseModel):
#     kaggle_count: int = Field(description="Total number of Kaggle resources found")
#     huggingface_count: int = Field(description="Total number of HuggingFace resources found")
#     github_count: int = Field(description="Total number of GitHub repositories found")
#     kaggle_recommendations: List[str] = Field(description="Top Kaggle recommendations")
#     huggingface_recommendations: List[str] = Field(description="Top HuggingFace recommendations")
#     github_recommendations: List[str] = Field(description="Top GitHub recommendations")

# class UseCaseResource(BaseModel):
#     use_case_resources: List[ResourceLink] = Field(description="Resources for each use case", default=[])
#     implementation_roadmap: List[ImplementationPhase] = Field(description="Implementation phases", default=[])
#     total_resources_found: int = Field(description="Total number of resources found")
#     platform_summary: PlatformSummary = Field(description="Summary by platform")




