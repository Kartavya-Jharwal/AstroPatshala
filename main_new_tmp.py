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
from nlp_processor import NLPProcessor

app = FastAPI(
    title="Chaldean Numerology Calculator",
    description="A comprehensive web application for Chaldean numerology calculations and interpretations",
    version="1.0.0"
)

calculator = ChaldeanNumerology()
text_normalizer = TextNormalizer()
session_manager = SessionManager()
nlp_processor = NLPProcessor()

Path("templates").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})

@app.post('/calculate')
async def calculate_numerology(request: NumerologyRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, '%Y-%m-%d')
        report = calculator.generate_full_report(request.name, birth_date)
        return JSONResponse(report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/calculate-form')
async def calculate_numerology_form(request: Request, name: str = Form(...), birth_date: str = Form(...)):
    try:
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
        report = calculator.generate_full_report(name, birth_date_obj)
        return templates.TemplateResponse('report.html', {'request': request, 'report': report})
    except Exception as e:
        return templates.TemplateResponse('index.html', {'request': request, 'error': str(e)})

@app.post('/compatibility')
async def calculate_compatibility(request: CompatibilityRequest):
    try:
        p1_birth = datetime.strptime(request.person1_birth_date, '%Y-%m-%d')
        p2_birth = datetime.strptime(request.person2_birth_date, '%Y-%m-%d')
        r1 = calculator.generate_full_report(request.person1_name, p1_birth)
        r2 = calculator.generate_full_report(request.person2_name, p2_birth)
        name_comp = calculator.calculate_compatibility(r1['core_numbers']['name_number']['reduced'], r2['core_numbers']['name_number']['reduced'])
        birth_comp = calculator.calculate_compatibility(r1['core_numbers']['birth_number']['number'], r2['core_numbers']['birth_number']['number'])
        destiny_comp = calculator.calculate_compatibility(r1['core_numbers']['destiny_number']['reduced'], r2['core_numbers']['destiny_number']['reduced'])
        overall = 'High' if any([name_comp['compatible'], birth_comp['compatible'], destiny_comp['compatible']]) else 'Moderate'
        return JSONResponse({
            'person1': r1,
            'person2': r2,
            'compatibility': {
                'name_numbers': name_comp,
                'birth_numbers': birth_comp,
                'destiny_numbers': destiny_comp,
                'overall_rating': overall
            }
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/compatibility', response_class=HTMLResponse)
async def compatibility_page(request: Request):
    return templates.TemplateResponse('compatibility.html', {'request': request})

@app.post('/quick-calculate')
async def quick_calculate(request: QuickCalculationRequest):
    try:
        compound, reduced, letter_values = calculator.calculate_name_number(request.text)
        interpretation = calculator.get_number_interpretation(reduced)
        return JSONResponse({
            'text': request.text,
            'compound_number': compound,
            'reduced_number': reduced,
            'letter_breakdown': list(zip(list(request.text.upper()), letter_values)),
            'interpretation': interpretation,
            'compound_meaning': calculator.get_compound_interpretation(compound) if compound > 9 else None
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/api/chart')
async def get_chaldean_chart():
    return JSONResponse({
        'chart': calculator.CHALDEAN_CHART,
        'meanings': calculator.NUMBER_MEANINGS,
        'compound_meanings': calculator.COMPOUND_MEANINGS
    })

@app.get('/health')
async def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

@app.post('/smart-calculate', response_class=HTMLResponse)
async def smart_calculate(request: Request, natural_input: str = Form(...)):
    try:
        name, birth_date = nlp_processor.extract_name_and_date(natural_input)
        validation = nlp_processor.validate_input(name, birth_date)
        if not validation['name_valid'] or not validation['date_valid']:
            return templates.TemplateResponse('index.html', {
                'request': request,
                'error': 'Could not parse your input completely',
                'suggestions': validation['suggestions'],
                'warnings': validation.get('warnings', []),
                'parsed_name': name or '',
                'parsed_date': birth_date.strftime('%Y-%m-%d') if birth_date else ''
            })
        if birth_date is None:
            raise ValueError('Birth date parsing failed')
        session_manager.create_or_get_user_session(name, birth_date)
        recent = session_manager.get_recent_calculations(1)
        if recent:
            last = recent[-1]
            ts = datetime.fromisoformat(last['timestamp'])
            if (datetime.now() - ts).total_seconds() < 300:
                return templates.TemplateResponse('report.html', {
                    'request': request,
                    'report': last['data'],
                    'cached': True,
                    'user_summary': session_manager.get_user_summary()
                })
        report = calculator.generate_comprehensive_report(name, birth_date)
        session_manager.add_calculation(report)
        return templates.TemplateResponse('report.html', {
            'request': request,
            'report': report,
            'cached': False,
            'user_summary': session_manager.get_user_summary()
        })
    except Exception as e:
        return templates.TemplateResponse('index.html', {
            'request': request,
            'error': f'An error occurred: {str(e)}',
            'suggestions': [
                'Please try rephrasing your input',
                "Use format: 'Name, Date' or 'My name is [Name] born [Date]'"
            ]
        })

@app.get('/quick-lookup')
async def quick_lookup(request: Request, name: str = ''):
    try:
        matches = session_manager.find_user_by_name(name) if name else []
        suggestions = []
        for m in matches[:5]:
            summary = session_manager.get_user_summary(m['user_id'])
            suggestions.append({
                'name': m['name'],
                'birth_date': m['birth_date'],
                'calculation_count': m['calculation_count'],
                'quick_numbers': summary.get('quick_numbers', {}),
                'last_seen': m['last_seen']
            })
        return JSONResponse({'matches': suggestions, 'total_users': len(session_manager.users)})
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

@app.post('/load-user')
async def load_user(request: Request, user_name: str = Form(...), user_birth_date: str = Form(...)):
    try:
        birth_date = datetime.strptime(user_birth_date, '%Y-%m-%d')
        session_manager.create_or_get_user_session(user_name, birth_date)
        recent = session_manager.get_recent_calculations(1)
        if recent:
            return templates.TemplateResponse('report.html', {
                'request': request,
                'report': recent[-1]['data'],
                'cached': True,
                'user_summary': session_manager.get_user_summary()
            })
        report = calculator.generate_comprehensive_report(user_name, birth_date)
        session_manager.add_calculation(report)
        return templates.TemplateResponse('report.html', {
            'request': request,
            'report': report,
            'cached': False,
            'user_summary': session_manager.get_user_summary()
        })
    except Exception as e:
        return templates.TemplateResponse('index.html', {'request': request, 'error': f'Error loading user: {str(e)}'})

@app.get('/users-admin', response_class=HTMLResponse)
async def users_admin(request: Request):
    try:
        users = session_manager.get_all_users_summary()
        return templates.TemplateResponse('users_admin.html', {
            'request': request,
            'users': users,
            'total_count': len(users)
        })
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


def main():
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='info')

if __name__ == '__main__':
    main()
