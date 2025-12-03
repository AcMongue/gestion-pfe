# 📖 MANUEL D'UTILISATION - Système de Gestion des PFE
## École Nationale Supérieure Polytechnique de Douala (ENSPD)

**Version:** 1.0  
**Date:** 3 Décembre 2025  
**Plateforme:** Django 4.2.27

---

## 🎯 Table des matières

1. [Introduction](#introduction)
2. [Accès à la plateforme](#accès-à-la-plateforme)
3. [Guide par rôle](#guide-par-rôle)
   - [Étudiants](#pour-les-étudiants)
   - [Encadreurs](#pour-les-encadreurs)
   - [Administrateurs](#pour-les-administrateurs)
   - [Membres du jury](#pour-les-membres-du-jury)
4. [Fonctionnalités détaillées](#fonctionnalités-détaillées)
5. [FAQ](#faq)
6. [Support technique](#support-technique)

---

## 📌 Introduction

Le système de gestion des Projets de Fin d'Études (PFE) de l'ENSPD est une plateforme web complète qui permet de gérer tout le cycle de vie des projets de fin d'études, depuis la proposition de sujets jusqu'à la soutenance et l'archivage.

### Objectifs de la plateforme

- **Simplifier** le processus de proposition et d'attribution des sujets
- **Faciliter** la communication entre étudiants, encadreurs et administration
- **Automatiser** la planification des soutenances
- **Centraliser** tous les documents et informations liés aux PFE
- **Assurer** le suivi en temps réel de l'avancement des projets

### Fonctionnalités principales

1. ✅ **Gestion des utilisateurs et authentification**
2. ✅ **Catalogue et affectation des sujets**
3. 🚧 **Suivi collaboratif des projets**
4. 🚧 **Communication contextualisée**
5. 🚧 **Planification automatisée des soutenances**
6. 🚧 **Archivage et reporting**

**Légende:** ✅ Fonctionnalité disponible | 🚧 En développement

---

## 🔐 Accès à la plateforme

### URL d'accès

```
http://127.0.0.1:8000/
```

### Première connexion

1. Ouvrez votre navigateur web (Chrome, Firefox, Edge, Safari)
2. Entrez l'URL de la plateforme
3. Vous arrivez sur la page d'accueil

### Inscription

**Pour les nouveaux utilisateurs:**

1. Cliquez sur **"S'inscrire"** dans le menu
2. Remplissez le formulaire avec vos informations:
   - Nom d'utilisateur (unique)
   - Adresse email
   - Prénom et Nom
   - Rôle (Étudiant, Encadreur, Administrateur, Jury)
   - Mot de passe (8 caractères minimum)
3. Cliquez sur **"S'inscrire"**
4. Vous serez redirigé vers votre tableau de bord

### Connexion

**Pour les utilisateurs existants:**

1. Cliquez sur **"Se connecter"**
2. Entrez votre nom d'utilisateur
3. Entrez votre mot de passe
4. Cliquez sur **"Se connecter"**

### Récupération de mot de passe

*Fonctionnalité à venir*

---

## 👥 Guide par rôle

## POUR LES ÉTUDIANTS

### 🎓 Vue d'ensemble

En tant qu'étudiant, vous pouvez:
- Consulter le catalogue des sujets
- Candidater aux sujets qui vous intéressent
- Suivre l'état de vos candidatures
- Collaborer avec votre encadreur sur votre projet
- Préparer votre soutenance

### 📋 Tableau de bord étudiant

Après connexion, votre tableau de bord affiche:

- **Vos statistiques:**
  - Nombre de candidatures en cours
  - Statut de votre affectation
  - Progression de votre projet
  
- **Actions rapides:**
  - Accéder au catalogue des sujets
  - Voir mes candidatures
  - Accéder à mon projet

- **Notifications:**
  - Nouvelles réponses aux candidatures
  - Messages de votre encadreur
  - Dates importantes

### 🔍 Consulter le catalogue des sujets

1. Cliquez sur **"Catalogue des sujets"** dans le menu
2. Vous voyez tous les sujets disponibles pour votre niveau

**Filtrer les sujets:**

- **Recherche textuelle:** Entrez des mots-clés dans la barre de recherche
- **Niveau:** Les sujets sont automatiquement filtrés selon votre niveau (L3, M2, DOC)
- **Domaine:** Filtrez par domaine (Informatique, Réseaux, IA, Web, etc.)
- **Type:** Recherche, Développement, ou Mixte

**Informations affichées pour chaque sujet:**

- Titre et description courte
- Encadreur principal
- Niveau requis
- Domaine et type
- Nombre de places disponibles
- Badges de statut

### 📝 Candidater à un sujet

**Étapes pour candidater:**

1. **Trouver le sujet:** Utilisez les filtres ou la recherche
2. **Consulter les détails:** Cliquez sur le sujet pour voir tous les détails
3. **Vérifier votre éligibilité:**
   - Le sujet est de votre niveau
   - Il reste des places disponibles
   - Vous n'avez pas déjà un sujet affecté
4. **Cliquer sur "Candidater à ce sujet"**
5. **Remplir le formulaire:**
   - **Lettre de motivation (obligatoire):** Rédigez une lettre convaincante expliquant:
     * Pourquoi ce sujet vous intéresse
     * Vos compétences pertinentes
     * Votre motivation et vos objectifs
   - **CV (optionnel):** Uploadez votre CV en PDF, DOC ou DOCX
   - **Priorité (obligatoire):** Choisissez de 1 à 5
     * 1 = Priorité maximale (votre choix préféré)
     * 5 = Priorité minimale
6. **Soumettre la candidature**

**💡 Conseils pour une candidature réussie:**

- Prenez le temps de bien rédiger votre lettre
- Montrez votre connaissance du sujet
- Mettez en avant vos compétences techniques
- Soyez concret et sincère
- Relisez-vous avant de soumettre

### 📊 Suivre vos candidatures

1. Allez dans **"Mes candidatures"**
2. Vous voyez toutes vos candidatures avec leur statut:

**Statuts possibles:**

- 🟡 **En attente:** L'encadreur n'a pas encore évalué
- ✅ **Acceptée:** Félicitations! L'encadreur accepte de vous encadrer
- ❌ **Rejetée:** L'encadreur a choisi un autre étudiant
- ⏸️ **Retirée:** Vous avez retiré votre candidature

**Actions possibles:**

- **Voir les détails:** Cliquez sur une candidature
- **Retirer une candidature:** Si elle est "En attente"
- **Voir les notes de l'encadreur:** Si évaluée

### 🔄 Gérer plusieurs candidatures

**Stratégie recommandée:**

1. **Candidatez à 3-5 sujets** pour maximiser vos chances
2. **Utilisez le système de priorité:**
   - Priorité 1-2: Vos sujets préférés
   - Priorité 3: Sujets intéressants
   - Priorité 4-5: Options de secours
3. **Surveillez régulièrement** l'état de vos candidatures
4. **Retirez les candidatures** si vous êtes accepté ailleurs

### 📂 Mon profil

**Accéder à votre profil:**

1. Cliquez sur votre nom en haut à droite
2. Sélectionnez **"Mon profil"**

**Informations que vous pouvez modifier:**

**Informations personnelles:**
- Prénom et nom
- Email et téléphone
- Photo de profil
- Biographie

**Informations académiques (Étudiants):**
- Matricule
- Niveau d'études (L3, M2, DOC)
- Filière

**Informations supplémentaires:**
- Date de naissance
- Adresse
- Ville et pays
- Liens professionnels (LinkedIn, GitHub, site web)

**Préférences de notifications:**
- Notifications par email
- Notifications par SMS

---

## POUR LES ENCADREURS

### 👨‍🏫 Vue d'ensemble

En tant qu'encadreur, vous pouvez:
- Proposer des sujets de PFE
- Gérer vos sujets (modifier, supprimer)
- Recevoir et évaluer les candidatures
- Accepter ou rejeter des candidatures
- Suivre vos étudiants affectés
- Communiquer avec vos étudiants

### 📊 Tableau de bord encadreur

Votre tableau de bord affiche:

- **Statistiques:**
  - Nombre de sujets proposés
  - Nombre de candidatures reçues
  - Étudiants encadrés actuellement
  
- **Actions rapides:**
  - Proposer un nouveau sujet
  - Voir mes sujets
  - Candidatures en attente
  
- **Alertes:**
  - Nouvelles candidatures
  - Messages des étudiants

### ➕ Proposer un nouveau sujet

**Étapes:**

1. Cliquez sur **"Proposer un nouveau sujet"**
2. Remplissez le formulaire détaillé:

**Informations générales:**
- **Titre (obligatoire):** Un titre clair et descriptif
- **Description (obligatoire):** Description détaillée du projet
- **Objectifs:** Les buts à atteindre
- **Prérequis:** Connaissances et compétences requises

**Classification:**
- **Niveau (obligatoire):** L3, M2 ou Doctorat
- **Domaine (obligatoire):** Informatique, Réseaux, IA, Web, etc.
- **Type (obligatoire):** Recherche, Développement ou Mixte
- **Mots-clés:** Séparés par des virgules (ex: Python, Django, IA)

**Encadrement:**
- **Co-encadreur (optionnel):** Choisissez un collègue
- **Nombre maximum d'étudiants:** 1 à 3 (défaut: 1)

**Disponibilité:**
- **Statut (obligatoire):** 
  - **Brouillon:** Non visible par les étudiants
  - **Publié:** Visible dans le catalogue
  - **Attribué:** Déjà affecté
  - **Archivé:** Ancien sujet
- **Disponible à partir de:** Date de début (optionnel)
- **Disponible jusqu'au:** Date limite (optionnel)

3. Cliquez sur **"Créer le sujet"**

**💡 Conseils:**

- Soyez précis et détaillé dans la description
- Listez clairement les prérequis techniques
- Indiquez les technologies/outils à utiliser
- Mentionnez si le sujet peut être étendu pour plusieurs étudiants
- Utilisez le statut "Brouillon" pour préparer le sujet avant publication

### 📝 Gérer mes sujets

1. Allez dans **"Mes sujets"**
2. Vous voyez tous vos sujets avec:
   - Titre et niveau
   - Statut actuel
   - Nombre de candidatures reçues
   - Nombre d'étudiants affectés

**Actions possibles:**

- **Voir les détails:** Cliquez sur un sujet
- **Modifier:** Cliquez sur l'icône crayon
- **Supprimer:** Cliquez sur l'icône poubelle (si aucune candidature)
- **Voir les candidatures:** Cliquez sur "Candidatures"

### 📬 Évaluer les candidatures

**Accéder aux candidatures:**

1. **Option 1:** Depuis "Mes sujets" → Cliquez sur un sujet → "Voir les candidatures"
2. **Option 2:** Depuis le tableau de bord → "Candidatures en attente"

**Pour chaque candidature, vous voyez:**

- Nom de l'étudiant
- Niveau et filière
- Priorité donnée au sujet (1-5)
- Lettre de motivation
- CV (si fourni)
- Date de candidature

**Évaluer une candidature:**

1. Cliquez sur **"Évaluer"**
2. Choisissez un statut:
   - **Acceptée:** Vous acceptez d'encadrer cet étudiant
   - **Rejetée:** Vous refusez cette candidature
3. Ajoutez des notes (optionnel mais recommandé):
   - Feedback pour l'étudiant
   - Raisons de votre décision
   - Conseils ou encouragements
4. Cliquez sur **"Enregistrer l'évaluation"**

**💡 Bonnes pratiques:**

- Évaluez rapidement (dans les 48-72h)
- Lisez attentivement les lettres de motivation
- Comparez les candidatures avant de décider
- Donnez du feedback constructif
- Si vous rejetez, expliquez pourquoi (aide l'étudiant)

### 👨‍🎓 Suivre mes étudiants

*Fonctionnalité disponible après affectation - En développement*

### 📞 Communiquer avec les étudiants

*Fonctionnalité en développement*

---

## POUR LES ADMINISTRATEURS

### ⚙️ Vue d'ensemble

En tant qu'administrateur, vous avez accès à:
- Toutes les fonctionnalités de gestion
- L'interface d'administration Django
- Les statistiques globales
- La gestion des utilisateurs
- La configuration du système

### 🎛️ Interface d'administration

**Accès:**

1. Connectez-vous avec votre compte administrateur
2. Allez sur: `http://127.0.0.1:8000/admin/`
3. Vous accédez au panneau d'administration Django

**Sections disponibles:**

**👥 Gestion des utilisateurs:**
- Voir tous les utilisateurs
- Créer/modifier/supprimer des comptes
- Gérer les rôles et permissions
- Réinitialiser les mots de passe

**📚 Gestion des sujets:**
- Voir tous les sujets (tous encadreurs)
- Modifier les statuts
- Supprimer des sujets
- Créer des affectations manuelles

**📋 Gestion des candidatures:**
- Voir toutes les candidatures
- Résoudre les conflits
- Forcer des acceptations/rejets

**📊 Statistiques:**
- Nombre total d'utilisateurs par rôle
- Sujets proposés/publiés/affectés
- Taux de candidatures
- Sujets les plus populaires

### 🔧 Configuration du système

*À documenter selon les besoins*

---

## POUR LES MEMBRES DU JURY

### 👨‍⚖️ Vue d'ensemble

*Fonctionnalité en développement*

En tant que membre du jury, vous pourrez:
- Consulter les projets à évaluer
- Accéder aux rapports et soutenances
- Noter les présentations
- Rédiger des avis

---

## 📋 Fonctionnalités détaillées

### 🔔 Système de notifications

*En développement*

Le système vous notifiera pour:
- Nouvelles candidatures (encadreurs)
- Réponses aux candidatures (étudiants)
- Modifications de statut
- Dates de soutenance
- Messages reçus

### 💬 Messagerie intégrée

*En développement*

Fonctionnalités prévues:
- Messages directs étudiant ↔ encadreur
- Pièces jointes
- Historique des conversations
- Notifications en temps réel

### 📅 Gestion des jalons et livrables

*En développement*

Permet de:
- Définir des jalons de projet
- Suivre l'avancement
- Soumettre des livrables
- Valider les étapes

### 🎤 Planification des soutenances

*En développement*

Le système permettra:
- Planification automatisée
- Gestion des salles et créneaux
- Composition des jurys
- Génération des calendriers

### 📁 Archivage et rapports

*En développement*

Fonctionnalités:
- Archivage automatique des projets terminés
- Génération de rapports statistiques
- Export des données
- Recherche dans les archives

---

## ❓ FAQ - Foire Aux Questions

### Questions générales

**Q: Qui peut s'inscrire sur la plateforme?**  
R: Tous les étudiants de L3, M2 et Doctorat de l'ENSPD, ainsi que les encadreurs, administrateurs et membres du jury.

**Q: Dois-je créer un compte pour consulter les sujets?**  
R: Oui, vous devez être connecté pour accéder au catalogue des sujets et aux autres fonctionnalités.

**Q: Puis-je modifier mes informations après inscription?**  
R: Oui, via votre page de profil, vous pouvez modifier toutes vos informations personnelles.

### Pour les étudiants

**Q: Combien de candidatures puis-je soumettre?**  
R: Il n'y a pas de limite stricte, mais nous recommandons 3-5 candidatures maximum pour rester gérable.

**Q: Puis-je candidater à des sujets de niveaux différents?**  
R: Non, vous ne voyez que les sujets correspondant à votre niveau d'études.

**Q: Que se passe-t-il si plusieurs de mes candidatures sont acceptées?**  
R: Vous devrez choisir un seul sujet. Les autres seront automatiquement retirées.

**Q: Puis-je retirer une candidature après l'avoir soumise?**  
R: Oui, tant que le statut est "En attente". Une fois évaluée, vous ne pouvez plus la retirer.

**Q: Mon CV est-il obligatoire?**  
R: Non, le CV est optionnel, mais fortement recommandé pour augmenter vos chances.

**Q: Comment savoir si ma candidature a été évaluée?**  
R: Vous recevrez une notification et le statut changera dans "Mes candidatures".

**Q: Que signifie la priorité?**  
R: C'est votre classement personnel des sujets. 1 = sujet préféré, 5 = option de secours.

### Pour les encadreurs

**Q: Combien de sujets puis-je proposer?**  
R: Autant que vous souhaitez, mais assurez-vous de pouvoir les encadrer.

**Q: Puis-je modifier un sujet après réception de candidatures?**  
R: Oui, mais les modifications majeures doivent être évitées si des étudiants ont déjà candidaté.

**Q: Puis-je supprimer un sujet avec des candidatures?**  
R: Non, vous devez d'abord traiter toutes les candidatures.

**Q: Comment choisir entre plusieurs candidats?**  
R: Évaluez les lettres de motivation, CVs, et vérifiez que l'étudiant a les prérequis.

**Q: Que se passe-t-il si j'accepte plusieurs étudiants?**  
R: C'est possible si votre sujet accepte plusieurs étudiants (max 3). Sinon, n'acceptez qu'un seul étudiant.

**Q: Puis-je co-encadrer avec un collègue?**  
R: Oui, vous pouvez définir un co-encadreur lors de la création du sujet.

### Technique

**Q: Quels navigateurs sont supportés?**  
R: Chrome, Firefox, Edge, Safari (versions récentes).

**Q: Puis-je accéder depuis un mobile?**  
R: Oui, le site est responsive et fonctionne sur mobile, mais l'expérience est optimale sur ordinateur.

**Q: Quelle est la taille maximale pour les fichiers?**  
R: CVs et documents: 10 MB maximum.

**Q: Quels formats de fichiers sont acceptés?**  
R: PDF, DOC, DOCX pour les CVs et documents texte.

---

## 🆘 Support technique

### En cas de problème

**1. Vérifiez d'abord:**
- Votre connexion internet
- Que vous utilisez un navigateur à jour
- Que vous êtes bien connecté
- Les messages d'erreur affichés

**2. Solutions courantes:**

**Problème:** Je ne peux pas me connecter  
**Solution:** Vérifiez votre nom d'utilisateur et mot de passe. Respectez les majuscules/minuscules.

**Problème:** Je ne vois pas de sujets  
**Solution:** Vérifiez que votre niveau est bien défini dans votre profil.

**Problème:** Le formulaire ne se soumet pas  
**Solution:** Vérifiez que tous les champs obligatoires sont remplis et valides.

**Problème:** Mon fichier ne s'upload pas  
**Solution:** Vérifiez la taille (max 10 MB) et le format (PDF, DOC, DOCX).

### Contact

**Support technique:**
- Email: support-pfe@enspd.cm
- Bureau: Service informatique, Bâtiment A

**Heures d'assistance:**
- Lundi - Vendredi: 8h00 - 17h00
- Samedi: 9h00 - 13h00

---

## 📌 Annexes

### Glossaire

- **PFE:** Projet de Fin d'Études
- **Candidature:** Demande d'un étudiant pour travailler sur un sujet
- **Affectation:** Attribution officielle d'un sujet à un étudiant
- **Encadreur:** Enseignant qui supervise un projet
- **Co-encadreur:** Second enseignant assistant l'encadrement
- **Jalon:** Étape importante du projet
- **Livrable:** Document ou réalisation à remettre
- **Soutenance:** Présentation finale du projet devant un jury

### Raccourcis clavier

*À venir*

### Captures d'écran

*À ajouter selon les besoins*

---

## 📝 Notes de version

### Version 1.0 (3 Décembre 2025)

**Fonctionnalités disponibles:**
- ✅ Authentification et gestion des profils
- ✅ Proposition de sujets par les encadreurs
- ✅ Catalogue de sujets avec filtres
- ✅ Système de candidature
- ✅ Évaluation des candidatures
- ✅ Interface d'administration

**Fonctionnalités en développement:**
- 🚧 Suivi collaboratif des projets
- 🚧 Messagerie intégrée
- 🚧 Planification des soutenances
- 🚧 Archivage et statistiques

---

**© 2025 ENSPD - École Nationale Supérieure Polytechnique de Douala**  
*Ce document est destiné à l'usage interne de l'ENSPD*
