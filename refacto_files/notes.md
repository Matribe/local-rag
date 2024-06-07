
#### mettre le moins de parametres dans les methodes possible :

```python
def get_user(self, sql_formula):
    pass

def get_user(self, sql_formula):
    pass
```

==>

```python
def __init__(self, sql_formula):
    self.sql_formula = sql_formula

...
``` 


#### ne pas recréer un objet a chaque fois pour utiliser une de ses methodes

```python
AliasHandler().get_alias()
```

==>

```python
alias_handler = AliasHandler()

alias_handler.get_alias()
```

==> encore mieux si on peut le mettre dans le constructeur

```python
def __init__(self):
    self.alias_handler = AliasHandler()
```


#### ne pas utiliser de variables de classe

```python
class MyClass:
    my_var = 0
```

==>

```python
class MyClass:
    def __init__(self):
        self.my_var = 0
```


#### faire des retours a la ligne dans les string pour que ce soit plus lisible

```python
sql_formula = "SELECT * FROM table WHERE column1 = 'value1' AND column2 = 'value2' AND column3 = 'value3'"
```

==>

```python
sql_formula = """
    SELECT * 
    FROM table 
    WHERE column1 = 'value1' 
    AND column2 = 'value2' 
    AND column3 = 'value3'
"""
```

#### pas besoin de mettre des parentheses pour les fonctions

```python
if (condition):
    pass
```

==>

```python
if condition:
    pass
```

#### créer plein de variables temporaires pour plus de lisibilité et éviter les longues lignes
    
```python
if self.get_user(sql_formula).get(attributes[0]):
    pass
``

==>

```python   
user = self.get_user(sql_formula)
attribute = attributes[0]
if user.get(attribute):
    pass
```


#### Une classe une responsabilité

dans query le process_as_alias devrait etre integré a la classe AliasHandler



#### moi je préfere pas mettre d'explications ni de precision de ce que retourne la variable ou la fonction, je trouve que ca alourdit le code

```python
def get_user(self, sql_formula:str) -> User:
    ''' return the user '''
    pass
```

==>

```python
def get_user(self, sql_formula):
    pass
```

si ton nom de methode est bien choisi normalement pas besoin de preciser ce qu'elle fait

je mets plus des commentaires d'un mots pour regroupers plusieurs methodes qui ont le meme role en faisant CMD + K + CMD + 0


cf ==> refacto_files/editor.py



