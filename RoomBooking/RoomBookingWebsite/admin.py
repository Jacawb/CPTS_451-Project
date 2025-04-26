from django.contrib import admin
from django.apps import apps
from .models import Student, StudentRoommates


# Get all models of your app
app = apps.get_app_config('RoomBookingWebsite') 

# Register each model automatically
# for model_name, model in app.models.items():
#     admin.site.register(model)
  
for model_name, model in app.models.items():
    if model_name != 'student': 
        admin.site.register(model)

def match_students(modeladmin, request, queryset):
    unmatched = list(Student.objects.filter(matched=False).select_related('preferences'))
    pairs = []

    while unmatched:
        student = unmatched.pop(0)
        best_match = None
        best_score = -1

        for potential in unmatched:
            if student == potential or not potential.preferences:
                continue

            score = student.preferences.match_score(potential.preferences)

            if score > best_score:
                best_score = score
                best_match = potential

        if best_match:
            unmatched.remove(best_match)

            StudentRoommates.objects.create(student1=student, student2=best_match)

            student.roommates.add(best_match)
            best_match.roommates.add(student)

            student.matched = True
            best_match.matched = True
            student.save()
            best_match.save()

            pairs.append((student, best_match))

    modeladmin.message_user(request, f"{len(pairs)} roommate pairs assigned.")

    @admin.register(Student)
    class StudentAdmin(admin.ModelAdmin):
        list_display = ['user', 'gender', 'age', 'matched']
        actions = [match_students]

