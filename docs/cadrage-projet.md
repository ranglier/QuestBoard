# Cadrage projet — QuestBoard

## Synthèse

**QuestBoard** est un outil personnel, local-first, orienté travail professionnel.

Il poursuit deux objectifs complémentaires :

1. **Dashboard** : piloter le quotidien professionnel, visualiser les tâches, réunions, projets, relances, sujets en attente et interruptions.
2. **Camp** : proposer une pause courte sous forme d’un mini idle RPG d’expéditions, alimenté par les tâches réellement accomplies.

Principe central :

> Le travail réel alimente le jeu. Le jeu offre une pause courte, sans demander une attention continue.

## Décisions produit

- Le projet s’appelle **QuestBoard**.
- L’application comporte deux espaces séparés : **Dashboard** et **Camp**.
- Le Dashboard est l’espace sérieux, affiché par défaut.
- Le Camp est l’espace RPG, consultable pendant les pauses.
- Un mode discret permet de masquer le Camp et les marqueurs explicitement RPG.
- QuestBoard est personnel, local-first et non collaboratif.
- Le dépôt peut être public, mais aucune donnée professionnelle réelle ne doit être publiée.

## Dashboard

Le Dashboard doit permettre de :

- créer rapidement des tâches ;
- suivre les tâches en cours ;
- visualiser l’agenda et les éléments planifiés ;
- gérer une inbox dédiée ;
- suivre les projets et domaines ;
- suivre les tâches en attente ou à relancer ;
- conserver des notes utiles pour reprendre le contexte ;
- clôturer une tâche et générer des récompenses.

## Camp / RPG

La couche RPG est un mini idle RPG d’expéditions.

Décisions principales :

- compagnie itinérante d’aventuriers ;
- camp / bivouac comme base mobile ;
- capitaine jouable, créé par l’utilisateur ;
- un seul fondateur au départ ;
- ressources V1 : XP, or, provisions ;
- une seule expédition active dans le MVP ;
- durées d’expédition V1 : 30 min, 1 h, 2 h ;
- résultat non punitif : récompense réduite, fatigue, blessure légère, repos ;
- rapport narratif court ;
- première amélioration : tente de repos ;
- style visuel cible : pixel art, mais pas de pixel art définitif pendant le prototypage.

Classes V1 :

- Guerrier ;
- Rôdeur ;
- Mage ;
- Soigneur ;
- Artisan.

## Stack technique validée

- Frontend : **SvelteKit**.
- Backend : **FastAPI**.
- Base : **SQLite**.
- Déploiement : **Docker Compose dès le départ**.
- API propre dès le départ.
- Séparation stricte : code, données, exports, sauvegardes.

## Contraintes Microsoft

L’intégration Microsoft est importante pour l’adoption réelle, mais elle est traitée comme un chantier séparé après le MVP.

Approche retenue :

1. V0/MVP avec calendrier local QuestBoard.
2. Import manuel ou semi-manuel si utile.
3. Intégration Microsoft réelle à réévaluer plus tard selon la voie d’authentification possible.

## Risques principaux

- Friction de saisie.
- Intégration Microsoft.
- Surcomplexité.
- Données sensibles.
- Jeu trop distrayant.

Mesures de réduction :

- capture rapide en un titre ;
- champs avancés optionnels ;
- Dashboard affiché par défaut ;
- mode discret ;
- local-first ;
- pas de notifications Windows ;
- pas de clic répétitif ;
- une seule expédition active ;
- aucune punition si le joueur ne revient pas.
