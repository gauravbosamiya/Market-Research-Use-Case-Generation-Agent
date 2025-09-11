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




