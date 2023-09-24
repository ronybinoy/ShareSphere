from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username=models.CharField(max_length=32, blank=True, null=True)
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    img=models.ImageField(upload_to='pics',default='https://img.freepik.com/free-icon/man_318-677829.jpg',null=True)
    is_migrant=models.BooleanField('is_migrant',default=False,null=True)
    is_institute=models.BooleanField('is_institute',default=False,null=True)
    is_landlord=models.BooleanField('is_landlord',default=False,null=True)
    migrant_uid = models.CharField(("migrant_uid"),default='',max_length=20,null=True)
    institute_lis_no = models.CharField(("institute_lis_no"),default='',max_length=30,null=True)
    landlord_uid = models.CharField(("landlord_uid"),default='',max_length=20,null=True)
    nationality = models.CharField(("nationality"),default='',max_length=30,null=True)
    region = models.CharField(("region"),default='',max_length=30,null=True)
    institute_type = models.CharField(("institute_type"),default='',max_length=20,null=True)
    REQUIRED_FIELDS = []



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


    

    def __str__(self):
        return f"{self.user.first_name}'s Application for {self.course.course_name}"


        