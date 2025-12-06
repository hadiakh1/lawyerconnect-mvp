"""
Command-line database viewer.
Run: python view_db.py
"""
from app import create_app
from app.models import User, LawyerProfile, Issue, Chat, Message
from app.extensions import db

app = create_app()

with app.app_context():
    print("=" * 80)
    print("LAWYERCONNECT MVP - DATABASE VIEWER")
    print("=" * 80)
    
    # Statistics
    print("\n📊 STATISTICS")
    print("-" * 80)
    print(f"Total Users: {User.query.count()}")
    print(f"  - Regular Users: {User.query.filter_by(is_lawyer=False).count()}")
    print(f"  - Lawyers: {User.query.filter_by(is_lawyer=True).count()}")
    print(f"Lawyer Profiles: {LawyerProfile.query.count()}")
    print(f"Issues: {Issue.query.count()}")
    print(f"Chats: {Chat.query.count()}")
    print(f"Messages: {Message.query.count()}")
    
    # Users
    print("\n👥 USERS")
    print("-" * 80)
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id:3d} | Name: {user.name:30s} | Email: {user.email:35s} | Type: {'Lawyer' if user.is_lawyer else 'User'}")
    
    # Lawyers
    print("\n⚖️  LAWYER PROFILES")
    print("-" * 80)
    lawyers = LawyerProfile.query.all()
    for lawyer in lawyers:
        name = lawyer.user.name if lawyer.user else "N/A"
        print(f"ID: {lawyer.id:3d} | Name: {name:30s} | Rating: {lawyer.rating:.1f} | Success: {lawyer.case_success_rate*100:.1f}% | Expertise: {lawyer.expertise_categories[:40]}")
    
    # Issues
    print("\n📋 ISSUES")
    print("-" * 80)
    issues = Issue.query.order_by(Issue.created_at.desc()).all()
    for issue in issues:
        user_name = issue.user.name if issue.user else "N/A"
        print(f"ID: {issue.id:3d} | Title: {issue.title[:40]:40s} | Category: {issue.category:25s} | User: {user_name}")
    
    # Chats
    print("\n💬 CHATS")
    print("-" * 80)
    chats = Chat.query.all()
    for chat in chats:
        user_name = chat.user.name if chat.user else "N/A"
        lawyer_name = chat.lawyer.name if chat.lawyer else "N/A"
        issue_title = chat.issue.title[:30] if chat.issue else "N/A"
        print(f"ID: {chat.id:3d} | User: {user_name:20s} | Lawyer: {lawyer_name:20s} | Issue: {issue_title}")
    
    # Recent Messages
    print("\n📨 RECENT MESSAGES (Last 10)")
    print("-" * 80)
    messages = Message.query.order_by(Message.created_at.desc()).limit(10).all()
    for msg in messages:
        sender_name = msg.sender.name if msg.sender else "N/A"
        content = msg.content[:50] if len(msg.content) > 50 else msg.content
        print(f"ID: {msg.id:3d} | {msg.sender_role:8s} | {sender_name:20s} | {content}")
    
    print("\n" + "=" * 80)
    print("PRIVATE DATABASE ACCESS:")
    print("-" * 80)
    print("To view in browser (admin only):")
    print("  1. Log in with your admin email")
    print("  2. Visit: http://localhost:5000/admin/database?key=admin123")
    print("  (Change the key in app/routes.py for security)")
    print("=" * 80)

