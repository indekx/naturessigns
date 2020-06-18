from django.db import models

# Create your models here.
QUESTION_SET = (
    ('Account Login', 'why can\'t I login to my account?'),
)
class FAQ(models.Model):
    topic = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    question = models.CharField(choices=QUESTION_SET, max_length=255)

    def __str__(self):
        return self.topic


class Answer(models.Model):
    answer = models.ForeignKey(FAQ, on_delete=models.CASCADE, null=True)