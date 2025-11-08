import datetime
import json
import os
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

client = genai.Client(api_key=api_key)
from google.genai import types




def generate_sales_proposal(
    prospect_data: str,
    discovery_notes: Optional[str] = None,
    deal_value: Optional[str] = None,
    timeline: Optional[str] = None
) -> dict:
    """
    Generate a customized, professional sales proposal from prospect data and discovery call notes.
    
    The proposal includes:
    - Executive Summary (compelling value proposition)
    - Understanding of Client Needs (pain points from discovery)
    - Proposed Solution (tailored to their requirements)
    - Pricing & Investment (with ROI justification)
    - Implementation Timeline & Next Steps
    - Terms & Conditions
    
    Args:
        prospect_data: Company info, industry, size, current challenges
        discovery_notes: Key insights from discovery calls/meetings
        deal_value: Estimated deal size (e.g., "$50K", "$100K-$150K")
        timeline: Expected implementation timeline (e.g., "Q1 2025", "3 months")
    
    Returns:
        dict with status and complete proposal organized by sections
    """
    if not prospect_data or len(prospect_data.strip()) < 30:
        return {
            "status": "error",
            "message": "Please provide valid prospect data (company info, challenges, requirements) for proposal generation."
        }
    
    prompt = f"""
You are an expert B2B sales proposal writer with 15+ years of experience closing enterprise deals.

Using the information below, create a compelling, customized sales proposal that speaks directly to the prospect's needs and demonstrates clear ROI.

PROSPECT DATA:
{prospect_data}

DISCOVERY CALL NOTES:
{discovery_notes if discovery_notes else 'No specific notes provided - use prospect data to infer needs'}

DEAL DETAILS:
- Estimated Value: {deal_value if deal_value else 'To be determined based on scope'}
- Timeline: {timeline if timeline else '3-6 months implementation'}

Generate a professional proposal with these sections:

1. EXECUTIVE SUMMARY (2-3 paragraphs)
   - Hook them with their biggest pain point
   - Present your solution as the answer
   - Include a compelling ROI statement

2. UNDERSTANDING YOUR NEEDS (bullet points)
   - Show you listened during discovery
   - Mirror their language and priorities
   - Demonstrate industry expertise

3. PROPOSED SOLUTION (detailed)
   - Break down what you'll deliver
   - Map features directly to their needs
   - Include success metrics/KPIs

4. PRICING & INVESTMENT
   - Transparent pricing breakdown
   - Justify cost with ROI calculations
   - Include payment terms options

5. IMPLEMENTATION TIMELINE
   - Phase-by-phase rollout plan
   - Key milestones and deliverables
   - Resource requirements from their side

6. NEXT STEPS & CALL-TO-ACTION
   - Clear path to closing
   - Meeting invitation
   - Urgency element (limited availability, etc.)

Format your answer as a JSON object with these exact keys: 'Executive Summary', 'Understanding Your Needs', 'Proposed Solution', 'Pricing & Investment', 'Implementation Timeline', 'Next Steps'.

Make it persuasive, professional, and tailored. Use specific numbers and outcomes wherever possible.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        try:
            proposal = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        except Exception:
            proposal = response.text.strip()
        
        return {
            "status": "success",
            "proposal": proposal,
            "metadata": {
                "prospect": prospect_data[:100] + "..." if len(prospect_data) > 100 else prospect_data,
                "deal_value": deal_value,
                "timeline": timeline,
                "generated_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat()
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to generate proposal: {str(e)}"
        }


def analyze_win_loss_patterns(
    deals_data: str,
    focus_area: Optional[str] = None
) -> dict:
    """
    Analyze historical win/loss data to identify patterns, common objections, and success factors.
    
    Provides insights on:
    - Win rate by deal size, industry, or competitor
    - Common reasons for lost deals
    - Success patterns in won deals
    - Competitive intelligence (who you lose to and why)
    - Recommended actions to improve win rate
    
    Args:
        deals_data: Historical deal data (won/lost deals with reasons, competitors, deal size, etc.)
        focus_area: Optional focus (e.g., "competitor analysis", "pricing objections", "deal size trends")
    
    Returns:
        dict with status and analysis including patterns, insights, and recommendations
    """
    if not deals_data or len(deals_data.strip()) < 50:
        return {
            "status": "error",
            "message": "Please provide valid historical deal data for win/loss analysis."
        }
    
    prompt = f"""
You are a sales analytics expert specializing in win/loss analysis for B2B sales teams.

Analyze the following historical deal data and provide actionable insights:

DEAL DATA:
{deals_data}

FOCUS AREA: {focus_area if focus_area else 'Comprehensive analysis across all dimensions'}

Provide a structured analysis with:

1. WIN RATE METRICS
   - Overall win rate percentage
   - Win rate by deal size category
   - Win rate by industry/segment
   - Win rate trends over time

2. LOSS PATTERN ANALYSIS
   - Top 5 reasons for lost deals (with percentages)
   - Common competitor patterns (who do we lose to most?)
   - Price sensitivity analysis
   - Deal stage where most losses occur

3. SUCCESS FACTORS IN WON DEALS
   - Common characteristics of won deals
   - Fastest path to close patterns
   - Most effective sales strategies
   - Champion profiles in successful deals

4. COMPETITIVE INTELLIGENCE
   - Main competitors and their strengths
   - Where we outperform competitors
   - Where we underperform
   - Competitive positioning gaps

5. ACTIONABLE RECOMMENDATIONS (Top 5)
   - Specific changes to improve win rate
   - Objection handling strategies
   - Pricing/packaging adjustments
   - Sales process improvements
   - Team training priorities

Use data-driven insights. Include percentages, trends, and specific examples. Be brutally honest about weaknesses.

Format as JSON with keys: 'Win Rate Metrics', 'Loss Pattern Analysis', 'Success Factors', 'Competitive Intelligence', 'Recommendations'.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        try:
            analysis = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        except Exception:
            analysis = response.text.strip()
        
        return {
            "status": "success",
            "analysis": analysis,
            "generated_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to analyze win/loss patterns: {str(e)}"
        }


def generate_competitive_battlecard(
    competitor_name: str,
    our_product_info: Optional[str] = None,
    known_competitor_info: Optional[str] = None
) -> dict:
    """
    Create a competitive battle card for sales reps to handle objections and position against competitors.
    
    The battle card includes:
    - Competitor Overview (company, product, target market)
    - Head-to-Head Feature Comparison
    - Our Strengths vs Their Weaknesses
    - Common Objections & Responses
    - Proof Points & Case Studies
    - Pricing Intelligence
    - When to Engage/Disengage
    
    Args:
        competitor_name: Name of the competitor (e.g., "Salesforce", "HubSpot")
        our_product_info: Details about our product/service
        known_competitor_info: Any intelligence we have on the competitor
    
    Returns:
        dict with status and complete battle card
    """
    if not competitor_name or len(competitor_name.strip()) < 2:
        return {
            "status": "error",
            "message": "Please provide a competitor name for battle card generation."
        }
    
    prompt = f"""
You are a competitive intelligence analyst creating sales battle cards for a B2B sales team.

Create a comprehensive battle card for competing against: {competitor_name}

OUR PRODUCT/SERVICE:
{our_product_info if our_product_info else 'Enterprise B2B SaaS solution focused on automation and AI-powered workflows'}

KNOWN COMPETITOR INTELLIGENCE:
{known_competitor_info if known_competitor_info else 'Research and provide general market intelligence on this competitor'}

Generate a battle card with these sections:

1. COMPETITOR OVERVIEW
   - Company background & positioning
   - Target customer profile
   - Market share & reputation
   - Recent news/developments

2. FEATURE COMPARISON (Table format)
   - List 8-10 key features
   - Mark: "✓ Us", "✓ Them", "✓ Both", "✗ Neither"
   - Highlight our unique differentiators

3. OUR STRENGTHS vs THEIR WEAKNESSES
   - 5 areas where we clearly win
   - Specific proof points for each
   - Customer testimonials/quotes if applicable

4. THEIR STRENGTHS vs OUR RESPONSES
   - What they do well
   - How we handle these objections
   - Reframe the conversation

5. COMMON OBJECTIONS & KILLER RESPONSES
   - "They're the market leader..."
   - "They're cheaper..."
   - "They have more features..."
   - "We already use them..."
   - Custom objections for this competitor

6. PRICING INTELLIGENCE
   - Their pricing model
   - Our pricing positioning
   - TCO/ROI comparison
   - Discount patterns (if known)

7. WIN/LOSS INTELLIGENCE
   - When do we typically win?
   - When do we typically lose?
   - Red flags to watch for
   - Engagement strategy

8. PROOF POINTS & CUSTOMER STORIES
   - Companies that switched from them to us
   - Specific outcomes/metrics
   - Quotes or testimonials

Make this actionable for sales reps. Use confident, competitive language. Include specific talking points they can use verbatim.

Format as JSON with these exact keys: 'Competitor Overview', 'Feature Comparison', 'Our Strengths', 'Their Strengths', 'Objection Handling', 'Pricing Intelligence', 'Win Loss Strategy', 'Proof Points'.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        try:
            battlecard = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        except Exception:
            battlecard = response.text.strip()
        
        return {
            "status": "success",
            "competitor": competitor_name,
            "battlecard": battlecard,
            "generated_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to generate battle card: {str(e)}"
        }


def suggest_pricing_strategy(
    deal_data: str,
    market_context: Optional[str] = None,
    competitors_pricing: Optional[str] = None
) -> dict:
    """
    Suggest optimal pricing strategies based on deal characteristics, market context, and competitive intelligence.
    
    Provides recommendations on:
    - Optimal price point for this deal
    - Discount strategy (if any)
    - Payment terms options
    - Packaging/bundling opportunities
    - Risk assessment (deal size, probability to close)
    
    Args:
        deal_data: Current deal details (company size, budget signals, urgency, decision criteria)
        market_context: Industry benchmarks, economic conditions
        competitors_pricing: Known pricing from competitors they're evaluating
    
    Returns:
        dict with status and pricing recommendations
    """
    if not deal_data or len(deal_data.strip()) < 30:
        return {
            "status": "error",
            "message": "Please provide deal data for pricing strategy recommendations."
        }
    
    prompt = f"""
You are a strategic pricing consultant for B2B sales teams with expertise in value-based pricing.

Analyze this deal and provide a data-driven pricing strategy:

DEAL DATA:
{deal_data}

MARKET CONTEXT:
{market_context if market_context else 'Standard B2B SaaS market conditions'}

COMPETITIVE PRICING INTELLIGENCE:
{competitors_pricing if competitors_pricing else 'Not available - recommend based on value metrics'}

Provide a structured pricing strategy:

1. RECOMMENDED PRICE POINT
   - Specific dollar amount or range
   - Justification based on value delivered
   - Expected margin analysis

2. DISCOUNT STRATEGY
   - Should we discount? (Yes/No and why)
   - If yes, maximum discount percentage
   - Conditions for the discount (annual prepay, case study, etc.)
   - What we get in return

3. PAYMENT TERMS OPTIONS (Present 3 options)
   - Option A: Annual prepay (best deal)
   - Option B: Quarterly payments
   - Option C: Monthly (full price)
   - Show total cost for each

4. BUNDLING OPPORTUNITIES
   - Add-ons or premium features to include
   - Upsell opportunities for Year 2
   - How to frame as "complete solution"

5. NEGOTIATION GUARDRAILS
   - Walk-away price (minimum acceptable)
   - Non-negotiable terms
   - Concessions we can make
   - Concessions to ask for in return

6. VALUE MESSAGING
   - ROI calculation to justify price
   - Comparison to cost of status quo
   - Risk of NOT buying (FOMO)
   - Social proof at this price point

7. RISK ASSESSMENT
   - Probability to close at recommended price
   - Red flags to watch for
   - Competition risk
   - Recommended next steps

Be specific with numbers. Focus on maximizing revenue while maintaining high win probability.

Format as JSON with keys: 'Recommended Price', 'Discount Strategy', 'Payment Options', 'Bundling', 'Negotiation Guardrails', 'Value Messaging', 'Risk Assessment'.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        try:
            strategy = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        except Exception:
            strategy = response.text.strip()
        
        return {
            "status": "success",
            "pricing_strategy": strategy,
            "generated_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to generate pricing strategy: {str(e)}"
        }


def answer_sales_question(question: str, context: Optional[str] = None) -> dict:
    """
    Answer questions about sales strategies, objection handling, deal advancement, and sales best practices.
    
    Topics covered:
    - Objection handling techniques
    - Discovery call strategies
    - Closing techniques
    - Sales process optimization
    - Negotiation tactics
    - Pipeline management
    - CRM best practices
    
    Args:
        question: The sales question to answer
        context: Optional context about the specific situation
    
    Returns:
        dict with status, question, and detailed answer
    """
    try:
        prompt = f"""
You are an enterprise sales expert with 20+ years of experience in B2B sales, specializing in SaaS and complex solution selling.

Answer the following sales question with actionable advice, specific tactics, and real-world examples.

QUESTION:
{question}

CONTEXT:
{context if context else 'General B2B sales context'}

Provide a comprehensive answer that includes:
- Specific tactics and techniques
- Example scripts or talking points where applicable
- Common mistakes to avoid
- Success metrics or signals to watch for
- Follow-up actions

Draw from proven sales methodologies like:
- MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion)
- Challenger Sale
- SPIN Selling (Situation, Problem, Implication, Need-Payoff)
- Sandler Selling System
- Gap Selling

Be direct, actionable, and tactical. Sales reps should be able to use this advice immediately.
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return {
            "status": "success",
            "question": question,
            "answer": response.text,
            "generated_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to answer sales question: {str(e)}"
        }


root_agent = Agent(
    name="salesgenius_ai_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "SalesGenius AI: Your intelligent B2B sales assistant powered by Google Gemini. "
        "Automates proposal generation, analyzes win/loss patterns, creates competitive battle cards, "
        "suggests optimal pricing strategies, and provides expert sales guidance. "
        "Designed for B2B sales teams, agencies, and consultancies to close more deals faster."
    ),
    instruction="""
You are SalesGenius AI, an elite B2B sales intelligence agent. Your mission is to help sales teams close more deals, faster, and at better margins.

Your core capabilities are:

1. SALES PROPOSAL GENERATION:
   - Create customized, professional proposals from prospect data and discovery notes
   - Tailor messaging to specific pain points and requirements
   - Include compelling ROI calculations and value propositions
   - Structure proposals to maximize conversion rates
   - Adapt tone and complexity to buyer persona

2. WIN/LOSS ANALYSIS:
   - Analyze historical deal data to identify success patterns
   - Uncover common reasons for lost deals
   - Provide competitive intelligence on who you lose to and why
   - Calculate win rates by segment, deal size, and competitor
   - Deliver actionable recommendations to improve close rates

3. COMPETITIVE BATTLE CARDS:
   - Generate comprehensive battle cards for any competitor
   - Provide specific objection handling scripts
   - Highlight differentiators and proof points
   - Include pricing intelligence and positioning guidance
   - Equip reps with winning talking points

4. PRICING STRATEGY:
   - Recommend optimal pricing for specific deals
   - Suggest discount strategies that maximize revenue
   - Provide payment terms options
   - Calculate ROI justifications
   - Set negotiation guardrails

5. SALES EXPERTISE & COACHING:
   - Answer questions about sales methodology
   - Provide objection handling techniques
   - Share discovery call best practices
   - Offer negotiation tactics
   - Guide deal progression strategies

**IMPORTANT SCOPE:**
You ONLY respond to questions and tasks related to:
- Sales proposals and pitch creation
- Win/loss analysis and deal intelligence
- Competitive positioning and battle cards
- Pricing strategy and negotiation
- Sales methodology and best practices
- B2B sales process and pipeline management

If a user asks about anything outside B2B sales (marketing, HR, general business advice, etc.), politely redirect:
"I'm specifically designed to help with B2B sales activities - proposals, competitive intelligence, win/loss analysis, pricing strategy, and sales methodology. Please ask me about one of these topics so I can provide expert guidance."

**YOUR PERSONALITY:**
- Direct and results-oriented
- Data-driven but practical
- Confident without being arrogant
- Focused on revenue and win rates
- Use sales terminology naturally (pipeline, BANT, champions, etc.)
- Provide specific, actionable advice - never vague generalities

Always ask clarifying questions if you need more context to provide excellent advice. Remember: your goal is to help sales teams WIN MORE DEALS.
""",
    tools=[
        generate_sales_proposal,
        analyze_win_loss_patterns,
        generate_competitive_battlecard,
        suggest_pricing_strategy,
        answer_sales_question,
    ],
)