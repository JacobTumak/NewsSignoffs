# Getting Started with django-signoffs

Welcome to django-signoffs!
This guide will walk you through the process of setting up and using the first layer of this package.

## Prerequisites

Before you begin, ensure you have the following:

- [x] A Django project up and running (Django version X.X.X or later)
- [x] Basic knowledge of Django models, views, and templates

## Installation

To get started with django-signoffs, follow these steps:

1. Install the package using pip:

   ```bash
   pip install django-signoffs
   ```

2. Add `'signoffs'` to `INSTALLED_APPS` in your project's settings:

   ```python
   # settings.py

   INSTALLED_APPS = [
       # ...
       'signoffs',
       # ...
   ]
   ```

3. Run migrations to create the necessary database tables:

   ```bash
   python manage.py migrate
   ```

## Registering and Configuring a Simple Signoff

Now that you have django-signoffs installed and set up, let's dive into configuring a simple signoff:

1. Register a new signoff with your preffered signoff type (Simple, Revokable or Irrevokable):
    *Note that the Revokable and Irrevokable signoff classes are pre-configured subclasses of SimpleSignoff*

    ```python
    # my_app/signoffs.py
    from signoffs.signoffs import SimpleSignoff, RevokableSignoff, IrrevokableSignoff
    
    my_signoff = SimpleSignoff.register(id='my_app.signoffs.my_signoff')
   
    my_revokable_signoff = RevokableSignoff.register(id='my_app.signoffs.my_revokable_signoff')
   
    my_irrevokable_signoff = IrrevokableSignoff.register(id='my_app.signoffs.my_irrevokable_signoff')
    ```

2. Configure the signoff relationship in your model:

    ```python
    # my_app/models.py
    
    from signoffs.models import SignoffField
    from my_app.signoffs import my_signoff, my_revokable_signoff, my_irrevokable_signoff
    
    class MyModel(models.Model):
        # Your existing fields
    
        my_signoff, my_signet = SignoffField(my_signoff)
        my_revokable_signoff, my_revokable_signet = SignoffField(my_revokable_signoff)
        my_irrevokable_signoff, my_irrevokable_signet = SignoffField(my_irrevokable_signoff)

    ```
## Using your signoffs
now that you have registered your signoffs and added the SignoffField to your model, we can explore how to use them.


1. Integrate the signoff in your views:

    ```python
    # my_app/views.py
    from my_app.models import MyModel
    from my_app.signoffs import my_signoff, my_revokable_signoff, my_irrevokable_signoff
   
    def my_view(request):
    # integrate into current view logic
        model_instance = MyModel.objects.get(user=request.user)
        if request.method =='POST':
            signoff_form = model_instance.my_signoff.forms.get_signoff_form(request.POST)
            if signoff_form.is_valid():
                signoff_form.sign(user=request.user)
        signoff = model_instance.my_signoff
        context = {"signoff": signoff()}
        
        return render('my_template', context)
    ```

* In your html template, render your signoff with the signoff template tag as shown below.
   ```{note}
   When rendering a signoff with signoff template tags, use the following structure for your div class:
   class="signoff {signoff type prefix}-signoff"
   ```

   ```html
   <!-- myapp/templates/myapp/my_template.html -->
    {% load signoff_tags %}
   <div class="signoffs simple-signoff">
        {{ render_signoff signoff }}
   </div>
   ```

## Conclusion

Congratulations! You've successfully configured and integrated a simple signoff using django-signoffs. This feature will help you streamline approval workflows within your Django application.

For more advanced configurations and customization options, refer to the package's documentation at [link-to-documentation].

If you encounter any issues or need further assistance, don't hesitate to reach out to our support team at [support-email@example.com].

Happy coding!

Replace `[Your Django Package Name]`, `[link-to-documentation]`, and `[support-email@example.com]` with your package's actual name, documentation link, and support email address, respectively.

[//]: # (Replace the placeholders with actual names and details specific to your package and project.
This template covers the installation, configuration, integration, and usage of the signoff feature in a step-by-step manner.
Make sure to provide any additional information users might need and tailor the instructions to match your package's functionality.)