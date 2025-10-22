from django.contrib import admin
from .models import (
    About, Education, Experience, Skill, 
    Project, Testimonial, ContactMessage, BlogPost
)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'profession', 'location', 'email']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'alias', 'profession', 'location', 'tagline')
        }),
        ('About', {
            'fields': ('bio', 'profile_image', 'cv_file')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'email', 'whatsapp')
        }),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'institution']
    search_fields = ['institution', 'degree', 'field_of_study']
    date_hierarchy = 'start_date'


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'location', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'company']
    search_fields = ['position', 'company', 'description']
    date_hierarchy = 'start_date'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['order', 'proficiency']
    ordering = ['order', '-proficiency']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'date_added', 'order']
    list_filter = ['is_featured', 'date_added']
    search_fields = ['title', 'description', 'tech_stack']
    list_editable = ['is_featured', 'order']
    date_hierarchy = 'date_added'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'detailed_description', 'image')
        }),
        ('Technical Details', {
            'fields': ('tech_stack', 'github_link', 'demo_link')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'company', 'relation', 'is_active', 'order']
    list_filter = ['is_active', 'relation']
    search_fields = ['name', 'quote', 'company']
    list_editable = ['is_active', 'order']
    ordering = ['order', '-created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'published_date', 'views', 'created_at']
    list_filter = ['is_published', 'published_date']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_date')
        }),
        ('Metadata', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )