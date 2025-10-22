from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from .models import (
    About, Education, Experience, Skill, 
    Project, Testimonial, BlogPost
)
from .forms import ContactForm


def home(request):
    """Main portfolio page with all sections"""
    try:
        about = About.objects.first()
    except About.DoesNotExist:
        about = None
    
    education = Education.objects.all()[:3]
    experience = Experience.objects.all()[:3]
    skills = Skill.objects.all()
    projects = Project.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    context = {
        'about': about,
        'education': education,
        'experience': experience,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'testimonials': testimonials,
        'recent_posts': recent_posts,
        'contact_form': ContactForm(),
    }
    
    return render(request, 'index.html', context)


def contact_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification
            try:
                subject = f"Portfolio Contact: {contact_message.subject or 'New Message'}"
                message_body = f"""
                New contact form submission:
                
                Name: {contact_message.name}
                Email: {contact_message.email}
                Subject: {contact_message.subject}
                
                Message:
                {contact_message.message}
                
                ---
                Sent from Portfolio Website
                """
                
                email = EmailMessage(
                    subject=subject,
                    body=message_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.EMAIL_HOST_USER],
                    reply_to=[contact_message.email]
                )
                email.send(fail_silently=False)
                
                messages.success(request, 'Thank you for your message! I will get back to you soon.')
            except Exception as e:
                messages.warning(request, 'Your message was saved, but email notification failed. I will still review it.')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
            
            return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            
            messages.error(request, 'Please correct the errors in the form.')
    
    return redirect('home')


def project_detail(request, pk):
    """Get project details for modal"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'title': project.title,
            'description': project.description,
            'detailed_description': project.detailed_description or project.description,
            'image': project.image.url if project.image else '',
            'tech_stack': project.get_tech_list(),
            'github_link': project.github_link,
            'demo_link': project.demo_link,
        }
        return JsonResponse(data)
    
    return render(request, 'project_detail.html', {'project': project})


def blog_list(request):
    """List all published blog posts"""
    posts = BlogPost.objects.filter(is_published=True)
    context = {
        'posts': posts,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    """Individual blog post"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views += 1
    post.save(update_fields=['views'])
    
    context = {
        'post': post,
    }
    return render(request, 'blog_detail.html', context)