from langchain.prompts import PromptTemplate

def CompanyResearchPrompt() -> PromptTemplate:
    template = """
        You are a business research analyst. Based on the user input and search results, 
        provide comprehensive information about the company including:
        
        User Input: {input}
        Search Results: {search_results}
        
        Extract and structure the following information:
        - Company name
        - Industry they operate in
        - Business segment/sector
        - Key products and services offered
        - Strategic focus areas (operations, customer experience, innovation, etc.)
        - Company vision and mission
        
        Be specific and factual based on the search results provided.
        """

    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "search_results"]
    )
    return prompt

def MarketAnalysisPrompt()-> PromptTemplate:
    template = """
        You are an expert market analyst specializing in AI and ML adoption across industries.
        
        Based on the company research and search results, analyze the market standards and industry trends for AI/ML adoption.
        
        Company Information:
        - Company: {company}
        - Industry: {industry}
        - Segment: {segment}
        
        Search Results:
        {search_results}
        
        Competitor Analysis:
        {competitor_search}
        
        Provide a comprehensive market analysis including:
        1. Current AI/ML trends in the {industry} industry
        2. Industry standards for AI adoption and implementation
        3. What competitors and industry leaders are doing with AI technologies
        4. Market opportunities for AI adoption in this industry
        
        Focus on:
        - Emerging technologies (GenAI, LLMs, Computer Vision, etc.)
        - Implementation patterns and best practices
        - ROI and business impact metrics
        - Regulatory and compliance considerations
        - Technology adoption timelines and maturity levels
        """

    prompt = PromptTemplate(
        template=template,
        input_variables=["company", "industry", "segment", "search_results", "competitor_search"],
    )
    return prompt

def UseCaseGenerationPrompt()->PromptTemplate:
    template = """
        You are an expert AI solution architect who generates practical and implementable AI/ML use cases for businesses.
        
        Company Context:
        - Company: {company}
        - Industry: {industry}
        - Key Offerings: {key_offerings}
        - Strategic Focus Areas: {strategic_focus}
        
        Market Intelligence:
        - Industry Trends: {industry_trends}
        - Market Opportunities: {market_opportunities}
        
        Industry Use Case Research:
        {use_case_search}
        
        Generate comprehensive AI/ML use cases that align with the company's strategic focus areas. For each use case, consider:
        
        TECHNOLOGY FOCUS:
        - Generative AI (GenAI): Content generation, code assistance, document processing
        - Large Language Models (LLMs): Conversational AI, text analysis, knowledge extraction
        - Traditional ML: Predictive analytics, classification, clustering
        - Computer Vision: Image/video analysis, quality control, automation
        - NLP: Sentiment analysis, entity extraction, document understanding
        
        BUSINESS AREAS:
        - Operations: Process automation, predictive maintenance, quality control
        - Customer Experience: Chatbots, personalization, recommendation systems
        - Supply Chain: Demand forecasting, inventory optimization, logistics
        - Finance: Fraud detection, risk assessment, automated reporting
        - HR: Talent acquisition, employee engagement, performance analysis
        - Marketing: Content generation, customer segmentation, campaign optimization
        
        For each use case, provide:
        1. Clear title and category
        2. Specific business problem it solves
        3. Detailed AI/ML solution approach
        4. Expected quantifiable benefits (cost savings, efficiency gains, revenue impact)
        5. Implementation complexity assessment (High/Medium/Low)
        
        Generate 8-12 diverse use cases covering different business functions and AI technologies.
        Rank the top 5 use cases by priority based on:
        - Business impact potential
        - Implementation feasibility
        - Alignment with company strategy
        - Market readiness and competitive advantage
        """

    prompt = PromptTemplate(
        template=template,
        input_variables=[
                "company", "industry", "key_offerings", "strategic_focus", 
                "industry_trends", "market_opportunities", "use_case_search"
            ],
    )
    return prompt

def ResourceCollectionPrompt() -> PromptTemplate:
    template = """
        You are an expert AI/ML resource curator and data scientist specializing in finding relevant datasets, repositories, and implementation resources.
        
        Company Context:
        - Company: {company}
        - Industry: {industry}
        
        Use Cases to Support:
        {use_cases}
        
        Resource Search Results:
        {resource_searches}
        
        Based on the search results from Kaggle, HuggingFace, GitHub, and other platforms, curate comprehensive resource assets for each use case.
        
        For each use case, extract and organize:
        
        KAGGLE DATASETS:
        - Focus on datasets relevant to the use case domain
        - Include both training and benchmark datasets
        - Prefer datasets with high usability scores
        - Examples: customer data, sales data, image datasets, text corpora
        
        HUGGINGFACE RESOURCES:
        - Pre-trained models that can be fine-tuned for the use case
        - Relevant datasets from HuggingFace Hub
        - Spaces with working demos
        - Examples: bert-base-uncased, gpt2, stable-diffusion, sentiment analysis models
        
        GITHUB REPOSITORIES:
        - Implementation examples and tutorials
        - Open-source frameworks and libraries
        - End-to-end project templates
        - Industry-specific implementations
        
        ADDITIONAL RESOURCES:
        - Research papers and white papers
        - Documentation and tutorials
        - API services and cloud resources
        - Industry reports and case studies
        
        For each resource, provide:
        1. Clear title and description
        2. Direct URL link (ensure links are valid and accessible)
        3. Relevance explanation to the specific use case
        4. Quality assessment and recommendations
        
        Create a platform summary with:
        - Total count of resources found on each platform
        - Top 3-5 recommendations for each platform
        - Quality and relevance ranking
        
        Generate an implementation roadmap with phases:
        - Phase 1 (Quick Wins): Low complexity, high impact use cases
        - Phase 2 (Core Implementation): Medium complexity, strategic use cases  
        - Phase 3 (Advanced): High complexity, transformational use cases
        
        For each phase include:
        - Timeline estimates
        - Priority level
        - Key resources and dependencies
        - Use cases to be implemented
        
        Ensure all URLs are clickable and properly formatted.
        Focus on resources that are:
        - Actively maintained and updated
        - Well-documented
        - Relevant to the specific industry and use cases
        - Accessible and free to use where possible
        
        REQUIREMENTS:
        1. Generate resources for ALL use cases provided
        2. Each list must contain exactly 3 URLs
        3. URLs must be realistic and properly formatted
        4. Focus on resources that support the specific technology focus        

        """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["company", "industry", "use_cases", "resource_searches"]
    )
    return prompt

