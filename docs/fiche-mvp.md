# Fiche MVP — QuestBoard

> Version 1 — périmètre MVP stabilisé  
> Objectif : définir la plus petite version utile permettant de tester la promesse centrale de QuestBoard.

---

## 1. Vision courte

**QuestBoard** est un outil personnel local-first destiné à piloter le quotidien professionnel tout en alimentant un mini-jeu RPG de pause.

Le MVP doit valider la boucle :

> Capturer une tâche → la suivre → la terminer → gagner XP/or/provisions → lancer une expédition → récupérer un rapport et une récompense.

Le MVP ne cherche pas encore à être beau, complet ou connecté à Microsoft 365. Il cherche à prouver que l’outil est utilisable et motivant.

---

## 2. Utilisateur cible

Utilisateur unique : administrateur / ingénieur système.

Besoins prioritaires :

- ne pas perdre le fil des sujets en cours ;
- capturer rapidement une tâche ou une note ;
- visualiser ce qui est planifié, actif, en attente ou à relancer ;
- éviter une liste interminable ;
- obtenir une récompense ludique après les tâches accomplies ;
- faire une pause courte dans un mini-jeu non intrusif.

---

## 3. Périmètre MVP

Le MVP contient deux espaces :

- **Dashboard** : suivi sérieux des tâches, projets, agenda local et relances.
- **Camp** : mini idle RPG d’expéditions.

### 3.1 Dashboard MVP

Fonctionnalités incluses :

- création rapide de tâche ;
- capture ultra-rapide avec titre seul ;
- attribution ou suggestion d’un type et d’une priorité ;
- inbox dédiée ;
- transformation d’une entrée inbox en tâche, projet, note ou relance ;
- statuts de base ;
- vue Aujourd’hui ;
- vue Projets ;
- domaines personnalisables ;
- tâches en attente avec date de relance ;
- vue dédiée aux relances ;
- notes simples ;
- liens externes simples ;
- calendrier local en vue semaine si raisonnable ;
- clôture d’une tâche ;
- calcul automatique XP/or ;
- historique minimal des tâches terminées.

### 3.2 Camp MVP

Fonctionnalités incluses :

- compagnie niveau 1 ;
- création du capitaine fondateur ;
- choix d’une classe parmi : guerrier, rôdeur, mage, soigneur, artisan ;
- ressources : XP, or, provisions ;
- affichage du camp sous forme de cartes ou menus ;
- une expédition active maximum ;
- durées d’expédition : 30 min, 1 h, 2 h ;
- coût en provisions ;
- taux de réussite calculé puis affiché en libellé + pourcentage (formule : voir `docs/economie-rpg.md`) ;
- résolution automatique ;
- aucun échec punitif ;
- états **Fatigué** / **Blessé** de l’aventurier après un revers ;
- rapport narratif court ;
- récompenses ;
- première amélioration de camp : tente de repos.

---

## 4. V0 technique avant MVP

Avant le MVP complet, une V0 technique très courte doit être créée.

Objectif : valider la stack et le socle.

Contenu V0 :

- dépôt projet structuré ;
- Docker Compose ;
- frontend SvelteKit ;
- backend FastAPI ;
- base SQLite ;
- modèle `Task` minimal ;
- création rapide d’une tâche ;
- liste de tâches ;
- clôture d’une tâche ;
- calcul XP/or minimal.

Critère de réussite V0 :

> Depuis l’interface web locale, l’utilisateur peut créer une tâche, la terminer, et voir XP/or calculés.

---

## 5. Hors périmètre MVP

Sont exclus du MVP :

- intégration Microsoft Graph ;
- synchronisation Outlook / To Do / Planner ;
- application mobile ;
- notifications Windows ;
- multi-utilisateur ;
- gestion collaborative ;
- sauvegarde/restauration complète ;
- IA embarquée ;
- imports automatiques de mails ou tickets ;
- pixel art définitif ;
- carte du monde ;
- plusieurs expéditions simultanées ;
- équipement détaillé ;
- objets rares ;
- traits de personnalité ;
- journal de compagnie dédié.

---

## 6. Critères d’acceptation MVP

Le MVP est considéré comme atteint si :

1. L’application démarre localement via Docker Compose.
2. Le Dashboard est affiché par défaut.
3. L’utilisateur peut capturer une tâche en quelques secondes.
4. L’utilisateur peut consulter une vue Aujourd’hui exploitable.
5. L’utilisateur peut envoyer une entrée d’inbox vers une tâche ou une note.
6. L’utilisateur peut suivre un projet avec notes et tâches associées.
7. L’utilisateur peut créer une tâche en attente avec date de relance.
8. Une tâche terminée génère XP/or selon les règles de scoring.
9. Les ressources sont visibles dans le Camp.
10. L’utilisateur peut créer son capitaine fondateur.
11. L’utilisateur peut lancer une expédition.
12. L’expédition se termine automatiquement après sa durée.
13. Le rapport d’expédition est affiché.
14. Les récompenses de l’expédition sont créditées.
15. L’utilisateur peut acheter ou améliorer la tente de repos.

---

## 7. Risques MVP

### Friction de saisie

Risque principal. La capture doit rester extrêmement rapide.

Mesures :

- champ titre seul possible ;
- type/priorité proposés ;
- qualification différée ;
- raccourci clavier souhaité.

### Surcomplexité RPG

Le Camp ne doit pas ralentir le Dashboard.

Mesures :

- une seule expédition active ;
- pas d’équipement détaillé ;
- pas de carte ;
- pas d’objets rares en MVP.

### Intégration Microsoft

L’intégration Microsoft est importante mais incertaine.

Mesures :

- calendrier local V1 ;
- intégration Microsoft traitée comme chantier séparé ;
- QuestBoard reste utilisable hors réseau professionnel.

### Données sensibles

QuestBoard manipule des informations professionnelles.

Mesures :

- local-first ;
- pas de cloud obligatoire ;
- libellés sobres recommandés ;
- pas de secrets, tokens, mots de passe ou données RH détaillées.

---

## 8. Scoring MVP

### 8.1 Principe

Le scoring sépare volontairement la progression et la valeur opérationnelle :

- **XP** : basée sur la complexité, l’effort et l’apprentissage.
- **Or** : basé sur la priorité, la valeur immédiate et l’importance opérationnelle.

Formule de base :

```text
Récompense = XP(complexité) + Or(priorité) + bonus automatiques éventuels
```

### 8.2 XP par complexité

| Complexité côté Dashboard | Libellé RPG | XP |
|---|---|---:|
| Très simple | Triviale | 5 |
| Simple | Simple | 10 |
| Standard | Normale | 25 |
| Difficile | Difficile | 50 |
| Complexe | Complexe | 80 |
| Majeure | Boss | 150 |

### 8.3 Or par priorité

| Priorité | Or |
|---|---:|
| Basse | 2 |
| Normale | 5 |
| Haute | 15 |
| Critique | 35 |

### 8.4 Bonus automatiques

| Cas | Bonus XP | Bonus or |
|---|---:|---:|
| Interruption traitée | +0 | +5 |
| Incident critique résolu | +0 | +25 |
| Sujet en attente débloqué | +0 | +10 |
| Documentation produite | +10 | +0 |
| Réunion organisée par l’utilisateur | +10 | +5 |
| Projet / quête terminé | Récompense spéciale | Récompense spéciale |

### 8.5 Répartition XP et or d’expédition

Voir `docs/economie-rpg.md` pour le détail :

- **XP d’une tâche terminée** : **100 % à la compagnie**, **50 % au capitaine** (créditée en plus).
- **Or d’expédition** : gain net visant **~½ du gain or des tâches du jour**, **plafonné sous lui**. Le travail réel reste la principale source d’or.

---

## 9. Roadmap MVP opérationnelle

### Lot 0 — Squelette technique

- dépôt ;
- Docker Compose ;
- SvelteKit ;
- FastAPI ;
- SQLite ;
- healthcheck API.

### Lot 1 — Tâches minimales

- modèle Task ;
- création rapide ;
- liste ;
- clôture ;
- scoring XP/or.

### Lot 2 — Dashboard utile

- vue Aujourd’hui ;
- statuts ;
- priorités ;
- filtres ;
- tâches en cours ;
- tâches en attente / relances.

### Lot 3 — Inbox et projets

- inbox dédiée ;
- transformer en tâche/projet/note/relance ;
- domaines ;
- vue Projets ;
- fiche projet.

### Lot 4 — Calendrier local

- événements locaux ;
- vue semaine ;
- tâches planifiées ;
- lien tâche ↔ bloc calendrier.

### Lot 5 — Camp minimal

- compagnie ;
- capitaine ;
- ressources ;
- camp ;
- expédition ;
- rapport ;
- récompenses ;
- tente de repos.

---

## 10. Définition finale du MVP

Le MVP de QuestBoard est réussi si l’utilisateur peut s’en servir pendant une vraie journée de travail pour :

- capturer rapidement des tâches ;
- retrouver ce qui est prévu, actif, en attente ou à relancer ;
- terminer des tâches ;
- voir une progression ;
- faire une courte pause dans le Camp ;
- lancer et récupérer une expédition sans être distrait en continu.
