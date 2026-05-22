from typing import List, Dict, Any
from google import genai
from app.config import get_settings
from loguru import logger

class GeminiService:
    def __init__(self):
        self.settings = get_settings()
        if self.settings.gemini_api_key:
            self.client = genai.Client(api_key=self.settings.gemini_api_key)
        else:
            self.client = None
            logger.warning("GEMINI_API_KEY is not set. Gemini reports will be unavailable.")

    def generate_stress_report(self, time_points: List[Dict[str, Any]]) -> str:
        if not self.client:
            return "Error: Gemini API key is not configured on the server."

        if not time_points:
            return "No data provided to generate a report."

        # Format data for prompt
        data_summary = []
        for pt in time_points:
            data_summary.append(f"Time: {pt.get('timestamp')}, HR: {pt.get('heartRate')} bpm, Stress Score: {pt.get('stressScore')}, IsStressed: {pt.get('isStressed')}")
        
        formatted_data = "\n".join(data_summary)

        prompt = f"""
You are an expert physiological data analyst and stress management coach. 
Analyze the following daily heart rate and stress score data points for a subject and provide a concise, professional report.

Data Points:
{formatted_data}

Please structure your report using Markdown with the following sections:
1. **Daily Overview**: A brief summary of their overall stress levels and heart rate trends throughout the day.
2. **Key Stress Events**: Identify specific times when stress peaked (if any). Describe the severity and duration.
3. **Recovery & Baseline**: Note periods where the subject successfully recovered and maintained a healthy baseline.
4. **Actionable Recommendations**: Provide 2-3 brief, personalized recommendations to help manage the identified stress patterns.

Keep the report professional, empathetic, and easy to read. Do not hallucinate data that is not provided.
"""
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return f"Error generating report: {str(e)}"

gemini_service = GeminiService()
