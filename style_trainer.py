"""
סקריפט ללימוד סגנון הכתיבה האישי שלך
הזן 3-5 פוסטים מוצלחים שלך והמערכת תלמד את הסגנון
"""

import json
from pathlib import Path

def collect_writing_samples():
    """Collect writing samples from user"""
    print("=" * 60)
    print("🎯 לימוד סגנון כתיבה אישי")
    print("=" * 60)
    print("\nכדי שהמערכת תלמד את סגנון הכתיבה שלך,")
    print("הדבק 3-5 פוסטים מוצלחים שכתבת בלינקדין")
    print("(פוסטים עם הרבה engagement - לייקים, תגובות, שיתופים)\n")
    
    examples = []
    
    while True:
        print(f"\n📝 פוסט מספר {len(examples) + 1}")
        print("-" * 60)
        
        if examples:
            continue_input = input("\nהאם לדבק פוסט נוסף? (y/n): ").strip().lower()
            if continue_input != 'y' and len(examples) >= 3:
                break
        
        print("\nהדבק את הפוסט המלא (לחץ Enter פעמיים כשסיימת):")
        print("-" * 60)
        
        lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        
        post_text = "\n".join(lines).strip()
        
        if not post_text:
            print("❌ לא הוזן טקסט. מדלג...")
            continue
        
        # Get metadata
        print(f"\nכמה לייקים קיבל הפוסט? (אופציונלי, Enter לדילוג): ", end="")
        likes = input().strip()
        
        print(f"כמה תגובות? (אופציונלי, Enter לדילוג): ", end="")
        comments = input().strip()
        
        examples.append({
            "text": post_text,
            "likes": likes if likes else "לא צוין",
            "comments": comments if comments else "לא צוין"
        })
        
        print(f"\n✅ פוסט נשמר! (סה\"כ {len(examples)} פוסטים)")
        
        if len(examples) >= 5:
            print("\n✨ יופי! יש לנו 5 פוסטים. זה מספיק ללמוד את הסגנון שלך.")
            break
    
    return examples

def collect_style_guidelines():
    """Collect explicit style guidelines from user"""
    print("\n" + "=" * 60)
    print("📋 הנחיות סגנון נוספות (אופציונלי)")
    print("=" * 60)
    print("\nיש לך הנחיות ספציפיות לסגנון הכתיבה?")
    print("לדוגמה:")
    print("  - תמיד להתחיל בשאלה")
    print("  - להשתמש באימוג'י בתחילת כל פסקה")
    print("  - לכתוב בטון אישי וחברי")
    print("  - לסיים תמיד בקריאה לפעולה")
    print("\nאם אין, פשוט לחץ Enter\n")
    print("הזן הנחיות (Enter פעמיים כשסיימת):")
    print("-" * 60)
    
    lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if line == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line)
    
    return "\n".join(lines).strip()

def save_style_data(examples, guidelines):
    """Save the writing style data"""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    style_data = {
        "examples": examples,
        "style_guidelines": guidelines,
        "metadata": {
            "num_examples": len(examples),
            "has_guidelines": bool(guidelines)
        }
    }
    
    with open(config_dir / "writing_style.json", "w", encoding="utf-8") as f:
        json.dump(style_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ סגנון הכתיבה נשמר בהצלחה!")
    print("=" * 60)
    print(f"\n📊 סיכום:")
    print(f"   • {len(examples)} דוגמאות פוסטים")
    print(f"   • הנחיות סגנון: {'כן' if guidelines else 'לא'}")
    print(f"   • נשמר ב: config/writing_style.json")
    print("\n🚀 עכשיו אפשר להשתמש ב-agents.py ליצירת פוסטים חדשים!")

def main():
    print("\n🎨 למידת סגנון כתיבה אישי\n")
    
    # Collect samples
    examples = collect_writing_samples()
    
    if not examples:
        print("\n❌ לא נוספו פוסטים. יוצא...")
        return
    
    # Collect guidelines
    guidelines = collect_style_guidelines()
    
    # Save
    save_style_data(examples, guidelines)

if __name__ == "__main__":
    main()