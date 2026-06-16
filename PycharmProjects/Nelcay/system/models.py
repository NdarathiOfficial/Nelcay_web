from django.db import models


class AccessToken(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token


# defined outside the class for easy import in views.py/forms.py
RESIDENCE_CHOICES = [
    ('baringo', 'Baringo'),
    ('bomet', 'Bomet'),
    ('bungoma', 'Bungoma'),
    ('busia', 'Busia'),
    ('elgeyo-marakwet', 'Elgeyo-Marakwet'),
    ('embu', 'Embu'),
    ('garissa', 'Garissa'),
    ('homa-bay', 'Homa Bay'),
    ('isiolo', 'Isiolo'),
    ('kajiado', 'Kajiado'),
    ('kakamega', 'Kakamega'),
    ('kericho', 'Kericho'),
    ('kiambu', 'Kiambu'),
    ('kilifi', 'Kilifi'),
    ('kirinyaga', 'Kirinyaga'),
    ('kisii', 'Kisii'),
    ('kisumu', 'Kisumu'),
    ('kitui', 'Kitui'),
    ('kwale', 'Kwale'),
    ('laikipia', 'Laikipia'),
    ('lamu', 'Lamu'),
    ('machakos', 'Machakos'),
    ('makueni', 'Makueni'),
    ('mandera', 'Mandera'),
    ('marsabit', 'Marsabit'),
    ('meru', 'Meru'),
    ('migori', 'Migori'),
    ('mombasa', 'Mombasa'),
    ('muranga', 'Muranga'),
    ('nairobi', 'Nairobi'),
    ('nakuru', 'Nakuru'),
    ('nandi', 'Nandi'),
    ('narok', 'Narok'),
    ('nyamira', 'Nyamira'),
    ('nyandarua', 'Nyandarua'),
    ('nyeri', 'Nyeri'),
    ('samburu', 'Samburu'),
    ('siaya', 'Siaya'),
    ('taita-taveta', 'Taita Taveta'),
    ('tana-river', 'Tana River'),
    ('tharaka-nithi', 'Tharaka Nithi'),
    ('trans-nzoia', 'Trans Nzoia'),
    ('turkana', 'Turkana'),
    ('uasin-gishu', 'Uasin Gishu'),
    ('vihiga', 'Vihiga'),
    ('wajir', 'Wajir'),
    ('west-pokot', 'West Pokot'),
]

PASTRY_CHOICES = [
    ('biscuits', 'Biscuits'),
    ('bread', 'Bread'),
    ('brownies', 'Brownies'),
    ('cake', 'Cake'),
    ('cinnamon-rolls', 'Cinnamon Rolls'),
    ('cookies', 'Cookies'),
    ('cupcakes', 'Cupcakes'),
    ('donuts', 'Donuts'),
    ('muffins', 'Muffins'),
    ('pies', 'Pies'),
    ('samosas', 'Samosas'),
    ('scones', 'Scones'),
    ('mandazi', 'Mandazi'),
    ('croissants', 'Croissants')
]

OCCASION_CHOICES = [
    ('anniversary', 'Anniversary'),
    ('baby-shower', 'Baby Shower'),
    ('birthday', 'Birthday'),
    ('farewell-party', 'Farewell Party'),
    ('gender-reveal', 'Gender Reveal'),
    ('housewarming', 'Housewarming'),
    ('promotion', 'Promotion'),
    ('retirement-party', 'Retirement Party'),
    ('wedding', 'Wedding'),
]

FLAVOUR_CHOICES = [
    ('almond-cake', 'Almond Cake'),
    ('apple-cinnamon', 'Apple Cinnamon'),
    ('banana', 'Banana'),
    ('black-forest', 'Black Forest'),
    ('blueberry', 'Blueberry'),
    ('butter-cake', 'Butter Cake'),
    ('caramel', 'Caramel'),
    ('cheese-layered-cake', 'Cheese Layered Cake'),
    ('chocolate', 'Chocolate'),
    ('chocolate-fudge', 'Chocolate Fudge'),
    ('coconut-cake', 'Coconut Cake'),
    ('lemon', 'Lemon'),
    ('lemon-vanilla', 'Lemon Vanilla'),
    ('mango', 'Mango'),
    ('marble', 'Marble'),
    ('mixed-fruit', 'Mixed Fruit'),
    ('mocha', 'Mocha'),
    ('nutella', 'Nutella'),
    ('nutty-carrot-cake', 'Nutty Carrot Cake'),
    ('orange', 'Orange'),
    ('oreo', 'Oreo'),
    ('passion', 'Passion'),
    ('pecan-praline', 'Pecan Praline'),
    ('pineapple', 'Pineapple'),
    ('plain-carrot-cake', 'Plain Carrot Cake'),
    ('red-velvet', 'Red Velvet'),
    ('sponge-cake', 'Sponge Cake'),
    ('spice-cake', 'Spice Cake'),
    ('strawberry', 'Strawberry'),
    ('vanilla', 'Vanilla'),
    ('walnut-cake', 'Walnut Cake'),
    ('white-forest', 'White Forest'),
    ('other', 'Other'),
]

# Prices map to slugs in FLAVOUR_CHOICES
FLAVOUR_PRICES = {
    'almond-cake': 10,
    'apple-cinnamon': 3000,
    'banana': 2500,
    'black-forest': 2800,
    'blueberry': 3000,
    'butter-cake': 3500,
    'caramel': 2700,
    'cheese-layered-cake': 3500,
    'chocolate': 3500,
    'chocolate-fudge': 3200,
    'coconut-cake': 2700,
    'lemon': 2500,
    'lemon-vanilla': 2500,
    'mango': 2600,
    'marble': 2500,
    'mixed-fruit': 3000,
    'mocha': 2800,
    'nutella': 3500,
    'nutty-carrot-cake': 3000,
    'orange': 2500,
    'oreo': 3200,
    'passion': 2600,
    'pecan-praline': 4000,
    'pineapple': 2500,
    'plain-carrot-cake': 2700,
    'red-velvet': 3000,
    'sponge-cake': 2300,
    'spice-cake': 2800,
    'strawberry': 2900,
    'vanilla': 2500,
    'walnut-cake': 3500,
    'white-forest': 3000,
    'other': 2000,
}

MEASUREMENT_CHOICES = [
    ('kgs', 'Kgs'),
    ('pieces', 'Pieces')
]



class OrderHere(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)

    residence = models.CharField(choices=RESIDENCE_CHOICES, max_length=50)
    pastry = models.CharField(choices=PASTRY_CHOICES, max_length=50)
    occasion = models.CharField(choices=OCCASION_CHOICES, max_length=50)
    flavour = models.CharField(choices=FLAVOUR_CHOICES, max_length=50)
    measurement = models.CharField(choices=MEASUREMENT_CHOICES, max_length=6)

    # Changed to DecimalField to allow fractional quantities (e.g. 1.5 Kgs)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)

    message = models.TextField()
    # Added null=True to allow migration on existing databases without a default value prompt
    payment_status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pastry}"


