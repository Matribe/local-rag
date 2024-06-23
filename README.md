Attention : Nous avons utilisé Python 3.11.9.
Les versions 3.12.XX ne permettent pas de faire fonctionner le projet.

## Installation

Il faut installer ollama : https://ollama.com/


Puis installer Mistral via : 

```bash
ollama pull mistral
```


Vérifier que le serveur ollama est bian lancé via : 

```bash
ollama serve
```

Installer les modules externes :

```bash
pip install -r requirements.txt
```

## Lancement du programme

Pour lancer le projet :  

```bash
streamlit run interface.py
```

---

Si vous souhaitez lancer le projet sans l'interface, directement en ligne de commande :

1. Modifier dans src/settings.py la constante :

```python
SQL_REQUEST = """Votre rêquete SQL"""
```
2. Lancer le fichier principal :

```bash
python main_without_interface.py
```

Ou encore avec python3

```bash
python3 main_without_interface.py
```


## Post-Scriptum

Il est aussi possible d'utiliser le modèle Llama3, pour ce faire :

1. Installer le modèle via 

```bash
ollama pull llama3
```

2. Dans le fichier src/settings.py modifier la constante :

```python
MODEL_LLM = "llama3"
```


## License

MIT License


## Authors

- [Mathieu Ribeyron]()
- [Claire Mathieu]()
- [Robin Violet]()
- [Raphaël Pietrzak]()

