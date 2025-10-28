"""
Post Generator UI - יצירת פוסטים ללינקדין עם Reflex
"""

import reflex as rx
from typing import List, Dict
import json
from pathlib import Path
from datetime import datetime
import asyncio
import sys
sys.path.append(str(Path(__file__).parent.parent))
from agents import generate_post

# Database/Storage for posts
class PostHistory:
    def __init__(self):
        self.history_file = Path("data/post_history.json")
        self.history_file.parent.mkdir(exist_ok=True)
        
    def load(self) -> List[Dict]:
        if self.history_file.exists():
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save(self, posts: List[Dict]):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
    
    def add_post(self, post_data: Dict):
        posts = self.load()
        posts.insert(0, post_data)  # Add to beginning
        self.save(posts)

post_db = PostHistory()

class State(rx.State):
    """State management for the app"""
    
    # Input fields
    content_input: str = ""
    is_generating: bool = False
    
    # Current post
    generated_post: str = ""
    generation_time: float = 0.0
    generation_error: str = ""
    
    # Agent progress tracking
    current_agent: str = ""
    agent_progress: str = ""
    
    # Post history
    post_history: List[Dict] = []
    
    # Stats
    total_posts: int = 0
    total_generation_time: float = 0.0
    avg_generation_time: float = 0.0
    
    def load_history(self):
        """Load post history from file"""
        self.post_history = post_db.load()
        self.total_posts = len(self.post_history)
        
        if self.total_posts > 0:
            self.total_generation_time = sum(p.get("generation_time", 0) for p in self.post_history)
            self.avg_generation_time = self.total_generation_time / self.total_posts
    
    async def generate_new_post(self):
        """Generate a new LinkedIn post"""
        if not self.content_input.strip():
            self.generation_error = "❌ אנא הזן URL או נושא"
            return
        
        self.is_generating = True
        self.generated_post = ""
        self.generation_error = ""
        self.current_agent = "מתחיל..."
        self.agent_progress = "מכין את ה-AI Agents..."
        
        try:
            start_time = datetime.now()
            
            # Update progress
            self.current_agent = "🔍 Content Researcher"
            self.agent_progress = "חוקר את התוכן..."
            
            # Generate post using CrewAI agents
            result = await asyncio.to_thread(
                generate_post,
                self.content_input,
                use_existing_style=True
            )
            
            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()
            
            self.current_agent = "✅ הושלם"
            self.agent_progress = "הפוסט נוצר בהצלחה!"
            
            # Extract post text from result
            post_text = str(result)
            
            self.generated_post = post_text
            self.generation_time = generation_time
            
            # Save to history
            post_data = {
                "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "content_input": self.content_input,
                "generated_post": post_text,
                "generation_time": generation_time,
                "timestamp": datetime.now().isoformat(),
                "posted_to_linkedin": False,
                "engagement": {
                    "likes": 0,
                    "comments": 0,
                    "shares": 0
                }
            }
            
            post_db.add_post(post_data)
            self.load_history()
            
        except Exception as e:
            self.generation_error = f"❌ שגיאה ביצירת הפוסט: {str(e)}"
            self.current_agent = "❌ נכשל"
            self.agent_progress = ""
            print(f"Error in generate_new_post: {e}")  # Debug logging
        
        finally:
            self.is_generating = False
    
    def clear_input(self):
        """Clear the input field"""
        self.content_input = ""
        self.generated_post = ""
        self.generation_error = ""
        self.current_agent = ""
        self.agent_progress = ""
    
    def delete_post(self, post_id: str):
        """Delete a post from history"""
        posts = post_db.load()
        posts = [p for p in posts if p.get("id") != post_id]
        post_db.save(posts)
        self.load_history()
    
    def copy_post(self, post_text: str):
        """Copy post to clipboard"""
        # Note: Actual clipboard copy needs JS interop
        return rx.call_script(f"navigator.clipboard.writeText(`{post_text}`)")


def header() -> rx.Component:
    """App header"""
    return rx.box(
        rx.hstack(
            rx.heading(
                "🚀 LinkedIn Post Generator",
                size="8",
                color="blue.600"
            ),
            rx.spacer(),
            rx.badge(
                "Powered by AI Agents",
                color_scheme="green",
                size="2"
            ),
            width="100%",
            align="center"
        ),
        rx.text(
            "יצירת פוסטים ויראליים בעברית עם AI",
            color="gray.600",
            size="3"
        ),
        padding="1.5rem",
        border_bottom="2px solid",
        border_color="gray.200",
        background="white"
    )


def stats_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    """Statistics card component"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(icon, size="6"),
                rx.spacer(),
                rx.badge(title, color_scheme=color, size="1"),
                width="100%"
            ),
            rx.heading(value, size="7", color=f"{color}.600"),
            spacing="2",
            align="start"
        ),
        width="100%"
    )


def stats_section(state: State) -> rx.Component:
    """Stats dashboard section"""
    return rx.box(
        rx.heading("📊 סטטיסטיקות", size="5", margin_bottom="1rem"),
        rx.cond(
            state.total_posts > 0,
            rx.grid(
                stats_card(
                    "פוסטים שנוצרו",
                    state.total_posts,
                    "📝",
                    "blue"
                ),
                stats_card(
                    "זמן יצירה ממוצע",
                    f"{state.avg_generation_time:.1f}s",
                    "⏱️",
                    "green"
                ),
                stats_card(
                    "סה\"כ זמן",
                    f"{state.total_generation_time:.1f}s",
                    "⌚",
                    "purple"
                ),
                stats_card(
                    "פוסטים היום",
                    "0",  # TODO: Calculate today's posts
                    "🎯",
                    "orange"
                ),
                columns="4",
                spacing="4",
                width="100%"
            ),
            rx.box(
                rx.text(
                    "עדיין לא נוצרו פוסטים",
                    color="gray.500",
                    size="4",
                    text_align="center"
                ),
                padding="3rem",
                background="gray.50",
                border_radius="8px",
                width="100%"
            )
        ),
        padding="1.5rem",
        background="white",
        border_radius="8px",
        box_shadow="sm"
    )


def input_section(state: State) -> rx.Component:
    """Main input section for generating posts"""
    return rx.box(
        rx.heading("✍️ יצירת פוסט חדש", size="5", margin_bottom="1rem"),
        rx.vstack(
            rx.text(
                "הזן URL (GitHub, מאמר, כלי AI) או נושא חופשי:",
                size="3",
                color="gray.700",
                margin_bottom="0.5rem"
            ),
            rx.text_area(
                placeholder="לדוגמה: https://github.com/openai/gpt-4 או 'מגמות חדשות ב-AI לשנת 2025'",
                value=state.content_input,
                on_change=State.set_content_input,
                width="100%",
                min_height="120px",
                font_size="16px",
                dir="auto"
            ),
            rx.hstack(
                rx.button(
                    rx.cond(
                        state.is_generating,
                        rx.hstack(
                            rx.spinner(size="2"),
                            rx.text("מייצר פוסט..."),
                            spacing="2"
                        ),
                        rx.hstack(
                            rx.text("🚀"),
                            rx.text("צור פוסט"),
                            spacing="2"
                        )
                    ),
                    on_click=State.generate_new_post,
                    disabled=state.is_generating,
                    size="3",
                    color_scheme="blue",
                    width="200px"
                ),
                rx.button(
                    "🗑️ נקה",
                    on_click=State.clear_input,
                    size="3",
                    variant="outline",
                    color_scheme="gray"
                ),
                spacing="3",
                width="100%"
            ),
            rx.cond(
                state.generation_error != "",
                rx.callout(
                    state.generation_error,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="100%"
                )
            ),
            rx.cond(
                state.is_generating,
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.spinner(size="3"),
                            rx.heading("AI Agents עובדים...", size="4"),
                            spacing="3",
                            align="center"
                        ),
                        rx.divider(),
                        rx.vstack(
                            rx.hstack(
                                rx.text("Agent נוכחי:", weight="bold", size="2"),
                                rx.text(state.current_agent, size="2"),
                                spacing="2"
                            ),
                            rx.text(
                                state.agent_progress,
                                size="2",
                                color="gray.600"
                            ),
                            spacing="2",
                            align="start",
                            width="100%"
                        ),
                        rx.text(
                            "התהליך כולל: חקר תוכן → ניתוח סגנון → כתיבה → ולידציה → אופטימיזציה",
                            size="1",
                            color="gray.500",
                            font_style="italic"
                        ),
                        spacing="3",
                        width="100%",
                        align="start"
                    ),
                    width="100%",
                    background="blue.50"
                )
            ),
            spacing="4",
            width="100%"
        ),
        padding="1.5rem",
        background="white",
        border_radius="8px",
        box_shadow="sm"
    )


def generated_post_section(state: State) -> rx.Component:
    """Display the generated post"""
    return rx.cond(
        state.generated_post != "",
        rx.box(
            rx.heading("✨ הפוסט שנוצר", size="5", margin_bottom="1rem"),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.badge(
                            f"נוצר ב-{state.generation_time:.1f} שניות",
                            color_scheme="green"
                        ),
                        rx.spacer(),
                        rx.button(
                            "📋 העתק",
                            on_click=lambda: State.copy_post(state.generated_post),
                            size="2",
                            variant="soft"
                        ),
                        width="100%"
                    ),
                    rx.divider(),
                    rx.box(
                        rx.text(
                            state.generated_post,
                            white_space="pre-wrap",
                            font_size="16px",
                            line_height="1.7",
                            dir="auto"
                        ),
                        padding="1rem",
                        background="gray.50",
                        border_radius="6px",
                        width="100%"
                    ),
                    spacing="4",
                    width="100%"
                )
            ),
            padding="1.5rem",
            background="white",
            border_radius="8px",
            box_shadow="sm"
        )
    )


def post_history_card(post: Dict) -> rx.Component:
    """Single post history card"""
    # Pre-process data to avoid Var slicing issues
    timestamp_raw = post.get("timestamp", "")
    timestamp = timestamp_raw[:10] if isinstance(timestamp_raw, str) else ""
    
    gen_time = post.get('generation_time', 0)
    gen_time_str = f"{gen_time:.1f}s" if isinstance(gen_time, (int, float)) else "0.0s"
    
    content_input = post.get("content_input", "")
    content_preview = (content_input[:100] + "...") if isinstance(content_input, str) and len(content_input) > 100 else content_input
    
    generated_post = post.get("generated_post", "")
    post_preview = (generated_post[:200] + "...") if isinstance(generated_post, str) and len(generated_post) > 200 else generated_post
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    timestamp,
                    color_scheme="blue",
                    size="1"
                ),
                rx.spacer(),
                rx.badge(
                    gen_time_str,
                    color_scheme="green",
                    size="1"
                ),
                rx.button(
                    "🗑️",
                    on_click=lambda: State.delete_post(post.get("id")),
                    size="1",
                    variant="ghost",
                    color_scheme="red"
                ),
                width="100%",
                align="center"
            ),
            rx.text(
                content_preview,
                color="gray.600",
                size="2",
                font_weight="500"
            ),
            rx.divider(),
            rx.box(
                rx.text(
                    post_preview,
                    size="2",
                    color="gray.700",
                    white_space="pre-wrap",
                    dir="auto"
                ),
                max_height="150px",
                overflow="hidden"
            ),
            rx.hstack(
                rx.button(
                    "📋 העתק",
                    on_click=lambda: State.copy_post(post.get("generated_post", "")),
                    size="2",
                    variant="soft",
                    color_scheme="blue"
                ),
                rx.button(
                    "👁️ צפה מלא",
                    size="2",
                    variant="outline"
                ),
                spacing="2",
                width="100%"
            ),
            spacing="3",
            width="100%",
            align="start"
        ),
        width="100%"
    )


def history_section(state: State) -> rx.Component:
    """Post history section"""
    return rx.box(
        rx.heading("📚 היסטוריית פוסטים", size="5", margin_bottom="1rem"),
        rx.cond(
            state.total_posts > 0,
            rx.grid(
                rx.foreach(
                    state.post_history,
                    post_history_card
                ),
                columns="3",
                spacing="4",
                width="100%"
            ),
            rx.box(
                rx.text(
                    "עדיין לא נוצרו פוסטים",
                    color="gray.500",
                    size="4",
                    text_align="center"
                ),
                padding="3rem",
                background="gray.50",
                border_radius="8px",
                width="100%"
            )
        ),
        padding="1.5rem",
        background="white",
        border_radius="8px",
        box_shadow="sm"
    )


def index() -> rx.Component:
    """Main page"""
    return rx.container(
        header(),
        rx.vstack(
            stats_section(State),
            input_section(State),
            generated_post_section(State),
            history_section(State),
            spacing="6",
            padding_y="2rem",
            width="100%"
        ),
        max_width="1400px",
        padding_x="1rem"
    )


# App configuration
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue"
    )
)

app.add_page(index, on_load=State.load_history)