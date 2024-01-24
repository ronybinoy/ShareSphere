from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    username=models.CharField(max_length=32, blank=True, null=True)
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    is_migrant = models.BooleanField('is_migrant', default=False, null=True)
    is_institute = models.BooleanField('is_institute', default=False, null=True)
    is_landlord = models.BooleanField('is_landlord', default=False, null=True)
    migrant_uid = models.CharField(("migrant_uid"), default='', max_length=20, null=True)
    institute_lis_no = models.CharField(("institute_lis_no"), default='', max_length=30, null=True)
    nationality = models.CharField(("nationality"), default='', max_length=30, null=True)
    region = models.CharField(("region"), default='', max_length=30, null=True)
    phone = models.CharField(("phone"), default='', max_length=15, null=True)
    country_code = models.CharField(("country_code"), default='', max_length=5, null=True)
    REQUIRED_FIELDS = []

class Migrant(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Use the custom user model as the target
        on_delete=models.CASCADE,
    )
    dob = models.DateField(("Date of Birth"), null=True, blank=True)
    contact_no = models.CharField(("Contact Number"), max_length=15, null=True, blank=True)
    profile_photo = models.ImageField(
        ("Profile Photo"),
        upload_to='profile_photos/',
        default='default_profile.png',  # Use the filename of your default profile photo
        null=True,
        blank=True
    )


class Course(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        default=None  # Use None as the default value
    )  
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    course_name = models.CharField(max_length=255)
    course_mode = models.CharField(max_length=255, default='Online')
    course_type = models.CharField(max_length=255, default='Bachelor Degree')
    academic_disciplines = models.CharField(max_length=255, default='Business and Information Technology')
    course_desc = models.TextField(null=True)
    eligibility = models.TextField()
    duration = models.CharField(max_length=255)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    opendate = models.DateField()
    appdeadline = models.DateField()
    is_active = models.BooleanField(default=True) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail_image = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    seat_available = models.IntegerField(null=True, blank=True)
    rejection_remark = models.TextField(blank=True, null=True)
    course_code = models.CharField(max_length=20, default='ABC1234')  # You can adjust max_length as needed
    


    def approve(self):
        self.status = 'approved'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()
    
    def save(self, *args, **kwargs):
        # Set the default application deadline as the same date as opendate
        if not self.appdeadline:
            self.appdeadline = self.opendate
        
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name



class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True) 


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
        
class Inst_info(models.Model):
    license_number = models.CharField(max_length=12, unique=True)
    inst_name = models.CharField(max_length=255)
    inst_email = models.EmailField()

    def __str__(self):
        return self.inst_name



class Course_Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Reference CustomUser model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    application_id = models.CharField(primary_key=True,max_length=7, default='0000000')    
    full_name = models.CharField(default='',max_length=255)  # Official Full Name
    email = models.EmailField(default='')  # Email (Taken from CustomUser)
    gender = models.CharField(default='', max_length=10)  # Gender
    date_of_birth = models.DateField(default='')  # Date of Birth
    citizenship = models.CharField(default='', max_length=255)  # Citizenship (Taken from CustomUser)
    country = models.CharField(default='', max_length=100)  # Country
    province = models.CharField(default='',max_length=100)  # Province/State/Territory
    street_address1 = models.CharField( default='', max_length=255)  # Street Address 1
    street_address2 = models.CharField(default='', max_length=255, blank=True)  # Street Address 2
    postal_code = models.CharField(default='', max_length=20)  # Postal/Zip Code
    contact_number = models.CharField(default='', max_length=20)  # Contact Number with Country Code
    qualification1 = models.CharField(default='', max_length=255)  # Qualification Name
    institute1 = models.CharField(default='', max_length=255)  # Institute Name
    percentage1 = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)  # Overall Percentage of the Course
    passing_year1 = models.IntegerField(default=0)  # Year of Passout
    english_proficiency_test = models.CharField(default='', max_length=10)  # English Proficiency Test
    english_score = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)  # Test Score
    english_validity = models.IntegerField(default=0)  # Validity (Year)
    proficiency_result = models.FileField(null=True, upload_to='proficiency_results/')  # Proficiency Result (PDF)
    policy_declaration = models.BooleanField(default=True)  # Policy Declaration Agreement
    average_percentage = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)  # Average Percentage
    application_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    APPLICATION_STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    )
    application_status = models.CharField(
        max_length=10,
        choices=APPLICATION_STATUS_CHOICES,
        default='applied',  # Set the default status to 'pending'
    )

    

    def __str__(self):
        return f"{self.user.first_name}'s Application for {self.course.course_name}"


class Payment(models.Model):
    application = models.ForeignKey(Course_Application, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_datetime = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
    ))

    def __str__(self):
        return f"Payment for Application {self.application_id}"
    
class Property(models.Model):

    landlord = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    address = models.TextField()
    property_location_link = models.URLField()
    country = models.CharField(max_length=255)
    state_province = models.CharField(max_length=255)
    
    frontview_image = models.ImageField(upload_to='property_images/')
    living_room_image = models.ImageField(upload_to='property_images/')
    bedroom_image = models.ImageField(upload_to='property_images/')
    bathroom_image = models.ImageField(upload_to='property_images/')
    kitchen_image = models.ImageField(upload_to='property_images/')
    dining_room_image = models.ImageField(upload_to='property_images/')
    other1_image = models.ImageField(upload_to='property_images/')
    other2_image = models.ImageField(upload_to='property_images/')
    
    contact_number = models.CharField(max_length=15)  # Assuming the maximum length for a phone number
    
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_duration_of_rent = models.IntegerField(choices=[(1, '1 month'), (2, '2 months'), (3, '3 months'), (4, '4 months'), (5, '5 months'), (6, '6 months')])
    number_of_bedrooms = models.IntegerField(choices=[(1, '1 BHK'), (2, '2 BHK'), (3, '3 BHK'), (4, '4 BHK')])
    
    parking_area = models.BooleanField(default=False)
    cctv = models.BooleanField(default=False)
    heater = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    power_backup = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.property_name
