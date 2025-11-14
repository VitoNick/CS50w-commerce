from django.db import models


class CategoryChoices(models.TextChoices):
    PETS = "PE", "Pets"
    ELECTRONICS = "EL", "Electronics"
    TOOLS = "TL", "Tools"
    VEHICLES = "VE", "Vehicles"
    BOOKS = "BK", "Books"
    TOYS = "TO", "Toys"
    OTHER = "OT", "Other"