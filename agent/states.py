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
class ResourceLink(BaseModel):
    title: str = Field(description="Title of the resource")
    url: str = Field(description="URL link to the resource")
    description: str = Field(description="Brief description of what this resource provides")

class UseCaseResource(BaseModel):
    use_case_title: str = Field(description="Title of the use case this resource supports")
    category: str = Field(description="Category of the use case")
    technology_focus: str = Field(description="Primary AI/ML technology focus")
    kaggle_datasets: List[ResourceLink] = Field(description="Relevant Kaggle datasets", default=[])
    huggingface_resources: List[ResourceLink] = Field(description="Relevant HuggingFace models/datasets", default=[])
    github_repositories: List[ResourceLink] = Field(description="Relevant GitHub repositories", default=[])
    additional_resources: List[ResourceLink] = Field(description="Other relevant resources", default=[])

class PlatformSummary(BaseModel):
    kaggle_count: int = Field(description="Total number of Kaggle resources found")
    huggingface_count: int = Field(description="Total number of HuggingFace resources found")
    github_count: int = Field(description="Total number of GitHub repositories found")
    kaggle_recommendations: List[str] = Field(description="Top Kaggle dataset recommendations")
    huggingface_recommendations: List[str] = Field(description="Top HuggingFace resource recommendations")
    github_recommendations: List[str] = Field(description="Top GitHub repository recommendations")

class ImplementationPhase(BaseModel):
    phase_name: str = Field(description="Name of the implementation phase")
    timeline: str = Field(description="Estimated timeline for this phase")
    priority: str = Field(description="Priority level: High/Medium/Low")
    use_cases: List[str] = Field(description="Use cases to be implemented in this phase")
    key_resources: List[str] = Field(description="Key resources needed for this phase")

class ResourceAssets(BaseModel):
    use_case_resources: List[UseCaseResource] = Field(description="Resources organized by use case")
    platform_summary: PlatformSummary = Field(description="Summary of resources by platform")
    implementation_roadmap: List[ImplementationPhase] = Field(description="Phased implementation roadmap")
    total_resources_found: int = Field(description="Total number of resources collected")

class ProposedUseCase(BaseModel):
    title: str = Field(description="Title of the proposed use case")
    category: str = Field(description="Business category")
    priority: str = Field(description="High/Medium/Low priority")
    timeline: str = Field(description="Estimated implementation timeline")
    investment_estimate: str = Field(description="Estimated investment required")
    expected_roi: str = Field(description="Expected return on investment")
    problem_statement: str = Field(description="Detailed problem statement")
    solution_approach: str = Field(description="Detailed AI/ML solution approach")
    benefits: List[str] = Field(description="Expected business benefits")
    success_metrics: List[str] = Field(description="Key performance indicators")
    risk_factors: List[str] = Field(description="Potential risks and mitigation strategies")
    references: List[ResourceLink] = Field(description="Supporting references and resources")

class ProjectPhase(BaseModel):
    phase_number: int = Field(description="Phase sequence number")
    phase_name: str = Field(description="Name of the phase")
    duration: str = Field(description="Estimated duration")
    budget_estimate: str = Field(description="Budget estimate for this phase")
    deliverables: List[str] = Field(description="Key deliverables for this phase")
    milestones: List[str] = Field(description="Important milestones")
    success_criteria: List[str] = Field(description="Success criteria for phase completion")

class ImplementationPlan(BaseModel):
    total_timeline: str = Field(description="Total project timeline")
    total_budget: str = Field(description="Total budget estimate")
    phases: List[ProjectPhase] = Field(description="Detailed project phases")
    critical_path: List[str] = Field(description="Critical path activities")
    dependencies: List[str] = Field(description="Key dependencies and prerequisites")

class BusinessCase(BaseModel):
    total_investment: str = Field(description="Total investment required")
    expected_roi: str = Field(description="Expected return on investment")
    payback_period: str = Field(description="Expected payback period")
    risk_assessment: str = Field(description="Overall risk assessment")
    key_benefits: List[str] = Field(description="Key business benefits")
    success_factors: List[str] = Field(description="Critical success factors")
    assumptions: List[str] = Field(description="Key assumptions", default=[])

class NextStep(BaseModel):
    action: str = Field(description="Action to be taken")
    timeline: str = Field(description="When this should be completed")
    owner: str = Field(description="Who should be responsible")
    description: str = Field(description="Detailed description of the action")

class FinalProposal(BaseModel):
    executive_summary: str = Field(description="Executive summary of the proposal")
    top_use_cases: List[ProposedUseCase] = Field(description="Top recommended use cases (5-7)")
    implementation_plan: ImplementationPlan = Field(description="Detailed implementation plan")
    business_case: BusinessCase = Field(description="Business case and ROI analysis")
    next_steps: List[NextStep] = Field(description="Recommended immediate next steps")
    strategic_alignment: str = Field(description="How this aligns with company strategy")
    competitive_advantage: str = Field(description="Expected competitive advantages")





