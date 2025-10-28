import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv
import yaml
import json
from pathlib import Path
import hashlib

load_dotenv()

# ==== LLM Configuration ====
# Gemini keeps routing to Vertex AI (503 errors) with multi-agent crews
# Best option: Use OpenAI (very cheap) or wait for Gemini to be available

if os.getenv("OPENAI_API_KEY"):
    gemini_llm = LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )
    print("✅ Using OpenAI GPT-4o-mini (recommended)")
elif os.getenv("GROQ_API_KEY"):
    gemini_llm = LLM(
        model="groq/llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    print("⚠️  Using Groq (free but has rate limits)")
else:
    gemini_llm = LLM(
        model="gemini/gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
        timeout=90,
        max_retries=3
    )
    print("⚠️  Using Gemini (may hit Vertex AI rate limits)")
    print("💡 For better reliability, add OPENAI_API_KEY to .env")

# ==== כלים חיצוניים (עם קאשינג + Fallback) ====
class CachedResearchTool:
    def __init__(self):
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.scrape_tool = ScrapeWebsiteTool(timeout=30, retries=2)
        self.serper_tool = SerperDevTool()

    def _cache_file(self, key):
        h = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return self.cache_dir / f"{h}.json"

    def fetch(self, input_url_or_topic):
        f = self._cache_file(input_url_or_topic)
        if f.exists():
            with open(f, "r", encoding="utf-8") as cf:
                return json.load(cf)["content"]
        # ניסיון scrap מהאתר
        try:
            content = self.scrape_tool.run({'website_url': input_url_or_topic})
            with open(f, "w", encoding="utf-8") as cf:
                json.dump({"content": content}, cf, ensure_ascii=False)
            return content
        except Exception as e:
            print(f"❌ ScrapeWebsiteTool failed: {e}")
        # חיפוש Google
        try:
            result = self.serper_tool.run({'search_query': input_url_or_topic})
            with open(f, "w", encoding="utf-8") as cf:
                json.dump({"content": result}, cf, ensure_ascii=False)
            return result
        except Exception as e:
            print(f"❌ SerperDevTool failed: {e}")
        # Fallback חסר הצלחה
        return "לא נמצאה תוצאה. נסה מונח אחר או בדוק את החיבור."

# ==== קונפיג סגנון ====
def load_writing_style():
    style_file = Path("config/writing_style.json")
    if style_file.exists():
        with open(style_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"examples": [], "style_guidelines": ""}

def save_writing_style(examples, guidelines):
    style_file = Path("config/writing_style.json")
    style_file.parent.mkdir(exist_ok=True)
    with open(style_file, "w", encoding="utf-8") as f:
        json.dump({
            "examples": examples,
            "style_guidelines": guidelines
        }, f, ensure_ascii=False, indent=2)

# ==== טעינת הגדרות YAML ====
with open("config/agents.yaml", "r", encoding="utf-8") as f:
    agents_config = yaml.safe_load(f)
with open("config/tasks.yaml", "r", encoding="utf-8") as f:
    tasks_config = yaml.safe_load(f)

# ==== אייג'נטים ====
style_analyzer = Agent(
    role=agents_config['style_analyzer']['role'],
    goal=agents_config['style_analyzer']['goal'],
    backstory=agents_config['style_analyzer']['backstory'],
    verbose=True,
    llm=gemini_llm,
)

# Agent without tools - will work from context provided
content_researcher = Agent(
    role=agents_config['content_researcher']['role'],
    goal=agents_config['content_researcher']['goal'],
    backstory=agents_config['content_researcher']['backstory'],
    verbose=True,
    llm=gemini_llm,
)

viral_writer = Agent(
    role=agents_config['viral_writer']['role'],
    goal=agents_config['viral_writer']['goal'],
    backstory=agents_config['viral_writer']['backstory'],
    verbose=True,
    llm=gemini_llm,
)

engagement_optimizer = Agent(
    role=agents_config['engagement_optimizer']['role'],
    goal=agents_config['engagement_optimizer']['goal'],
    backstory=agents_config['engagement_optimizer']['backstory'],
    verbose=True,
    llm=gemini_llm,
)

viral_validator = Agent(
    role=agents_config['viral_validator']['role'],
    goal=agents_config['viral_validator']['goal'],
    backstory=agents_config['viral_validator']['backstory'],
    verbose=True,
    llm=gemini_llm,
)

# ==== בניית משימות ====
def create_tasks(content_url_or_topic, writing_style_data):
    research_task = Task(
        description=tasks_config['research_task']['description'].format(content_input=content_url_or_topic),
        agent=content_researcher,
        expected_output=tasks_config['research_task']['expected_output'],
    )
    style_task = Task(
        description=tasks_config['style_task']['description'].format(
            style_examples=json.dumps(writing_style_data.get('examples', []), ensure_ascii=False),
            style_guidelines=writing_style_data.get('style_guidelines', '')
        ),
        agent=style_analyzer,
        expected_output=tasks_config['style_task']['expected_output'],
        context=[research_task]
    )
    writer_task = Task(
        description=tasks_config['writer_task']['description'],
        agent=viral_writer,
        expected_output=tasks_config['writer_task']['expected_output'],
        context=[research_task, style_task]
    )
    viral_validator_task = Task(
        description=tasks_config['viral_validator_task']['description'],
        agent=viral_validator,
        expected_output=tasks_config['viral_validator_task']['expected_output'],
        context=[writer_task]
    )
    optimization_task = Task(
        description=tasks_config['optimization_task']['description'],
        agent=engagement_optimizer,
        expected_output=tasks_config['optimization_task']['expected_output'],
        context=[viral_validator_task]
    )
    return [research_task, style_task, writer_task, viral_validator_task, optimization_task]

def generate_post(content_input, use_existing_style=True):
    writing_style = load_writing_style() if use_existing_style else {"examples": [], "style_guidelines": ""}
    
    # Pre-fetch content using cached tool (outside of agent execution)
    print("📥 מוריד תוכן...")
    researcher = CachedResearchTool()
    research_content = researcher.fetch(content_input)
    print(f"✅ התוכן הורד ({len(research_content)} תווים)")
    
    # Pass the pre-fetched content directly to tasks
    tasks = create_tasks(research_content, writing_style)
    crew = Crew(
        agents=[content_researcher, style_analyzer, viral_writer, viral_validator, engagement_optimizer],
        tasks=tasks,
        verbose=True,
    )
    result = crew.kickoff()
    return result


if __name__ == "__main__":
    # שימוש יכול להיות גם בלינק וגם בנושא
    content = "AI agents and automation trends in 2025"
    try:
        print("🚀 מתחיל ליצור פוסט...")
        result = generate_post(content, use_existing_style=True)
        print("\n" + "="*50)
        print("✅ הפוסט הסופי:")
        print("="*50)
        print(result)
    except Exception as e:
        print(f"\n❌ שגיאה ביצירת הפוסט: {str(e)}")
        print("\nטיפים לפתרון בעיות:")
        print("1. בדוק שה-GEMINI_API_KEY תקין ב-.env")
        print("2. נסה להריץ שוב (לפעמים יש בעיות זמניות ברשת)")
        print("3. אם הבעיה נמשכת, נסה מודל אחר או הקטן את הבקשה")

