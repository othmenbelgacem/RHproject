from django.db import models

# Create your models here.
class Candidate(models.Model):
    Candidate_number = models.PositiveIntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    Candidate_job_category = models.CharField(max_length=50)
    gpa =models.FloatField()
    Years_of_Experience =models.IntegerField()
    salary = models.IntegerField()
    skills = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.Candidate_number:
            # Generate Candidate_number only if it's not provided
            last_candidate = Candidate.objects.order_by('-Candidate_number').first()
            if last_candidate:
                self.Candidate_number = last_candidate.Candidate_number + 1
            else:
                # If there are no existing candidates, start with 1
                self.Candidate_number = 1

        super().save(*args, **kwargs)
    def __str__(self):
        return f'Candisdate: {self.first_name}{self.last_name}'

