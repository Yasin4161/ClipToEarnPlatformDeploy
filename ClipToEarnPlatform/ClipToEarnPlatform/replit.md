# ClipToEarn - Replit Development Guide

## Overview

ClipToEarn is a Flask-based web application that allows users to create short clips from streaming videos and earn money based on view counts. The platform connects streamers who want their content clipped with creators who make YouTube Shorts and TikTok videos.

**Current Status**: Ready for production deployment to klipper.com.tr - fully functional platform with KVKK/GDPR compliance and social media link submission workflow.

## User Preferences

Preferred communication style: Simple, everyday language.
UI/UX Preferences: Twitch-style purple/dark theme, mobile-first responsive design.
Deployment preference: Always-accessible deployment for continuous availability.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating
- **UI Library**: Tailwind CSS for styling and responsive design
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JS for interactive features and form validation
- **Theme**: Twitch-style purple/dark theme with mobile-first responsive design

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login for session management
- **Forms**: WTForms with Flask-WTF for form handling and validation
- **Security**: Werkzeug for password hashing and proxy handling

### Database Schema
The application uses SQLAlchemy with three main models:
- **User**: Stores user accounts with admin/clipper roles
- **StreamTask**: Represents clip creation tasks with rewards
- **Clip**: Tracks submitted clips with view counts and earnings

## Key Components

### Authentication System
- User registration and login functionality
- Role-based access control (admin vs. regular users)
- Session management with Flask-Login
- Password hashing with Werkzeug security

### Task Management
- Admins can create stream tasks with:
  - Title and description
  - Stream URL source
  - Reward per 1K views
  - Deadlines
- Tasks are displayed to clippers for selection

### Clip Submission System
- Users can submit clips for specific tasks
- Support for YouTube Shorts and TikTok platforms
- View count tracking and earnings calculation
- Status management (pending, approved, rejected)

### Admin Panel
- Dashboard with statistics and metrics
- Task creation and management
- Clip review and approval system
- User management capabilities

## Data Flow

1. **Admin creates task** → StreamTask record created
2. **Clipper selects task** → Views task details and requirements
3. **Clipper submits clip** → Clip record created with pending status
4. **Admin reviews clip** → Updates view count and status
5. **Earnings calculation** → Automatic calculation based on views and reward rate
6. **Payment tracking** → Marks clips as paid when processed

## External Dependencies

### Backend Dependencies
- Flask and Flask extensions (SQLAlchemy, Login, WTF)
- SQLAlchemy for database operations
- Werkzeug for security utilities
- WTForms for form validation

### Frontend Dependencies
- Tailwind CSS (via CDN) for styling
- Font Awesome (via CDN) for icons
- No major JavaScript frameworks (vanilla JS approach)

### Database
- Configured to use SQLite by default (`cliptolearn.db`)
- Supports PostgreSQL through `DATABASE_URL` environment variable
- Connection pooling and health checks configured

## Deployment Strategy

### Environment Configuration
- Uses environment variables for sensitive data:
  - `SESSION_SECRET`: Flask session key
  - `DATABASE_URL`: Database connection string
- Defaults provided for development environment

### Production Considerations
- Proxy fix middleware for reverse proxy deployments
- Database connection pooling configured
- Session security with environment-based secret key
- Logging configured for debugging

### File Structure
```
├── app.py              # Application factory and configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routing and view functions
├── forms.py            # WTForms form definitions
├── templates/          # Jinja2 templates
│   ├── base.html       # Base template
│   ├── auth/           # Authentication templates
│   ├── admin/          # Admin panel templates
│   └── clipper/        # User interface templates
└── static/             # Static assets (CSS, JS)
```

### Key Features
- Mobile-first responsive design optimized for all screen sizes
- Twitch-style purple/dark theme with consistent branding
- Form validation and error handling
- Real-time earnings calculation
- Multi-platform support (YouTube, TikTok)
- Deadline tracking and task management
- Statistics and analytics dashboard
- Mobile-friendly navigation with hamburger menu
- Touch-optimized buttons and interface elements

## Recent Changes (July 15, 2025)
- ✓ Updated system logic to use social media link submission workflow
- ✓ Users now submit social media post links instead of uploading files
- ✓ Admin reviews clips by clicking external links
- ✓ Fixed SelectField choices error in ClipSubmissionForm
- ✓ Updated all templates to reflect link-based submission process
- ✓ Enhanced admin panel with "Klip İncele" buttons for direct link review
- ✓ Improved mobile responsiveness across all pages
- ✓ Changed currency from USD ($) to Turkish Lira (₺) across all templates
- ✓ Updated admin email to yasinozdin0@gmail.com with new password
- ✓ Fixed admin user creation to prevent duplicate key errors
- ✓ Added IBAN and full name fields to user profiles for payment processing
- ✓ Enhanced admin submissions view to show user payment information
- ✓ Added admin contact email (yasin4161trabzon@gmail.com) to footer
- ✓ Added "Recent Tasks" section to clipper dashboard showing newest 5 tasks
- ✓ Updated user registration form to include payment information fields
- ✓ Added KVKK/GDPR compliance with privacy policy page
- ✓ Implemented consent tracking system with IP and timestamp logging
- ✓ Added IBAN encryption using AES for enhanced security
- ✓ Created admin privacy compliance dashboard
- ✓ Added required consent checkbox to registration form
- ✓ User purchased klipper.com.tr domain for production deployment
- ✓ Password reset functionality removed due to email server issues
- ✓ Added Instagram Reels as third platform option alongside YouTube Shorts and TikTok
- ✓ Integrated custom Klipper logo throughout the site (navigation, hero section, title)
- ✓ Added admin users panel to view all registered users with their details, IBAN info, and KVKK compliance status

## Deployment Ready
The application is ready for deployment with:
- PostgreSQL database configured
- All core functionality tested and working
- Social media link workflow implemented
- Admin panel fully operational
- Mobile-responsive design complete

The application is designed to be scalable and maintainable, with clear separation of concerns between models, views, and templates. The modular structure allows for easy extension and modification of features.