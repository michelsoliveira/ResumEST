import os
from dotenv import load_dotenv
from pymongo import MongoClient
from falcon import App
from interfaces.api.resources.resume_resource import ResumeResource
from interfaces.api.resources.contact_resource import ContactResource
from interfaces.api.resources.education_resource import EducationResource
from interfaces.api.resources.experience_resource import ExperienceResource
from interfaces.api.resources.skill_resource import SkillResource
from interfaces.api.resources.auth_resource import AuthResource
from interfaces.api.middleware.auth_middleware import AuthMiddleware
from infrastructure.repositories.mongodb_resume_repository import MongoDBResumeRepository
from infrastructure.repositories.mongodb_user_repository import MongoDBUserRepository
from application.services.resume_service import ResumeService
from application.services.auth_service import AuthService

# Load environment variables
load_dotenv()

def create_app():
    # Initialize MongoDB connection
    mongo_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
    database_name = os.getenv('MONGODB_DATABASE', 'resume_api')
    secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Initialize repositories
    resume_repository = MongoDBResumeRepository(mongo_client, database_name)
    user_repository = MongoDBUserRepository(mongo_client, database_name)
    
    # Initialize services
    resume_service = ResumeService(resume_repository)
    auth_service = AuthService(user_repository, secret_key)
    
    # Create Falcon app with middleware
    app = App(middleware=[AuthMiddleware(secret_key)])
    
    # Add routes
    app.add_route('/auth', AuthResource(auth_service))
    
    app.add_route('/resumes', ResumeResource(resume_service))
    app.add_route('/resumes/{resume_id}', ResumeResource(resume_service))
    
    # Contact routes
    app.add_route('/resumes/{resume_id}/contact', ContactResource(resume_service))
    
    # Education routes
    app.add_route('/resumes/{resume_id}/education', EducationResource(resume_service))
    app.add_route('/resumes/{resume_id}/education/{education_id}', EducationResource(resume_service))
    
    # Experience routes
    app.add_route('/resumes/{resume_id}/experience', ExperienceResource(resume_service))
    app.add_route('/resumes/{resume_id}/experience/{experience_id}', ExperienceResource(resume_service))
    
    # Skills routes
    app.add_route('/resumes/{resume_id}/skills', SkillResource(resume_service))
    app.add_route('/resumes/{resume_id}/skills/{skill_id}', SkillResource(resume_service))
    
    return app

app = create_app() 