# Fiche MVP — QuestBoard

## Objectif du MVP

Le MVP doit valider la boucle complète :

> Capturer une tâche → la suivre → la terminer → gagner XP / or / provisions → lancer une expédition → récupérer un rapport narratif et une récompense.

Le MVP ne cherche pas encore à être beau, complet ou connecté à Microsoft 365. Il doit prouver que l’outil est utilisable et motivant.

## MVP Dashboard

Fonctionnalités à inclure :

- création rapide de tâche ;
- capture avec titre seul possible ;
- qualification minimale : titre, type, priorité ;
- inbox dédiée ;
- transformation d’une entrée inbox en tâche, projet, note ou relance ;
- statuts de base : inbox, à faire, en cours, en attente, planifié, terminé, abandonné ;
- date de relance sur une tâche en attente ;
- vue Aujourd’hui ;
- projets et domaines personnalisables ;
- notes simples ;
- liens externes simples ;
- clôture de tâche ;
- calcul automatique XP / or ;
- historique minimal.

## MVP Camp

Fonctionnalités à inclure :

- compagnie niveau 1 ;
- capitaine fondateur créé par l’utilisateur ;
- ressources : XP, or, provisions ;
- camp fonctionnel sous forme de cartes / menus ;
- une expédition active maximum ;
- choix d’une expédition ;
- coût en provisions ;
- durée automatique ;
- taux de réussite affiché ;
- résolution non punitive ;
- rapport narratif court ;
- récompenses ;
- achat d’une première amélioration : tente de repos.

## Hors périmètre MVP

- synchronisation Microsoft Graph ;
- notifications Windows ;
- gestion multi-utilisateurs ;
- application mobile native ;
- intégration ticketing ;
- import automatique de mails ;
- IA embarquée ;
- statistiques avancées ;
- carte du monde complexe ;
- pixel art définitif ;
- équipement détaillé ;
- objets rares ;
- traits de personnalité ;
- plusieurs expéditions simultanées.

## V0 technique préalable

Avant le MVP complet, une V0 technique courte est recommandée :

- Docker Compose ;
- API FastAPI ;
- frontend SvelteKit ;
- base SQLite ;
- modèle Task minimal ;
- capture rapide ;
- clôture de tâche ;
- calcul XP / or minimal.

## Critères de réussite

Le MVP est réussi si :

- une tâche peut être capturée en quelques secondes ;
- la vue Aujourd’hui aide réellement à reprendre le fil ;
- une tâche terminée génère une récompense ;
- les récompenses permettent de lancer une expédition ;
- l’expédition se résout sans attention continue ;
- le Camp donne envie d’être consulté pendant une pause courte ;
- l’usage reste sobre et non intrusif.
