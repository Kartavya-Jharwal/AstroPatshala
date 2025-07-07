from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uvicorn
from pathlib import Path

from chaldean_calculator import ChaldeanNumerology
from models import NumerologyRequest, CompatibilityRequest, QuickCalculationRequest

# Initialize FastAPI app
app = FastAPI(
    title="Chaldean Numerology Calculator",
    description="A comprehensive web application for Chaldean numerology calculations and interpretations",
    version="1.0.0"
)

# Initialize the calculator
calculator = ChaldeanNumerology()

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
