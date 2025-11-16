import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional CORS (keeps it flexible if you later host frontend separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return FileResponse('story_page.html')

class StoryRequest(BaseModel):
    heading: str

class StoryResponse(BaseModel):
    story: str

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GOOGLE_API_KEY environment variable not set."
            )

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = (
            f"Write a short and engaging story (2-3 paragraphs) based on the "
            f"following heading: '{request.heading}'. Use simple Indian Hindi "
            f"with easy words and natural flow, like how people speak in everyday life. "
            f"The story should have a clear beginning, middle, and end, with emotions "
            f"and a small message or moral at the end."
        )

        response = model.generate_content(prompt)

        return StoryResponse(story=response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate story from the AI model."
        )
