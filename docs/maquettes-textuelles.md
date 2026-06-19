# Maquettes textuelles — QuestBoard

> Version 1 — maquettes fonctionnelles textuelles  
> Objectif : décrire les écrans principaux avant de produire les composants UI.

---

## 1. Structure globale de l’application

### 1.1 Navigation principale

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ QuestBoard                                      [+ Capture] [Mode discret]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Dashboard | Inbox | Projets | Calendrier | Historique | Camp               │
└─────────────────────────────────────────────────────────────────────────────┘
```

Comportement :

- **Dashboard** est l’écran par défaut.
- **Camp** peut être masqué par le mode discret.
- Le bouton **+ Capture** est toujours visible.
- Le raccourci clavier de capture rapide ouvre la même fenêtre que le bouton.

---

## 2. Vue Dashboard / Aujourd’hui

### 2.1 Objectif

Permettre de comprendre rapidement :

- ce qui est planifié ;
- ce qui est en cours ;
- ce qui attend une relance ;
- ce qui peut être repris ;
- ce qu’il serait pertinent de faire ensuite.

### 2.2 Maquette textuelle

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Dashboard — Aujourd’hui                                         Jeudi 18/06 │
│ Vue jour | Vue semaine                                  [Filtres] [Réglages]│
├─────────────────────────────────────────────────────────────────────────────┤
│ AGENDA / CALENDRIER LOCAL                                                   │
│ ┌───────────────┬─────────────────────────────────────────────────────────┐ │
│ │ 09:00 - 09:30 │ Daily / point équipe                                    │ │
│ │ 10:00 - 11:00 │ MEO prévue — changement firewall                        │ │
│ │ 14:00 - 15:00 │ Réunion projet messagerie                               │ │
│ └───────────────┴─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ PLANIFIÉ AUJOURD’HUI                                                        │
│ [Haute] [MEO] Valider prérequis changement Netscaler                        │
│ [Normale] [Réunion] Préparer les points pour comité messagerie              │
├─────────────────────────────────────────────────────────────────────────────┤
│ EN COURS                                                                    │
│ [Critique] [Incident] MECM Remote Control Windows 11                        │
│   Dernière note : règles firewall OK, pas de trace CmRcService.log          │
│   Actions : [Ouvrir] [Ajouter note] [Mettre en attente] [Terminer]          │
│                                                                             │
│ [Haute] [Audit] Assainissement règles transport Exchange                    │
│   Dernière note : exports disponibles, première passe à faire               │
│   Actions : [Ouvrir] [Ajouter note] [Planifier] [Terminer]                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ EN ATTENTE / À RELANCER                                                     │
│ [À relancer] NOC — vérifier drops port 2701                                 │
│ [En attente] RSSI — avis délégation domaine Mailjet                         │
│   Actions rapides : [Relancer aujourd’hui] [Dans 2 jours] [Lundi prochain]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ REPRENDRE                                                                    │
│ Derniers sujets modifiés récemment :                                        │
│ - BAL DRH — inventaire N1/N2                                                │
│ - Audit mail — matrice flux SMTP                                            │
│ - Récupération CSV RH                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ À FAIRE PROPOSÉ                                                             │
│ [Normale] [Documentation] Mettre à jour note d’exploitation BAL DRH          │
│ [Basse] [Veille] Relire notes alternatives O365                             │
│                                                                             │
│ Affichage : 8 tâches maximum par défaut — [Voir plus]                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Règles d’affichage

- L’agenda est toujours en haut.
- Les tâches planifiées du jour passent avant les tâches non planifiées.
- Les tâches en cours doivent être visibles sans recherche.
- Les tâches à relancer doivent être clairement identifiables avec un badge discret.
- Le nombre de tâches affichées est réglable, avec **8** par défaut.
- L’XP/or potentiel de la journée n’est pas affiché.
- Les éléments RPG ne sont pas visibles dans cette vue.

---

## 3. Capture rapide

### 3.1 Objectif

Créer une entrée en moins de 10 secondes.

### 3.2 Capture ultra-rapide

```text
┌──────────────────────────────────────────────────────────────┐
│ Capture rapide                                                │
├──────────────────────────────────────────────────────────────┤
│ Titre                                                         │
│ [__________________________________________________________]  │
│                                                              │
│ Suggestions automatiques :                                   │
│ Type : [Demande]     Priorité : [Normale]                    │
│                                                              │
│ [Créer dans Inbox] [Créer tâche] [Plus d’options] [Annuler]  │
└──────────────────────────────────────────────────────────────┘
```

Comportement :

- Si seul le titre est saisi, l’entrée part dans l’Inbox.
- QuestBoard propose type/priorité, mais l’utilisateur peut les corriger.
- La capture ne doit jamais forcer la saisie d’un projet, d’une date ou d’une description.

### 3.3 Capture avec options

```text
┌──────────────────────────────────────────────────────────────┐
│ Capture rapide — options                                      │
├──────────────────────────────────────────────────────────────┤
│ Titre            [________________________________________]   │
│ Type             [Incident ▼]                                │
│ Priorité         [Haute ▼]                                   │
│ Source           [Ticket ▼]                                  │
│ Projet/Domaine   [Optionnel ▼]                               │
│ Statut           [À faire ▼]                                 │
│ Date prévue      [Optionnel]                                 │
│ Relance          [Optionnel]                                 │
│ Notes rapides    [________________________________________]   │
│                                                              │
│ [Créer] [Créer et ouvrir] [Annuler]                          │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Vue Inbox

### 4.1 Objectif

Capturer sans réfléchir, puis qualifier plus tard.

### 4.2 Maquette textuelle

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Inbox                                                        [Traiter tout] │
├─────────────────────────────────────────────────────────────────────────────┤
│ Entrée brute                                                                  │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ “Relancer NOC sur flux MECM 2701”                                      │ │
│ │ Source : demande | créé aujourd’hui 10:42                              │ │
│ │ Actions : [Tâche] [Projet] [Note] [Relance] [Archiver]                 │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Copie mail / log / note libre                                          │ │
│ │ Source : mail | créé hier 16:20                                        │ │
│ │ Aperçu : “Bonjour, pouvez-vous vérifier...”                            │ │
│ │ Actions : [Tâche] [Projet] [Note] [Relance] [Archiver]                 │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Transformation d’une entrée

```text
Transformer en tâche

Titre             [Relancer NOC sur flux MECM 2701]
Type              [Suivi / relance]
Priorité          [Haute]
Source            [Demande]
Projet/Domaine    [MECM]
Statut            [En attente]
Date de relance   [Lundi prochain]
Notes             [Texte original conservé ici]

[Créer tâche] [Créer et ouvrir] [Annuler]
```

---

## 5. Vue Projets

### 5.1 Vue liste compacte

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Projets                                             [Liste] [Kanban] [+]    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Filtres : Domaine [Tous ▼]  Statut [Actifs ▼]  Type [Temporaires ▼]         │
├─────────────────────────────────────────────────────────────────────────────┤
│ [Audit] Infrastructure mail                                                 │
│   Progression : 42 % | Dernière note : collectes SMTP OK                    │
│   Prochaine action : analyser règles transport obsolètes                    │
│   Actions : [Ouvrir] [Ajouter note] [Archiver]                              │
│                                                                             │
│ [MECM] Remote Control Windows 11                                             │
│   Progression : 20 % | Dernière note : port 2701 écoute côté client         │
│   Prochaine action : vérifier piste mise à jour Windows 11                  │
│   Actions : [Ouvrir] [Ajouter note] [Planifier]                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Fiche projet

```text
Projet : Audit infrastructure mail
Domaine : Exchange / Messagerie
Statut : Actif
Progression : automatique, basée sur les tâches terminées

Dernière note
- Les exports SMTP sont disponibles. Nettoyage des flux à poursuivre.

Prochaine action recommandée
- Identifier les règles de transport désactivées ou obsolètes.

Tâches associées
- [En cours] Assainissement règles transport
- [À faire] Qualifier flux InternalRelay
- [En attente] Avis RSSI Mailjet

Historique
- 18/06 : ajout archive analyse SMTP
- 17/06 : consolidation matrice flux
```

### 5.3 Vue Kanban par projet

```text
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Audit mail   │ MECM         │ BAL DRH      │ RH / IMAJ    │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Règles trans │ Remote Win11 │ Inventaire   │ CSV gi_uo    │
│ InternalRelay│ Firewall 2701│ Groupes secu │ Références   │
│ Cartographie │ Logs client  │ Notes N1/N2  │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 6. Vue Calendrier local

### 6.1 Objectif

Offrir une planification locale en attendant une éventuelle intégration Microsoft.

### 6.2 Vue semaine minimale

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Calendrier local — Semaine du 18/06                         [+ Événement]  │
├────────────┬────────────┬────────────┬────────────┬────────────┬───────────┤
│ Lundi      │ Mardi      │ Mercredi   │ Jeudi      │ Vendredi   │ Notes     │
├────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│            │            │            │ 09:00 Daily│            │           │
│            │            │            │ 10:00 MEO  │            │           │
│            │            │            │ 14:00 Mail │            │           │
└────────────┴────────────┴────────────┴────────────┴────────────┴───────────┘
```

### 6.3 Créer un bloc depuis une tâche

```text
Planifier la tâche

Tâche : Préparer GDC règle transport
Date : [18/06/2026]
Début : [15:30]
Fin : [16:00]
Type d’événement : [Créneau de travail]

[Créer bloc local] [Annuler]
```

---

## 7. Vue Camp

### 7.1 Objectif

Permettre une pause courte, non intrusive, centrée sur la compagnie itinérante.

### 7.2 Maquette textuelle

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Camp — Compagnie des routes grises                         [Retour Dashboard]│
├─────────────────────────────────────────────────────────────────────────────┤
│ Compagnie niveau 1        XP : 45 / 100       Or : 30       Provisions : 4   │
├─────────────────────────────────────────────────────────────────────────────┤
│ CAMP                                                                        │
│ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐    │
│ │ Feu de camp          │ │ Tente de repos       │ │ Chariot intendance   │    │
│ │ Accueil              │ │ Niveau 0 : couverture│ │ Ressources           │    │
│ │ Rapport récent       │ │ [Améliorer 25 or]    │ │ Provisions / or      │    │
│ └─────────────────────┘ └─────────────────────┘ └─────────────────────┘    │
│ ┌─────────────────────┐ ┌─────────────────────┐                            │
│ │ Table de cartes      │ │ Coffre de compagnie  │                            │
│ │ Expéditions          │ │ Butin futur          │                            │
│ └─────────────────────┘ └─────────────────────┘                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ CAPITAINE                                                                    │
│ Nom : [à définir]        Classe : Rôdeur        Niveau : 1                  │
│ Statut : disponible      XP : 45 / 100                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ EXPÉDITION EN COURS                                                          │
│ Aucune expédition active                                                     │
│                                                                             │
│ Expéditions disponibles :                                                    │
│ [30 min] Reconnaissance du vieux sentier — Risque faible — Bon 80 %          │
│   Coût : 1 provision | Récompense : XP + or                                  │
│   [Lancer]                                                                   │
│                                                                             │
│ [1 h] Escorte d’un chariot isolé — Risque moyen — Correct 65 %               │
│   Coût : 2 provisions | Récompense : or                                      │
│   [Lancer]                                                                   │
│                                                                             │
│ [2 h] Fouille des ruines basses — Risque moyen — Correct 60 %                │
│   Coût : 3 provisions | Récompense : XP + or + provisions possibles          │
│   [Lancer]                                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Expédition active

```text
EXPÉDITION EN COURS

Reconnaissance du vieux sentier
Capitaine envoyé : Regias, Rôdeur niveau 1
Temps restant : 18 min
Risque : faible
Chance de réussite : Bon — 80 %

QuestBoard peut être fermé ou ignoré. Le résultat attendra ton retour.
```

### 7.4 Rapport d’expédition

```text
Rapport d’expédition

Regias a suivi les traces d’un ancien chemin de ronde envahi par les herbes.
La route était plus calme que prévu. Au retour, il rapporte quelques pièces,
un croquis utile et assez de vivres pour repartir bientôt.

Résultat : réussite correcte
Gains : +12 XP compagnie, +12 XP capitaine, +8 or, +1 provision
État : disponible

[Récupérer] [Voir Camp]
```

---

## 8. Mode discret

### 8.1 État normal

```text
Navigation : Dashboard | Inbox | Projets | Calendrier | Historique | Camp
Bouton : [Mode discret]
```

### 8.2 Mode discret actif

```text
Navigation : Dashboard | Inbox | Projets | Calendrier | Historique
Bouton : [Mode normal]
```

Comportement :

- L’onglet Camp disparaît.
- Les marqueurs RPG explicites sont masqués dans le Dashboard.
- Les données RPG ne sont pas supprimées.
- Le mode discret peut être activé par raccourci clavier.

---

## 9. Historique / journal de travail

### 9.1 Objectif

Conserver une trace sobre des tâches terminées.

### 9.2 Maquette textuelle

```text
Historique — Travail

18/06/2026
- [Terminé] Préparer inventaire BAL DRH — Documentation — +25 XP
- [Terminé] Relancer NOC port 2701 — Suivi / relance — +10 XP
- [Terminé] Réunion projet messagerie — Réunion — +10 XP

Filtres : période, type, domaine, projet, statut
Export : Markdown plus tard
```

---

## 10. Règles UX transverses

- Toute création doit pouvoir être faite rapidement.
- Les champs avancés restent optionnels.
- L’utilisateur ne doit pas être forcé à qualifier parfaitement une tâche dès la capture.
- Les états de retard ou relance doivent être visibles mais discrets.
- Le Dashboard ne doit pas afficher de langage RPG en mode sérieux.
- Le Camp ne doit pas générer de notification intrusive.
- Aucun retour tardif dans le Camp ne doit être puni.
- Les visuels pixel art ne sont pas nécessaires pour la V0/MVP.
- Les placeholders sont acceptés tant que les écrans restent lisibles.
