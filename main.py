from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uvicorn
from pathlib import Path

from chaldean_calculator import ChaldeanNumerology
from models import NumerologyRequest, CompatibilityRequest, QuickCalculationRequest
from text_normalizer import TextNormalizer
from session_manager import SessionManager

# Initialize FastAPI app
app = FastAPI(
    title="Chaldean Numerology Calculator",
    description="A comprehensive web application for Chaldean numerology calculations and interpretations",
    version="1.0.0"
)

# Initialize the calculator and support systems
calculator = ChaldeanNumerology()
text_normalizer = TextNormalizer()
session_manager = SessionManager()

# Create templates directory if it doesn't exist
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create static directory if it doesn't exist
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with the main calculator form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page explaining Chaldean numerology"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.post("/calculate")
async def calculate_numerology(request: NumerologyRequest):
    """Calculate full numerology report"""
    try:
        birth_date = datetime.strptime(request.birth_date, '%Y-%m-%d')
        report = calculator.generate_full_report(request.name, birth_date)
        return JSONResponse(content=report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/calculate-form")
async def calculate_numerology_form(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...)
):
    """Calculate numerology from form submission"""
    try:
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
        report = calculator.generate_full_report(name, birth_date_obj)
        return templates.TemplateResponse(
            "report.html", 
            {"request": request, "report": report}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": str(e)}
        )

@app.post("/compatibility")
async def calculate_compatibility(request: CompatibilityRequest):
    """Calculate compatibility between two people"""
    try:
        person1_birth = datetime.strptime(request.person1_birth_date, '%Y-%m-%d')
        person2_birth = datetime.strptime(request.person2_birth_date, '%Y-%m-%d')
        
        # Generate reports for both people
        report1 = calculator.generate_full_report(request.person1_name, person1_birth)
        report2 = calculator.generate_full_report(request.person2_name, person2_birth)
        
        # Calculate detailed compatibility
        name_compatibility = calculator.calculate_compatibility(
            report1["name_number"]["reduced"],
            report2["name_number"]["reduced"]
        )
        birth_compatibility = calculator.calculate_compatibility(
            report1["birth_number"]["number"],
            report2["birth_number"]["number"]
        )
        destiny_compatibility = calculator.calculate_compatibility(
            report1["destiny_number"]["reduced"],
            report2["destiny_number"]["reduced"]
        )
        
        compatibility_report = {
            "person1": report1,
            "person2": report2,
            "compatibility": {
                "name_numbers": name_compatibility,
                "birth_numbers": birth_compatibility,
                "destiny_numbers": destiny_compatibility,
                "overall_rating": "High" if any([
                    name_compatibility["compatible"],
                    birth_compatibility["compatible"],
                    destiny_compatibility["compatible"]
                ]) else "Moderate"
            }
        }
        
        return JSONResponse(content=compatibility_report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/compatibility", response_class=HTMLResponse)
async def compatibility_page(request: Request):
    """Compatibility calculator page"""
    return templates.TemplateResponse("compatibility.html", {"request": request})

@app.post("/quick-calculate")
async def quick_calculate(request: QuickCalculationRequest):
    """Quick calculation for any text"""
    try:
        compound, reduced, letter_values = calculator.calculate_name_number(request.text)
        interpretation = calculator.get_number_interpretation(reduced)
        
        result = {
            "text": request.text,
            "compound_number": compound,
            "reduced_number": reduced,
            "letter_breakdown": list(zip(list(request.text.upper()), letter_values)),
            "interpretation": interpretation,
            "compound_meaning": calculator.get_compound_interpretation(compound) if compound > 9 else None
        }
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/chart")
async def get_chaldean_chart():
    """Get the Chaldean numerology chart"""
    return JSONResponse(content={
        "chart": calculator.CHALDEAN_CHART,
        "meanings": calculator.NUMBER_MEANINGS,
        "compound_meanings": calculator.COMPOUND_MEANINGS
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/smart-calculate", response_class=HTMLResponse)
async def smart_calculate(request: Request, natural_input: str = Form(...)):
    """
    Smart calculation endpoint that processes natural language input.
    Handles typos, extracts name and date, and provides quick calculations.
    """
    try:
        # Process natural language input
        name, birth_date = nlp_processor.extract_name_and_date(natural_input)
        
        # Validate inputs
        validation = nlp_processor.validate_input(name, birth_date)
        
        if not validation['name_valid'] or not validation['date_valid']:
            # Return form with suggestions
            context = {
                "request": request,
                "error": "Could not parse your input completely",
                "suggestions": validation['suggestions'],
                "warnings": validation.get('warnings', []),
                "parsed_name": name if name else "",
                "parsed_date": birth_date.strftime('%Y-%m-%d') if birth_date else ""
            }
            return templates.TemplateResponse("index.html", context)
        
        # Create or get user session
        session = session_manager.create_or_get_user_session(name, birth_date)
        
        # Check for recent calculations
        recent_calcs = session_manager.get_recent_calculations(1)
        if recent_calcs:
            # Return cached result if very recent (within 5 minutes)
            last_calc = recent_calcs[-1]
            calc_time = datetime.fromisoformat(last_calc['timestamp'])
            if (datetime.now() - calc_time).total_seconds() < 300:  # 5 minutes
                context = {
                    "request": request,
                    "report": last_calc['data'],
                    "cached": True,
                    "user_summary": session_manager.get_user_summary()
                }
                return templates.TemplateResponse("report.html", context)
        
        # Perform new calculation
        report = calculator.generate_comprehensive_report(name, birth_date)
        
        # Save calculation to session
        session_manager.add_calculation(report)
        
        context = {
            "request": request,
            "report": report,
            "cached": False,
            "user_summary": session_manager.get_user_summary()
        }
        return templates.TemplateResponse("report.html", context)
        
    except Exception as e:
        context = {
            "request": request,
            "error": f"An error occurred: {str(e)}",
            "suggestions": ["Please try rephrasing your input", "Use format: 'Name, Date' or 'My name is [Name] born [Date]'"]
        }
        return templates.TemplateResponse("index.html", context)

@app.get("/quick-lookup")
async def quick_lookup(request: Request, name: str = ""):
    """
    Quick lookup endpoint for finding existing users by name.
    """
    try:
        matches = session_manager.find_user_by_name(name, fuzzy=True) if name else []
        
        # Format matches for display
        user_suggestions = []
        for match in matches[:5]:  # Limit to top 5 matches
            summary = session_manager.get_user_summary(match['user_id'])
            user_suggestions.append({
                'name': match['name'],
                'birth_date': match['birth_date'],
                'access_count': match.get('access_count', 0),
                'quick_numbers': summary.get('quick_numbers', {}),
                'last_access': match['last_access']
            })
        
        return JSONResponse({
            "matches": user_suggestions,
            "total_users": len(session_manager.sessions)
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/load-user")
async def load_user(request: Request, user_name: str = Form(...), user_birth_date: str = Form(...)):
    """
    Load a specific user's most recent calculation.
    """
    try:
        # Parse birth date
        birth_date = datetime.strptime(user_birth_date, '%Y-%m-%d')
        
        # Get user session
        session = session_manager.create_or_get_user_session(user_name, birth_date)
        
        # Get most recent calculation
        recent_calcs = session_manager.get_recent_calculations(1)
        if recent_calcs:
            context = {
                "request": request,
                "report": recent_calcs[-1]['data'],
                "cached": True,
                "user_summary": session_manager.get_user_summary()
            }
            return templates.TemplateResponse("report.html", context)
        else:
            # No cached calculation, generate new one
            report = calculator.generate_comprehensive_report(user_name, birth_date)
            session_manager.add_calculation(report)
            
            context = {
                "request": request,
                "report": report,
                "cached": False,
                "user_summary": session_manager.get_user_summary()
            }
            return templates.TemplateResponse("report.html", context)
            
    except Exception as e:
        context = {
            "request": request,
            "error": f"Error loading user: {str(e)}"
        }
        return templates.TemplateResponse("index.html", context)

@app.get("/users-admin")
async def users_admin(request: Request):
    """
    Admin endpoint to view all users (for debugging/management).
    """
    try:
        all_users = session_manager.get_all_users_summary()
        context = {
            "request": request,
            "users": all_users,
            "total_count": len(all_users)
        }
        return templates.TemplateResponse("users_admin.html", context)
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

def main():
    """Run the application"""
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
