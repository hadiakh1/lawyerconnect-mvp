import secrets

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from flask_login import login_user, logout_user, login_required, current_user

from .extensions import db
from .models import User, LawyerProfile, Issue, Chat, Message, ISSUE_CATEGORIES

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_lawyer:
            return redirect(url_for("main.lawyer_dashboard"))
        return redirect(url_for("main.user_dashboard"))
    return render_template("landing.html")


@main_bp.route("/signup/user", methods=["GET", "POST"])
def signup_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("main.signup_user"))

        user = User(name=name, email=email, is_lawyer=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("signup_user.html")


@main_bp.route("/signup/lawyer", methods=["GET", "POST"])
def signup_lawyer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        expertise = request.form.getlist("expertise")
        experience_description = request.form.get("experience_description")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("main.signup_lawyer"))

        user = User(name=name, email=email, is_lawyer=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = LawyerProfile(
            user_id=user.id,
            expertise_categories=",".join(expertise),
            experience_description=experience_description,
        )
        db.session.add(profile)
        db.session.commit()

        flash("Lawyer account created. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("signup_lawyer.html", categories=ISSUE_CATEGORIES)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)  # Remember user across browser sessions
            from flask import session
            session.permanent = True  # Make session permanent
            flash("Logged in successfully.", "success")
            if user.is_lawyer:
                return redirect(url_for("main.lawyer_dashboard"))
            return redirect(url_for("main.user_dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))


@main_bp.route("/dashboard/user")
@login_required
def user_dashboard():
    if current_user.is_lawyer:
        return redirect(url_for("main.lawyer_dashboard"))

    issues = Issue.query.filter_by(user_id=current_user.id).order_by(
        Issue.created_at.desc()
    )
    chats = Chat.query.filter_by(user_id=current_user.id).order_by(
        Chat.created_at.desc()
    )
    return render_template("user_dashboard.html", issues=issues, chats=chats)


@main_bp.route("/dashboard/lawyer")
@login_required
def lawyer_dashboard():
    if not current_user.is_lawyer:
        return redirect(url_for("main.user_dashboard"))

    profile = current_user.lawyer_profile
    chats = Chat.query.filter_by(lawyer_id=current_user.id).order_by(
        Chat.created_at.desc()
    )
    return render_template("lawyer_dashboard.html", profile=profile, chats=chats)


@main_bp.route("/issue/new", methods=["GET", "POST"])
@login_required
def submit_issue():
    if current_user.is_lawyer:
        flash("Only regular users can submit issues.", "error")
        return redirect(url_for("main.lawyer_dashboard"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        
        # Client profile fields for matching (with defaults for backward compatibility)
        try:
            budget_min = float(request.form.get("budget_min", 0) or 0)
            budget_max = float(request.form.get("budget_max", 10000) or 10000)
        except (ValueError, TypeError):
            budget_min = 0.0
            budget_max = 10000.0
        
        urgency = request.form.get("urgency", "normal")
        preferred_pricing = request.form.get("preferred_pricing", "hourly")

        if category not in ISSUE_CATEGORIES:
            flash("Invalid category.", "error")
            return redirect(url_for("main.submit_issue"))
        
        if budget_min > budget_max:
            flash("Minimum budget cannot be greater than maximum budget.", "error")
            return redirect(url_for("main.submit_issue"))

        # Create issue with new fields (will use defaults if columns don't exist yet)
        try:
            issue = Issue(
                user_id=current_user.id,
                title=title,
                description=description,
                category=category,
                budget_min=budget_min,
                budget_max=budget_max,
                urgency=urgency,
                preferred_pricing=preferred_pricing,
            )
        except Exception as e:
            # Fallback for databases without new columns
            print(f"Warning: Could not create issue with new fields: {e}")
            issue = Issue(
                user_id=current_user.id,
                title=title,
                description=description,
                category=category,
            )
        db.session.add(issue)
        db.session.commit()

        flash("Issue submitted.", "success")
        return redirect(url_for("main.lawyer_matches", issue_id=issue.id))

    return render_template("submit_issue.html", categories=ISSUE_CATEGORIES)


@main_bp.route("/issue/<int:issue_id>/lawyers")
@login_required
def lawyer_matches(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.user_id != current_user.id:
        flash("You do not have access to this issue.", "error")
        return redirect(url_for("main.user_dashboard"))

    # Use advanced matching algorithm with Priority Queue and Trie (with fallback for old database schema)
    try:
        from .advanced_matching import advanced_matcher
        
        # Check if issue has new fields (for backward compatibility)
        has_new_fields = hasattr(issue, 'budget_min') and hasattr(issue, 'urgency')
        
        if has_new_fields:
            # Get all available lawyers
            all_lawyers = (
                LawyerProfile.query.join(User, LawyerProfile.user_id == User.id)
                .filter(User.is_lawyer == True)
                .all()
            )
            
            # Fallback if join fails
            if not all_lawyers:
                all_lawyers = [
                    lp for lp in LawyerProfile.query.all()
                    if lp.user and lp.user.is_lawyer
                ]
            
            # Get matched lawyers using advanced Priority Queue algorithm
            matched_results = advanced_matcher.match_lawyers(issue, all_lawyers, top_k=20)
            
            # Format: (lawyer, score, breakdown, reasons) -> (lawyer, score, breakdown)
            matched_lawyers = [(lawyer, score, breakdown) for lawyer, score, breakdown, _ in matched_results]
            
            print(f"Found {len(matched_lawyers)} matched lawyers for issue: {issue.title}")
        else:
            # Fallback to simple matching for old database schema
            print("Using simple matching (database not migrated yet)")
            matching_lawyers = (
                LawyerProfile.query.join(User, LawyerProfile.user_id == User.id)
                .filter(
                    User.is_lawyer == True,
                    LawyerProfile.expertise_categories.like(f"%{issue.category}%")
                )
                .all()
            )
            # Convert to new format with dummy scores
            matched_lawyers = [(lp, 75.0, {'case_type': 100, 'specialization': 75, 'success_rate': lp.case_success_rate * 100, 'availability': 100, 'pricing': 50, 'client_profile': 50}) for lp in matching_lawyers]
        
    except Exception as e:
        print(f"Error in lawyer_matches: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to simple query
        try:
            matching_lawyers = (
                LawyerProfile.query.join(User, LawyerProfile.user_id == User.id)
                .filter(
                    User.is_lawyer == True,
                    LawyerProfile.expertise_categories.like(f"%{issue.category}%")
                )
                .all()
            )
            matched_lawyers = [(lp, 75.0, {}) for lp in matching_lawyers]
        except:
            matched_lawyers = []
    
    return render_template(
        "lawyer_matches.html", 
        issue=issue, 
        matched_lawyers=matched_lawyers  # Pass tuples of (lawyer, score, breakdown)
    )


@main_bp.route("/start_chat/<int:issue_id>/<int:lawyer_id>", methods=["POST"])
@login_required
def start_chat(issue_id, lawyer_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.user_id != current_user.id:
        flash("You do not have access to this issue.", "error")
        return redirect(url_for("main.user_dashboard"))

    lawyer = User.query.get_or_404(lawyer_id)
    if not lawyer.is_lawyer:
        flash("Selected user is not a lawyer.", "error")
        return redirect(url_for("main.lawyer_matches", issue_id=issue.id))

    chat = Chat.query.filter_by(
        user_id=current_user.id, lawyer_id=lawyer.id, issue_id=issue.id
    ).first()
    if not chat:
        chat = Chat(user_id=current_user.id, lawyer_id=lawyer.id, issue_id=issue.id)
        db.session.add(chat)
        db.session.commit()

    return redirect(url_for("main.chat_view", chat_id=chat.id))


@main_bp.route("/start_chat_and_call/<int:issue_id>/<int:lawyer_id>", methods=["POST"])
@login_required
def start_chat_and_call(issue_id, lawyer_id):
    """Start a chat and immediately generate a Jitsi link."""
    issue = Issue.query.get_or_404(issue_id)
    if issue.user_id != current_user.id:
        flash("You do not have access to this issue.", "error")
        return redirect(url_for("main.user_dashboard"))

    lawyer = User.query.get_or_404(lawyer_id)
    if not lawyer.is_lawyer:
        flash("Selected user is not a lawyer.", "error")
        return redirect(url_for("main.lawyer_matches", issue_id=issue.id))

    chat = Chat.query.filter_by(
        user_id=current_user.id, lawyer_id=lawyer.id, issue_id=issue.id
    ).first()
    if not chat:
        chat = Chat(user_id=current_user.id, lawyer_id=lawyer.id, issue_id=issue.id)
        db.session.add(chat)
        db.session.commit()

    # Generate Jitsi link if not exists
    if not chat.jitsi_link:
        random_string = secrets.token_urlsafe(10)
        chat.jitsi_link = f"https://meet.jit.si/{random_string}"
        db.session.commit()

    return redirect(url_for("main.chat_view", chat_id=chat.id))


def _user_can_access_chat(chat: Chat, user: User) -> bool:
    return user.id in {chat.user_id, chat.lawyer_id}


@main_bp.route("/chat/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_view(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if not _user_can_access_chat(chat, current_user):
        flash("You do not have access to this chat.", "error")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            role = "lawyer" if current_user.is_lawyer else "user"
            msg = Message(
                chat_id=chat.id,
                sender_id=current_user.id,
                sender_role=role,
                content=content,
            )
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for("main.chat_view", chat_id=chat.id))

    messages = chat.messages.all()
    return render_template(
        "chat.html",
        chat=chat,
        messages=messages,
    )


@main_bp.route("/chat/<int:chat_id>/generate_link", methods=["POST"])
@login_required
def generate_jitsi_link(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if not _user_can_access_chat(chat, current_user):
        flash("You do not have access to this chat.", "error")
        return redirect(url_for("main.index"))

    if not chat.jitsi_link:
        random_string = secrets.token_urlsafe(10)
        chat.jitsi_link = f"https://meet.jit.si/{random_string}"
        db.session.commit()

    flash("Video call link generated.", "success")
    return redirect(url_for("main.chat_view", chat_id=chat.id))


# ============================================================================
# TEMPORARY MIGRATION ENDPOINTS - Remove after Render setup
# ============================================================================

@main_bp.route("/admin/migrate", methods=["GET", "POST"])
def run_migrations():
    """One-time migration endpoint for Render deployment.
    Visit: https://your-app.onrender.com/admin/migrate
    """
    try:
        from app.extensions import db
        from app.models import User, LawyerProfile, Issue, Chat, Message
        import sys
        import os
        
        # Create all tables
        db.create_all()
        
        # Run migrations
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        
        try:
            from migrate_db_simple import migrate_database
            migrate_database()
            migration1 = "✅ Simple migration completed"
        except Exception as e:
            migration1 = f"⚠️ Simple migration: {str(e)}"
        
        try:
            from migrate_db_advanced import migrate_database
            migrate_database()
            migration2 = "✅ Advanced migration completed"
        except Exception as e:
            migration2 = f"⚠️ Advanced migration: {str(e)}"
        
        return f"""
        <html>
        <head><title>Migrations Complete</title>
        <style>
            body {{ font-family: Arial; padding: 40px; max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #800020; }}
            a {{ color: #800020; text-decoration: underline; }}
            .success {{ color: green; }}
            .warning {{ color: orange; }}
            hr {{ margin: 30px 0; }}
        </style>
        </head>
        <body>
            <h1>✅ Migrations Complete!</h1>
            <p><strong>Results:</strong></p>
            <p class="success">{migration1}</p>
            <p class="success">{migration2}</p>
            <hr>
            <p><a href="/admin/seed">Next: Seed Database →</a></p>
            <p><a href="/">Go to Home</a></p>
            <hr>
            <p style="color: red; font-size: 12px;">
                ⚠️ IMPORTANT: Remove /admin/migrate and /admin/seed endpoints after setup!
            </p>
        </body>
        </html>
        """
    except Exception as e:
        import traceback
        return f"""
        <html>
        <head><title>Migration Error</title></head>
        <body style="font-family: Arial; padding: 40px;">
            <h1 style="color: red;">❌ Migration Error</h1>
            <pre style="background: #f5f5f5; padding: 15px; overflow-x: auto;">{traceback.format_exc()}</pre>
        </body>
        </html>
        """, 500


@main_bp.route("/admin/seed", methods=["GET", "POST"])
def seed_database():
    """One-time database seeding endpoint for Render deployment.
    Visit: https://your-app.onrender.com/admin/seed
    """
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from seed_db import seed_database
        
        seed_database()
        
        return """
        <html>
        <head><title>Database Seeded</title>
        <style>
            body { font-family: Arial; padding: 40px; max-width: 600px; margin: 0 auto; }
            h1 { color: #800020; }
            a { color: #800020; text-decoration: underline; }
            hr { margin: 30px 0; }
        </style>
        </head>
        <body>
            <h1>✅ Database Seeded!</h1>
            <p>Sample lawyers have been added successfully.</p>
            <hr>
            <p><a href="/">Go to Home</a></p>
            <hr>
            <p style="color: red; font-size: 12px;">
                ⚠️ IMPORTANT: Remove /admin/migrate and /admin/seed endpoints after setup!
            </p>
        </body>
        </html>
        """
    except Exception as e:
        import traceback
        return f"""
        <html>
        <head><title>Seeding Error</title></head>
        <body style="font-family: Arial; padding: 40px;">
            <h1 style="color: red;">❌ Seeding Error</h1>
            <p>Make sure migrations ran first: <a href="/admin/migrate">Run Migrations</a></p>
            <pre style="background: #f5f5f5; padding: 15px; overflow-x: auto;">{traceback.format_exc()}</pre>
        </body>
        </html>
        """, 500
