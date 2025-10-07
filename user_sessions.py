#!/usr/bin/env python3
"""
User Session Management and Logging System

This module handles:
1. User session storage and retrieval
2. Quick lookup of previous calculations
3. User history and preferences
4. Session-based caching
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

class UserSessionManager:
    """
    Manages user sessions and calculation history for quick reference
    """
    
    def __init__(self, session_file: str = "user_sessions.json"):
        """
        Initialize the session manager.
        
        Args:
            session_file: Path to the JSON file storing user sessions
        """
        self.session_file = Path(session_file)
        self.sessions = {}
        self.current_session = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load existing sessions
        self._load_sessions()
    
    def _load_sessions(self):
        """Load sessions from file if it exists."""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sessions = data.get('sessions', {})
                    self.logger.info(f"Loaded {len(self.sessions)} user sessions")
            else:
                self.sessions = {}
                self.logger.info("No existing sessions file found, starting fresh")
        except Exception as e:
            self.logger.error(f"Error loading sessions: {e}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Save sessions to file."""
        try:
            data = {
                'sessions': self.sessions,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.debug("Sessions saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving sessions: {e}")
    
    def _generate_user_id(self, name: str, birth_date: datetime) -> str:
        """
        Generate a unique user ID based on name and birth date.
        
        Args:
            name: User's name
            birth_date: User's birth date
            
        Returns:
            Unique user ID hash
        """
        # Create a consistent identifier
        identifier = f"{name.lower().strip()}_{birth_date.strftime('%Y-%m-%d')}"
        return hashlib.md5(identifier.encode()).hexdigest()[:12]
    
    def create_or_get_user_session(self, name: str, birth_date: datetime) -> Dict[str, Any]:
        """
        Create a new user session or retrieve existing one.
        
        Args:
            name: User's name
            birth_date: User's birth date
            
        Returns:
            User session data
        """
        user_id = self._generate_user_id(name, birth_date)
        
        # Check if user exists
        if user_id in self.sessions:
            session = self.sessions[user_id]
            session['last_access'] = datetime.now().isoformat()
            session['access_count'] = session.get('access_count', 0) + 1
            self.logger.info(f"Retrieved existing session for {name} (ID: {user_id})")
        else:
            # Create new session
            session = {
                'user_id': user_id,
                'name': name,
                'birth_date': birth_date.isoformat(),
                'created_at': datetime.now().isoformat(),
                'last_access': datetime.now().isoformat(),
                'access_count': 1,
                'calculations': [],
                'preferences': {},
                'notes': ""
            }
            self.sessions[user_id] = session
            self.logger.info(f"Created new session for {name} (ID: {user_id})")
        
        self.current_session = session
        self._save_sessions()
        return session
    
    def add_calculation(self, calculation_data: Dict[str, Any]):
        """
        Add a numerology calculation to the current user's session.
        
        Args:
            calculation_data: Dictionary containing calculation results
        """
        if not self.current_session:
            self.logger.warning("No current session to add calculation to")
            return
        
        calculation_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': calculation_data.get('type', 'numerology_report'),
            'data': calculation_data
        }
        
        # Add to calculations list
        self.current_session['calculations'].append(calculation_entry)
        
        # Keep only last 10 calculations to avoid bloat
        if len(self.current_session['calculations']) > 10:
            self.current_session['calculations'] = self.current_session['calculations'][-10:]
        
        self._save_sessions()
        self.logger.debug(f"Added calculation to session {self.current_session['user_id']}")
    
    def get_recent_calculations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent calculations for the current user.
        
        Args:
            limit: Maximum number of calculations to return
            
        Returns:
            List of recent calculations
        """
        if not self.current_session:
            return []
        
        calculations = self.current_session.get('calculations', [])
        return calculations[-limit:] if calculations else []
    
    def find_user_by_name(self, name: str, fuzzy: bool = True) -> List[Dict[str, Any]]:
        """
        Find users by name for quick lookup.
        
        Args:
            name: Name to search for
            fuzzy: Whether to use fuzzy matching
            
        Returns:
            List of matching user sessions
        """
        matches = []
        search_name = name.lower().strip()
        
        for session in self.sessions.values():
            session_name = session['name'].lower().strip()
            
            if fuzzy:
                # Simple fuzzy matching - contains or similar
                if (search_name in session_name or 
                    session_name in search_name or
                    any(word in session_name for word in search_name.split())):
                    matches.append(session)
            else:
                # Exact match
                if session_name == search_name:
                    matches.append(session)
        
        # Sort by last access (most recent first)
        matches.sort(key=lambda x: x['last_access'], reverse=True)
        return matches
    
    def get_user_summary(self, user_id: str = None) -> Dict[str, Any]:
        """
        Get a summary of user's numerology profile.
        
        Args:
            user_id: User ID (uses current session if None)
            
        Returns:
            User summary with key numerology numbers
        """
        if user_id:
            session = self.sessions.get(user_id)
        else:
            session = self.current_session
        
        if not session:
            return {}
        
        summary = {
            'name': session['name'],
            'birth_date': session['birth_date'],
            'access_count': session.get('access_count', 0),
            'last_access': session['last_access'],
            'total_calculations': len(session.get('calculations', [])),
            'quick_numbers': {}
        }
        
        # Extract key numbers from most recent calculation
        calculations = session.get('calculations', [])
        if calculations:
            latest = calculations[-1]['data']
            if 'name_number' in latest:
                summary['quick_numbers']['name'] = latest['name_number']['reduced']
            if 'birth_number' in latest:
                summary['quick_numbers']['birth'] = latest['birth_number']
            if 'destiny_number' in latest:
                summary['quick_numbers']['destiny'] = latest['destiny_number']['reduced']
        
        return summary
    
    def cleanup_old_sessions(self, days: int = 90):
        """
        Remove sessions older than specified days with no recent access.
        
        Args:
            days: Number of days threshold
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        old_sessions = []
        
        for user_id, session in self.sessions.items():
            last_access = datetime.fromisoformat(session['last_access'])
            if last_access < cutoff_date:
                old_sessions.append(user_id)
        
        for user_id in old_sessions:
            del self.sessions[user_id]
        
        if old_sessions:
            self._save_sessions()
            self.logger.info(f"Cleaned up {len(old_sessions)} old sessions")
    
    def get_all_users_summary(self) -> List[Dict[str, Any]]:
        """
        Get a summary of all users for admin/debug purposes.
        
        Returns:
            List of user summaries
        """
        summaries = []
        for user_id in self.sessions.keys():
            summary = self.get_user_summary(user_id)
            if summary:
                summary['user_id'] = user_id
                summaries.append(summary)
        
        # Sort by last access
        summaries.sort(key=lambda x: x['last_access'], reverse=True)
        return summaries
    
    def export_user_data(self, user_id: str = None) -> Dict[str, Any]:
        """
        Export user data for backup or transfer.
        
        Args:
            user_id: User ID (uses current session if None)
            
        Returns:
            Complete user data
        """
        if user_id:
            session = self.sessions.get(user_id)
        else:
            session = self.current_session
        
        if not session:
            return {}
        
        return dict(session)  # Return a copy

def test_user_sessions():
    """Test the user session manager."""
    manager = UserSessionManager("test_sessions.json")
    
    print("🧪 Testing User Session Manager")
    print("=" * 50)
    
    # Test creating sessions
    session1 = manager.create_or_get_user_session("John Doe", datetime(1990, 1, 15))
    print(f"Created session for John Doe: {session1['user_id']}")
    
    # Add a calculation
    calc_data = {
        'type': 'numerology_report',
        'name_number': {'compound': 18, 'reduced': 9},
        'birth_number': 6,
        'destiny_number': {'compound': 24, 'reduced': 6}
    }
    manager.add_calculation(calc_data)
    
    # Test finding users
    matches = manager.find_user_by_name("john")
    print(f"Found {len(matches)} matches for 'john'")
    
    # Test getting summary
    summary = manager.get_user_summary()
    print(f"User summary: {summary}")
    
    # Test second user
    session2 = manager.create_or_get_user_session("Jane Smith", datetime(1985, 3, 20))
    print(f"Created session for Jane Smith: {session2['user_id']}")
    
    # Test getting all users
    all_users = manager.get_all_users_summary()
    print(f"Total users: {len(all_users)}")
    
    print("\\n✅ User session tests completed!")

if __name__ == "__main__":
    test_user_sessions()
