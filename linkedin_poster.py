"""
LinkedIn Auto-Poster
מודול לפרסום אוטומטי של פוסטים ללינקדין
"""

import os
import requests
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()


class LinkedInPoster:
    """Class to handle LinkedIn post publishing"""
    
    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.user_id = os.getenv("LINKEDIN_USER_ID")
        self.api_base = "https://api.linkedin.com/v2"
        
        if not self.access_token:
            raise ValueError("❌ LINKEDIN_ACCESS_TOKEN לא נמצא ב-.env")
        if not self.user_id:
            raise ValueError("❌ LINKEDIN_USER_ID לא נמצא ב-.env")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
    
    def post_to_linkedin(self, post_text: str, visibility: str = "PUBLIC") -> Dict:
        """
        Post content to LinkedIn
        
        Args:
            post_text: The post content
            visibility: Post visibility (PUBLIC, CONNECTIONS)
            
        Returns:
            Response dictionary with status and post URL
        """
        
        # Prepare the post payload
        payload = {
            "author": f"urn:li:person:{self.user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": post_text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        try:
            # Make the API request
            response = requests.post(
                f"{self.api_base}/ugcPosts",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                post_id = response.headers.get("X-RestLi-Id")
                return {
                    "success": True,
                    "message": "✅ הפוסט פורסם בהצלחה!",
                    "post_id": post_id,
                    "post_url": f"https://www.linkedin.com/feed/update/{post_id}"
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "message": f"❌ שגיאה בפרסום: {response.status_code}",
                    "error": error_data
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "❌ הבקשה פגה (timeout)"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"❌ שגיאת רשת: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ שגיאה לא צפויה: {str(e)}"
            }
    
    def get_user_profile(self) -> Optional[Dict]:
        """Get LinkedIn user profile info"""
        try:
            response = requests.get(
                f"{self.api_base}/me",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test if LinkedIn API connection works"""
        try:
            profile = self.get_user_profile()
            return profile is not None
        except:
            return False


def setup_linkedin_auth():
    """
    הדרכה להגדרת אישורי LinkedIn API
    """
    print("=" * 70)
    print("🔐 הגדרת חיבור ל-LinkedIn API")
    print("=" * 70)
    print("\nכדי להשתמש בפרסום אוטומטי, צריך להגדיר LinkedIn App:")
    print("\n📝 שלבים:")
    print("1. היכנס ל-https://www.linkedin.com/developers/apps")
    print("2. לחץ על 'Create app'")
    print("3. מלא את הפרטים:")
    print("   - App name: LinkedIn Post Generator")
    print("   - LinkedIn Page: בחר את הדף שלך (או צור חדש)")
    print("   - Privacy policy URL: אפשר להשתמש ב-https://example.com/privacy")
    print("   - App logo: העלה לוגו כלשהו")
    print("\n4. בטאב 'Auth', הוסף את הPermissions הבאים:")
    print("   ✓ w_member_social (פרסום פוסטים)")
    print("   ✓ r_liteprofile (קריאת פרופיל)")
    print("\n5. בטאב 'Auth', העתק:")
    print("   - Client ID")
    print("   - Client Secret")
    print("\n6. הוסף Redirect URL:")
    print("   http://localhost:3000/auth/linkedin/callback")
    print("\n7. צור Access Token:")
    print("   - לחץ על 'Request access token'")
    print("   - בחר בהרשאות הנדרשות")
    print("   - העתק את ה-Access Token")
    print("\n8. הוסף ל-.env:")
    print("   LINKEDIN_ACCESS_TOKEN=your_access_token")
    print("   LINKEDIN_USER_ID=your_user_id")
    print("\n⚠️  שים לב: Access token תקף ל-60 יום. תצטרך לחדש אותו.")
    print("=" * 70)


if __name__ == "__main__":
    # Test the connection
    try:
        poster = LinkedInPoster()
        print("🔄 בודק חיבור ל-LinkedIn...")
        
        if poster.test_connection():
            print("✅ החיבור ל-LinkedIn תקין!")
            
            profile = poster.get_user_profile()
            if profile:
                print(f"\n👤 מחובר כ: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
        else:
            print("❌ החיבור נכשל. בדוק את ה-Access Token")
            print("\n")
            setup_linkedin_auth()
            
    except ValueError as e:
        print(str(e))
        print("\n")
        setup_linkedin_auth()