from django.db import models

# Create your models here.

class Tag(models.Model):
  caption = models.CharField(max_length=20)

  def __str__(self):
    return f'{self.caption}'


class Author(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=254)

  def full_name(self):
    return f'{self.first_name} {self.last_name}'
  
  def __str__(self):
    return self.full_name()



class Post(models.Model):
  title = models.CharField(max_length=100)
  excerpt = models.CharField(max_length=150)
  image = models.ImageField(upload_to='post')
  date = models.DateField(auto_now=True, null=True)
  slug = models.SlugField(unique=True, db_index=True)
  content = models.TextField()
  author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name="posts", null=True)
  tags = models.ManyToManyField(Tag)



class Comment(models.Model):
  user_name = models.CharField(max_length=150)
  user_email = models.EmailField()
  text = models.TextField(max_length=400)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')