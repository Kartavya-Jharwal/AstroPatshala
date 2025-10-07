"""
User Session Manager for the numerology application
Handles user logging, session management, and quick access to previous calculations
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class UserRecord:
    """User record for session management"""
    name: str
    birth_date: str
    first_seen: str
    last_seen: str
    calculation_count: int
    search_key: str  # For quick searching


class SessionManager:
    """Manages user sessions and calculations history"""
    
    def __init__(self, data_file: str = "user_sessions.json"):
        self.data_file = data_file
        self.users: Dict[str, UserRecord] = {}
        self.load_users()
    
    def _generate_user_id(self, name: str, birth_date: str) -> str:
        """Generate a unique user ID based on name and birth date"""
        combined = f"{name.lower().strip()}|{birth_date}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    def _generate_search_key(self, name: str) -> str:
        """Generate a search key for fuzzy matching"""
        # Remove spaces, convert to lowercase, keep only letters
        import re
        clean_name = re.sub(r'[^a-zA-Z]', '', name.lower())
        return clean_name
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert dict data back to UserRecord objects
                for user_id, user_data in data.items():
                    self.users[user_id] = UserRecord(**user_data)
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            # Convert UserRecord objects to dict for JSON serialization
            data = {user_id: asdict(user) for user_id, user in self.users.items()}
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def add_or_update_user(self, name: str, birth_date: str) -> str:
        """
        Add a new user or update existing user's last seen time
        
        Args:
            name: User's normalized name
            birth_date: Birth date in YYYY-MM-DD format
            
        Returns:
            User ID
        """
        user_id = self._generate_user_id(name, birth_date)
        current_time = datetime.now().isoformat()
        
        if user_id in self.users:
            # Update existing user
            self.users[user_id].last_seen = current_time
            self.users[user_id].calculation_count += 1
        else:
            # Add new user
            search_key = self._generate_search_key(name)
            self.users[user_id] = UserRecord(
                name=name,
                birth_date=birth_date,
                first_seen=current_time,
                last_seen=current_time,
                calculation_count=1,
                search_key=search_key
            )
        
        self.save_users()
        return user_id
    
    def find_user_by_name(self, search_name: str, limit: int = 5) -> List[Dict]:
        """
        Find users by name using fuzzy matching
        
        Args:
            search_name: Name to search for
            limit: Maximum number of results
            
        Returns:
            List of matching user records
        """
        from fuzzywuzzy import fuzz
        
        search_key = self._generate_search_key(search_name)
        matches = []
        
        for user_id, user in self.users.items():
            # Calculate similarity scores
            name_score = fuzz.ratio(search_key, user.search_key)
            partial_score = fuzz.partial_ratio(search_name.lower(), user.name.lower())
            token_score = fuzz.token_sort_ratio(search_name.lower(), user.name.lower())
            
            # Use the highest score
            best_score = max(name_score, partial_score, token_score)
            
            if best_score > 60:  # Threshold for matching
                matches.append({
                    "user_id": user_id,
                    "name": user.name,
                    "birth_date": user.birth_date,
                    "last_seen": user.last_seen,
                    "calculation_count": user.calculation_count,
                    "score": best_score
                })
        
        # Sort by score (descending) and limit results
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:limit]
    
    def get_user(self, user_id: str) -> Optional[UserRecord]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_recent_users(self, limit: int = 10) -> List[Dict]:
        """
        Get recently seen users
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List of recent user records
        """
        # Sort users by last_seen (most recent first)
        sorted_users = sorted(
            self.users.items(),
            key=lambda x: x[1].last_seen,
            reverse=True
        )
        
        result = []
        for user_id, user in sorted_users[:limit]:
            result.append({
                "user_id": user_id,
                "name": user.name,
                "birth_date": user.birth_date,
                "last_seen": user.last_seen,
                "calculation_count": user.calculation_count
            })
        
        return result
    
    def get_user_stats(self) -> Dict:
        """Get statistics about users"""
        if not self.users:
            return {
                "total_users": 0,
                "total_calculations": 0,
                "most_active_user": None,
                "recent_users_count": 0
            }
        
        total_calculations = sum(user.calculation_count for user in self.users.values())
        
        # Find most active user
        most_active = max(self.users.values(), key=lambda x: x.calculation_count)
        
        # Count recent users (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        recent_count = sum(1 for user in self.users.values() if user.last_seen > thirty_days_ago)
        
        return {
            "total_users": len(self.users),
            "total_calculations": total_calculations,
            "most_active_user": {
                "name": most_active.name,
                "calculation_count": most_active.calculation_count
            },
            "recent_users_count": recent_count
        }
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user record"""
        if user_id in self.users:
            del self.users[user_id]
            self.save_users()
            return True
        return False
    
    def export_users(self, filepath: str = None) -> str:
        """Export users to JSON file"""
        if filepath is None:
            filepath = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            data = {user_id: asdict(user) for user_id, user in self.users.items()}
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return filepath
        except Exception as e:
            raise Exception(f"Export failed: {e}")


# Test function
def test_session_manager():
    """Test the session manager"""
    # Use a test file
    session_mgr = SessionManager("test_sessions.json")
    
    print("Testing Session Manager:")
    print("=" * 50)
    
    # Add some test users
    test_users = [
        ("John Smith", "1990-03-15"),
        ("Michael Jordan", "1963-02-17"),
        ("Elizabeth Brown", "1985-03-05"),
        ("William Shakespeare", "1564-04-23"),
        ("Catherine Martinez", "1992-08-12"),
    ]
    
    user_ids = []
    for name, birth_date in test_users:
        user_id = session_mgr.add_or_update_user(name, birth_date)
        user_ids.append(user_id)
        print(f"Added user: {name} -> {user_id}")
    
    print("\nRecent users:")
    recent = session_mgr.get_recent_users(3)
    for user in recent:
        print(f"  {user['name']} ({user['birth_date']}) - {user['calculation_count']} calculations")
    
    print("\nSearching for 'john':")
    matches = session_mgr.find_user_by_name("john")
    for match in matches:
        print(f"  {match['name']} (score: {match['score']})")
    
    print("\nUser stats:")
    stats = session_mgr.get_user_stats()
    print(f"  Total users: {stats['total_users']}")
    print(f"  Total calculations: {stats['total_calculations']}")
    print(f"  Most active: {stats['most_active_user']['name']} ({stats['most_active_user']['calculation_count']} calculations)")
    
    # Clean up test file
    try:
        os.remove("test_sessions.json")
    except:
        pass


if __name__ == "__main__":
    test_session_manager()
