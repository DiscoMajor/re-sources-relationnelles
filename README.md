docker compose run --rm web python manage.py migrate (à refaire après un git pull)

Bonnes pratiques (nommage etc.)

Nous nous baserons sur le PEP 8 de python (https://peps.python.org/pep-0008/) qui est en anglais, ci dessous un résumé en français.

- Indentation du code : 

  Utiliser 4 espaces par niveau d'indentation (à configurer sur votre IDE)
  /!\ Ce sont bien des espaces et non des tabulations (Tabs) 

- Longueur maxi d'une ligne

  Limiter toutes les lignes a 79 caractères maximum

- Annotation dans des chaines de caractères

  Les doubles quotes seront d'usages.
    Exemple : (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
  Dans le cas ou des annotations devrait se trouver dans la chaine nous utiliserons les annotations simples dans celle-ci pour plus de lisibilité.
    Exemple : (
            "This a string with 'single quote' on it"
          )

  - Espaces dans les expressions

    Eviter les espaces supplémentaires dans les cas suivants :

      Immediately inside parentheses, brackets or braces:

          # Correct:
          spam(ham[1], {eggs: 2})
          
          # Wrong:
          spam( ham[ 1 ], { eggs: 2 } )
          
          Between a trailing comma and a following close parenthesis:
          
          # Correct:
          foo = (0,)
          
          # Wrong:
          bar = (0, )
          
          Immediately before a comma, semicolon, or colon:
          
          # Correct:
          if x == 4: print(x, y); x, y = y, x
          
          # Wrong:
          if x == 4 : print(x , y) ; x , y = y , x

- Convention de nommage

  lower_case_with_underscore


!!TBC!!

Documentation de libs et framework utilisés : 

Tailwind CSS : https://tailwindcss.com/docs/styling-with-utility-classes

Django : https://docs.djangoproject.com/en/5.1/

Stimulus JS : https://stimulus.hotwired.dev/
