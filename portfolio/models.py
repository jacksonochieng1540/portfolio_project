from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class About(models.Model):
    name = models.CharField(max_length=100, default="Jackson Ochieng Odhiambo")
    alias = models.CharField(max_length=50, default="Jack Ayaga")
    profession = models.CharField(max_length=200, default="Software Engineer | Backend Developer")
    location = models.CharField(max_length=100, default="Kiambu, Kenya")
    tagline = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_file = models.FileField(upload_to='files/', blank=True, null=True)
    
    # Social Links
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"
    
    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    grade = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.TextField(blank=True, help_text="One achievement per line")
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    def get_achievements_list(self):
        return [a.strip() for a in self.achievements.split('\n') if a.strip()]


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Programming Language'),
        ('framework', 'Framework'),
        ('database', 'Database'),
        ('tool', 'Tool'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Proficiency level (1-100)"
    )
    icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Font Awesome or custom icon class"
    )
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-proficiency']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/')
    tech_stack = models.CharField(max_length=500, help_text="Comma-separated technologies")
    github_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    date_added = models.DateField(auto_now_add=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_added']
    
    def __str__(self):
        return self.title
    
    def get_tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',')]


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    relation = models.CharField(max_length=100, help_text="e.g., Colleague, Client, Manager")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.relation}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title