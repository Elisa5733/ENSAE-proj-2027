# Projet Python pour la Data Science

*Par Elisa Desloges, Maxime Girard, Amélie Thiebault* 

## Table des matières
1. [Sujet](#sujet)
2. [Problématique](#pblm)
3. [Données utilisées](#donnees)
4. [Présentation du dépôt](#pres)


## 1. Sujet <a name="sujet">

3,5 % : c’est la part de la population qu’il faudrait pour faire tomber n’importe quel gouvernement.

Cette règle a été théorisée par la chercheuse américaine Erica Chenoweth et sa consœur Maria J. Stephan en 2013 dans *Why Civil Resistance Works*. En étudiant 323 mouvements de contestation entre 1900 et 2006, les chercheuses ont observé qu'aucun gouvernement n'a résisté face à un mouvement civil non violent ayant réussi à mobiliser au moins 3,5 % de la population de son pays au plus fort de la crise.

Dans le contexte actuel de mobilisations en Europe, nous avons décidé de mettre à l’épreuve cette règle et d’analyser ce qui fait qu’un mouvement réussit ou non.


## 2. Problématique <a name="pblm">

Pour comprendre les ressorts réels d'une contestation efficace, deux questions s'imposent. Qu'est-ce qu'un soulèvement réussi ? La seule masse des participants suffit-elle à expliquer le succès d'une mobilisation ? 


## 3. Données utilisées <a name="donnees">

Nous avons utilisé deux bases de données pour ce projet :
- [NAVCO 2.1](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MHOXDV), une base de données qui recense les campagnes de masse (violentes et non violentes) visant un changement de régime, une lutte anti-occupation ou une sécession entre 1945 et 2013.
- [Our World in Data](https://ourworldindata.org/grapher/population?tab=table&time=latest&country=OWID_NAM~OWID_SAM~OWID_ASI~OWID_EUR), base de données sur la population.


## 4. Présentation du dépôt <a name="pres">

La partie essentielle de notre projet se trouve dans le fichier ```Main_notebook.ipynb``` qui contient les principales étapes de l'analyse ainsi que les résultats. Le code a été exécuté en amont pour pouvoir présenter les résultats. 
Toutes les étapes de nettoyage, de corrections et les merges sur les données utilisées se trouvent dans le deuxième fichier : ```Cleanup.ipynb```

Dans le dossier ```Data```, on retrouve les bases de données que nous avons utilisé pour ce projet.

Le dossier ```Graphiques``` est consacré à tous les graphiques qui apparaissent dans notre projet.

Avant d'exécuter le notebook, il faut installer la bibliothèque python-calamine (dans un terminal, saisir pip install python-calamine).
Les cellules de main_notebook doivent être effectuées dans l'ordre. Les cellules de cleanup sont exécutées automatiquement depuis main_notebook.
