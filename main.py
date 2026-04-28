from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from pydantic import BaseModel
from typing import Optional
import json

DATABASE_URL = "sqlite:///./snay3i.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Worker(Base):
    __tablename__ = "workers"
    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    service   = Column(String, nullable=False, index=True)
    city      = Column(String, nullable=False)
    rating    = Column(Float, default=5.0)
    reviews   = Column(Integer, default=0)
    verified  = Column(Boolean, default=False)
    bio       = Column(String, default="")
    tags      = Column(String, default="[]")
    phone     = Column(String, default="")
    whatsapp  = Column(String, default="")
    address   = Column(String, default="")
    years_exp = Column(Integer, default=1)

Base.metadata.create_all(bind=engine)

class WorkerOut(BaseModel):
    id: int; name: str; service: str; city: str
    rating: float; reviews: int; verified: bool
    bio: str; tags: list[str]; phone: str; whatsapp: str
    address: str; years_exp: int
    model_config = {"from_attributes": True}

class WorkerCreate(BaseModel):
    name: str; service: str; city: str
    rating: float = 5.0; reviews: int = 0; verified: bool = False
    bio: str = ""; tags: list[str] = []
    phone: str = ""; whatsapp: str = ""; address: str = ""; years_exp: int = 1

app = FastAPI(title="Snay3i.ma API", version="1.0.0")
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

SEED = [
  # ══ CASABLANCA — Plombiers ══════════════════════════════════════════════
  {"name":"Saber Omar","service":"plumber","city":"Casablanca","rating":4.8,"reviews":87,"verified":True,"bio":"Plombier professionnel Casablanca. Fuites, debouchage, chauffe-eau, sanitaires. Intervention rapide.","tags":["Fuites","Debouchage","Chauffe-eau"],"phone":"0664-676006","whatsapp":"212664676006","address":"Casablanca","years_exp":12},
  {"name":"Ets Said Rojdi","service":"plumber","city":"Casablanca","rating":5.0,"reviews":3,"verified":True,"bio":"Plombier certifie Casablanca. Reparations, installations sanitaires, mise aux normes.","tags":["Certifie","Sanitaires","Normes"],"phone":"0522-810699","whatsapp":"212522810699","address":"Casablanca","years_exp":15},
  {"name":"Plombier Elfath","service":"plumber","city":"Casablanca","rating":4.3,"reviews":3,"verified":False,"bio":"Plombier Casablanca. Debouchage, fuites, reparation robinetterie, chauffe-eau.","tags":["Robinetterie","Debouchage","Urgent"],"phone":"0661-802637","whatsapp":"212661802637","address":"Casablanca","years_exp":8},
  {"name":"Nammous Abderrahim","service":"plumber","city":"Casablanca","rating":4.7,"reviews":42,"verified":True,"bio":"Plombier electricien Casablanca. Double competence plomberie et electricite. Devis gratuit.","tags":["Plomberie","Electricite","Double comp."],"phone":"0660-625747","whatsapp":"212660625747","address":"Casablanca","years_exp":11},
  {"name":"Larbi Yous","service":"plumber","city":"Casablanca","rating":4.6,"reviews":31,"verified":False,"bio":"Plombier Casablanca. Fuites eau, debouchage canalisations, installation sanitaires.","tags":["Fuites","Canalisations","Rapide"],"phone":"0660-952040","whatsapp":"212660952040","address":"Casablanca","years_exp":9},
  {"name":"Plombier Napoli","service":"plumber","city":"Casablanca","rating":4.5,"reviews":18,"verified":False,"bio":"Plombier Casablanca. Toutes interventions plomberie. Disponible rapidement.","tags":["Toutes zones","Disponible","Economique"],"phone":"0661-525095","whatsapp":"212661525095","address":"Casablanca","years_exp":7},
  {"name":"Mes Depanneurs Maroc","service":"plumber","city":"Casablanca","rating":4.9,"reviews":203,"verified":True,"bio":"Depannage urgence 24h/7j. Plombier, serrurier, electricien. Intervention en 20 min sur Casablanca.","tags":["Urgence 24h","20 min","Multi-services"],"phone":"0600-888190","whatsapp":"212600888190","address":"Grand Casablanca","years_exp":10},
  {"name":"Hadj Omar","service":"plumber","city":"Casablanca","rating":4.6,"reviews":29,"verified":False,"bio":"Plombier experimente Casablanca. Fuites, sanitaires, debouchage, chauffe-eau solaire.","tags":["Solaire","Fuites","Experimente"],"phone":"0667-143399","whatsapp":"212667143399","address":"Casablanca","years_exp":18},
  {"name":"Asswa Abdelmajid","service":"plumber","city":"Casablanca","rating":4.7,"reviews":51,"verified":True,"bio":"Plombier Casablanca. Fuites, debouchage, installation salle de bain complete.","tags":["Salle de bain","Installation","Complet"],"phone":"0663-369721","whatsapp":"212663369721","address":"Casablanca","years_exp":13},

  # ══ CASABLANCA — Electriciens ═══════════════════════════════════════════
  {"name":"Radi Abderrahim","service":"electrician","city":"Casablanca","rating":4.8,"reviews":64,"verified":True,"bio":"Plombier et electricien Casablanca. Double competence. Depannage urgence toutes zones.","tags":["Double comp.","Urgence","Toutes zones"],"phone":"0660-275730","whatsapp":"212660275730","address":"Casablanca","years_exp":14},
  {"name":"Electricien Belvedere Casa","service":"electrician","city":"Casablanca","rating":4.8,"reviews":84,"verified":True,"bio":"Electricien Belvedere et Bourgogne. Depannage urgent, tableau electrique, interphone, camera.","tags":["Belvedere","Tableau","Camera"],"phone":"0659-787098","whatsapp":"212659787098","address":"Quartier Belvedere, Casablanca","years_exp":7},
  {"name":"Bricodar Electricien","service":"electrician","city":"Casablanca","rating":4.8,"reviews":203,"verified":True,"bio":"Electricien urgence Ain Sebaa. Diagnostic, court-circuit, LED, prises, tableaux electriques.","tags":["Ain Sebaa","Diagnostic","LED"],"phone":"0606-444400","whatsapp":"212606444400","address":"80 Bvd Moulay Slimane, Ain Sebaa, Casablanca","years_exp":15},

  # ══ CASABLANCA — Peintres ════════════════════════════════════════════════
  {"name":"Peintre Al Farabi Casa","service":"painter","city":"Casablanca","rating":4.8,"reviews":91,"verified":True,"bio":"Peintre professionnel Casablanca. Interieur, exterieur, facades, enduits decoratifs. Devis gratuit.","tags":["Interieur","Facades","Enduits"],"phone":"0665-717495","whatsapp":"212665717495","address":"6 Rue Al Farabi, Casablanca","years_exp":11},
  {"name":"Peintre Ibn Tachfine","service":"painter","city":"Casablanca","rating":4.7,"reviews":74,"verified":False,"bio":"Peintre decorateur tadelakt et beton cire. Stuc venezien. Devis sur place gratuit.","tags":["Tadelakt","Beton cire","Stuc"],"phone":"0661-410611","whatsapp":"212661410611","address":"Angle BD Ibn Tachfine et Rue Zineb Ishak, Casablanca","years_exp":9},
  {"name":"Peintre Travaux Maroc","service":"painter","city":"Casablanca","rating":4.9,"reviews":183,"verified":True,"bio":"Artisan peintre 17 ans experience. Peinture interieure, facades, tadelakt, renovation. Devis WhatsApp.","tags":["17 ans exp","Tadelakt","Renovation"],"phone":"0665-681061","whatsapp":"212665681061","address":"Casablanca, Rabat, Marrakech","years_exp":17},
  {"name":"Peintre Grand Casablanca","service":"painter","city":"Casablanca","rating":4.6,"reviews":58,"verified":False,"bio":"Peintre en batiment. Partout sur Casablanca et environs. Tarifs competitifs.","tags":["Grand Casa","Competitif","Facades"],"phone":"0660-804924","whatsapp":"212660804924","address":"Partout sur Casablanca et environs","years_exp":8},

  # ══ CASABLANCA — Macons ══════════════════════════════════════════════════
  {"name":"Noureddine Hajji","service":"builder","city":"Casablanca","rating":4.8,"reviews":203,"verified":True,"bio":"Entrepreneur en batiment Casablanca. Gros oeuvre, renovation complete, extensions, permis.","tags":["Gros oeuvre","Extension","Permis"],"phone":"0666-789012","whatsapp":"212666789012","address":"Bd Panoramique, Beausejour, Casablanca","years_exp":20},
  {"name":"Jami Ahmed Macon","service":"builder","city":"Casablanca","rating":5.0,"reviews":2,"verified":True,"bio":"Macon sanitariste Casablanca. Construction, renovation, carrelage, zellige, plomberie.","tags":["Carrelage","Zellige","Construction"],"phone":"0522-570267","whatsapp":"212522570267","address":"Casablanca","years_exp":16},

  # ══ CASABLANCA — Menuisiers ══════════════════════════════════════════════
  {"name":"Menuisier Oulfa","service":"carpenter","city":"Casablanca","rating":4.7,"reviews":74,"verified":False,"bio":"Menuisier bois et aluminium. Cuisine, placards, fenetres sur mesure. Hay Oulfa et environs.","tags":["Cuisine","Placards","Aluminium"],"phone":"0665-294929","whatsapp":"212665294929","address":"N67 Rue 162, Hay El Oulfa, Casablanca","years_exp":9},
  {"name":"Menuisier Maarif","service":"carpenter","city":"Casablanca","rating":4.8,"reviews":96,"verified":True,"bio":"Menuisier artisan Maarif. Portes, fenetres, dressings, cuisine sur mesure haut de gamme.","tags":["Sur mesure","Dressing","Haut de gamme"],"phone":"0614-662139","whatsapp":"212614662139","address":"Boulevard Brahim Roudani, Maarif, Casablanca","years_exp":16},

  # ══ CASABLANCA — Bricoleurs ══════════════════════════════════════════════
  {"name":"Bricoleur Casablanca Express","service":"handyman","city":"Casablanca","rating":4.6,"reviews":47,"verified":False,"bio":"Bricoleur toutes mains Casablanca. Montage meubles, petites reparations, jardinage, demenagement.","tags":["Montage","Jardinage","Rapide"],"phone":"0661-619231","whatsapp":"212661619231","address":"Casablanca, toutes zones","years_exp":5},

  # ══ RABAT ════════════════════════════════════════════════════════════════
  {"name":"Ets Hamid Ramadi","service":"plumber","city":"Rabat","rating":4.7,"reviews":38,"verified":True,"bio":"Plombier artisan Rabat. Reparations, installations, depannage. Devis gratuit.","tags":["Artisan","Devis gratuit","Rapide"],"phone":"0537-776836","whatsapp":"212537776836","address":"Rabat","years_exp":14},
  {"name":"Ets Amsri Sanitaire","service":"plumber","city":"Rabat","rating":4.6,"reviews":22,"verified":True,"bio":"Sanitaire et plomberie Rabat. Vente et installation. Chauffe-eau, robinetterie, sanitaires.","tags":["Sanitaires","Vente","Installation"],"phone":"0537-738540","whatsapp":"212537738540","address":"Rabat","years_exp":18},
  {"name":"Macon Hay Riad","service":"builder","city":"Rabat","rating":4.8,"reviews":189,"verified":True,"bio":"Macon entrepreneur Hay Riad. Gros oeuvre, renovation, extensions, finitions haut de gamme.","tags":["Hay Riad","Gros oeuvre","Finitions"],"phone":"0696-390302","whatsapp":"212696390302","address":"Hay Riad, Avenue Mahdi Ben Barka, Rabat","years_exp":18},
  {"name":"Youssef Alami Electricien","service":"electrician","city":"Rabat","rating":4.9,"reviews":146,"verified":True,"bio":"Electricien certifie Agdal Rabat. Bornes recharge VE, domotique, panneaux solaires.","tags":["VE","Domotique","Solaire"],"phone":"0672-345678","whatsapp":"212672345678","address":"Rue Moulay Ali Cherif, Agdal, Rabat","years_exp":10},
  {"name":"Peintre Facades Rabat","service":"painter","city":"Rabat","rating":4.8,"reviews":71,"verified":True,"bio":"Peintre en batiment Rabat Souissi. Ravalement facades, isolation thermique, peintures eco.","tags":["Facades","ITE","Ecologique"],"phone":"0656-091882","whatsapp":"212656091882","address":"Av. Moulay Ali Cherif, Temara-Rabat","years_exp":9},
  {"name":"Menuisier Agdal Rabat","service":"carpenter","city":"Rabat","rating":4.7,"reviews":58,"verified":True,"bio":"Menuisier Agdal Rabat. Bois, aluminium, PVC. Cuisine, dressing, portes et fenetres.","tags":["Agdal","PVC","Cuisine"],"phone":"0673-456789","whatsapp":"212673456789","address":"Quartier Agdal, Rabat","years_exp":12},

  # ══ MARRAKECH ════════════════════════════════════════════════════════════
  {"name":"Fouad Mimouni Plombier","service":"plumber","city":"Marrakech","rating":4.8,"reviews":112,"verified":True,"bio":"Plombier urgentiste Gueliz et Medina. Fuites, debouchage, installation sanitaires, hammam.","tags":["Hammam","Urgences","Gueliz"],"phone":"0660-558377","whatsapp":"212660558377","address":"Rue Yougoslavie, Gueliz, Marrakech","years_exp":12},
  {"name":"Karim Tazi Macon","service":"builder","city":"Marrakech","rating":4.9,"reviews":258,"verified":True,"bio":"Maitre macon zellige et tadelakt. Stucs marocains authentiques. Renovation riads et villas Marrakech.","tags":["Zellige","Tadelakt","Riad"],"phone":"0649-493514","whatsapp":"212649493514","address":"Quartier Daoudiate, Marrakech","years_exp":22},
  {"name":"Macon Syba Marrakech","service":"builder","city":"Marrakech","rating":4.7,"reviews":88,"verified":True,"bio":"Macon renovation et construction Marrakech. Gros oeuvre, carrelage zellige, enduits.","tags":["Gros oeuvre","Zellige","Enduits"],"phone":"0679-504360","whatsapp":"212679504360","address":"02 DB Sahraoua, Syba, Marrakech","years_exp":14},
  {"name":"Peintre Mhamid Marrakech","service":"painter","city":"Marrakech","rating":4.7,"reviews":65,"verified":False,"bio":"Peintre decoration Marrakech. Interieur, exterieur, motifs marocains, ocre de Marrakech.","tags":["Ocre","Motifs","Exterieur"],"phone":"0660-558377","whatsapp":"212660558377","address":"72 Lot Zaitouna, Rue Al Inab, Mhamid, Marrakech","years_exp":8},
  {"name":"Bilal Mansour Menuisier","service":"carpenter","city":"Marrakech","rating":4.8,"reviews":67,"verified":True,"bio":"Menuisier artisan Marrakech. Portes en cedre, moucharabiehs, meubles berberes sur mesure.","tags":["Cedre","Moucharabieh","Berbere"],"phone":"0670-123456","whatsapp":"212670123456","address":"Quartier Targa, Marrakech","years_exp":13},
  {"name":"Soufiane Azizi Electricien","service":"electrician","city":"Marrakech","rating":4.6,"reviews":54,"verified":True,"bio":"Electricien riads, hotels et villas Marrakech. Eclairage decoratif, domotique, solaire.","tags":["Riads","Hotels","Eclairage"],"phone":"0671-234567","whatsapp":"212671234567","address":"Av. Menara, Marrakech","years_exp":7},
  {"name":"Bricoleur Marrakech","service":"handyman","city":"Marrakech","rating":4.5,"reviews":33,"verified":False,"bio":"Bricoleur polyvalent Marrakech. Petites reparations, montage, jardinage riads et villas.","tags":["Riads","Jardinage","Petits travaux"],"phone":"0668-901234","whatsapp":"212668901234","address":"Gueliz, Marrakech","years_exp":6},

  # ══ FES ══════════════════════════════════════════════════════════════════
  {"name":"Mustapha Berrade Macon","service":"builder","city":"Fes","rating":4.8,"reviews":144,"verified":True,"bio":"Architecte macon Fes. Restauration patrimoine marocain, zellige, gebs, bois sculpte. Expert medinas.","tags":["Patrimoine","Gebs","Zellige"],"phone":"0678-901234","whatsapp":"212678901234","address":"Quartier Narjiss, Fes-Jdid, Fes","years_exp":25},
  {"name":"Hicham Filali Electricien","service":"electrician","city":"Fes","rating":4.7,"reviews":63,"verified":True,"bio":"Electricien rehabilitation medina Fes. Mise aux normes, alarmes, surveillance.","tags":["Medina","Normes","Alarme"],"phone":"0677-890123","whatsapp":"212677890123","address":"Rue Serrajine, Quartier Saiss, Fes","years_exp":9},
  {"name":"Menuisier Zouagha Fes","service":"carpenter","city":"Fes","rating":4.7,"reviews":58,"verified":True,"bio":"Menuisier traditionnel Fes. Bois sculpte, zellige bois, moucharabiehs, portes monumentales medina.","tags":["Bois sculpte","Traditionnel","Moucharabieh"],"phone":"0618-462335","whatsapp":"212618462335","address":"Quartier Zouagha, Fes","years_exp":18},
  {"name":"Plombier Bab Guissa Fes","service":"plumber","city":"Fes","rating":4.6,"reviews":49,"verified":False,"bio":"Plombier medina et ville nouvelle Fes. Renovation sanitaires, debouchage, hammam traditionnel.","tags":["Medina","Hammam","Debouchage"],"phone":"0676-789012","whatsapp":"212676789012","address":"Bab Guissa, Fes el-Bali, Fes","years_exp":8},
  {"name":"Peintre Fes Ville Nouvelle","service":"painter","city":"Fes","rating":4.6,"reviews":41,"verified":False,"bio":"Peintre Fes. Interieur, exterieur, decoration marocaine, tadelakt, beton cire.","tags":["Decoration","Tadelakt","Interieur"],"phone":"0666-543210","whatsapp":"212666543210","address":"Ville Nouvelle, Fes","years_exp":7},

  # ══ TANGER ═══════════════════════════════════════════════════════════════
  {"name":"Mehdi Cherkaoui Menuisier","service":"carpenter","city":"Tanger","rating":4.8,"reviews":107,"verified":True,"bio":"Menuisier aluminium PVC et bois Tanger. Menuiseries exterieures, verandas, store banne.","tags":["Aluminium","Veranda","PVC"],"phone":"0679-012345","whatsapp":"212679012345","address":"Av. Mohammed VI, Malabata, Tanger","years_exp":15},
  {"name":"Khalid Benomar Electricien","service":"electrician","city":"Tanger","rating":4.7,"reviews":58,"verified":True,"bio":"Electricien industriel et residentiel Tanger. Groupe electrogene, LED, installation complete.","tags":["Industriel","LED","Groupe elec"],"phone":"0680-123456","whatsapp":"212680123456","address":"Zone Industrielle Boukhalef, Tanger","years_exp":11},
  {"name":"Macon Route Rabat Tanger","service":"builder","city":"Tanger","rating":4.7,"reviews":82,"verified":True,"bio":"Macon construction et renovation Tanger. Gros oeuvre, villas, appartements, finitions.","tags":["Gros oeuvre","Villas","Finitions"],"phone":"0631-068885","whatsapp":"212631068885","address":"Zemouri 1, Route de Rabat, Tanger","years_exp":13},
  {"name":"Peintre Place 9 Avril Tanger","service":"painter","city":"Tanger","rating":4.6,"reviews":44,"verified":False,"bio":"Peintre interieur et exterieur Tanger. Ravalement, renovation, devis gratuit rapide.","tags":["Interieur","Ravalement","Devis gratuit"],"phone":"0662-886704","whatsapp":"212662886704","address":"Place du 9 Avril, Tanger","years_exp":7},
  {"name":"Hamza Riffi Plombier","service":"plumber","city":"Tanger","rating":4.6,"reviews":49,"verified":False,"bio":"Plombier sanitariste Tanger. Salle de bain cle en main, jacuzzi, hammam, fuites urgences.","tags":["Jacuzzi","Hammam","Cle en main"],"phone":"0681-234567","whatsapp":"212681234567","address":"Residence Ibn Batouta, Tanger","years_exp":7},
  {"name":"Macon Tanger 2","service":"builder","city":"Tanger","rating":4.6,"reviews":37,"verified":False,"bio":"Macon Tanger. Construction neuve, renovation, carrelage, enduits. Devis gratuit sur place.","tags":["Construction","Carrelage","Devis"],"phone":"0652-300088","whatsapp":"212652300088","address":"Tanger","years_exp":10},

  # ══ AGADIR ═══════════════════════════════════════════════════════════════
  {"name":"Plombier Agadir Service","service":"plumber","city":"Agadir","rating":4.7,"reviews":63,"verified":True,"bio":"Plombier Agadir et region Souss. Reparation, installation, chauffe-eau solaire. Disponible 7j/7.","tags":["Souss","Solaire","7j/7"],"phone":"0661-737666","whatsapp":"212661737666","address":"Agadir","years_exp":10},
  {"name":"Said Aouam Macon","service":"builder","city":"Agadir","rating":4.8,"reviews":176,"verified":True,"bio":"Entrepreneur batiment Agadir. Villas bord de mer, piscines, constructions parasismiques normes.","tags":["Villa","Piscine","Parasismique"],"phone":"0683-456789","whatsapp":"212683456789","address":"Bd du 20 Aout, Agadir","years_exp":19},
  {"name":"Amine Bensouda Electricien","service":"electrician","city":"Agadir","rating":4.6,"reviews":67,"verified":False,"bio":"Electricien residentiel Agadir. Climatisation, panneaux solaires, economies d energie.","tags":["Clim","Solaire","Economies"],"phone":"0682-345678","whatsapp":"212682345678","address":"Quartier Tilila, Agadir","years_exp":6},
  {"name":"Driss Ait Baha Bricoleur","service":"handyman","city":"Agadir","rating":4.7,"reviews":55,"verified":False,"bio":"Bricoleur paysagiste Agadir. Entretien villa, jardin, piscine, petits travaux et reparations.","tags":["Piscine","Jardin","Entretien"],"phone":"0684-567890","whatsapp":"212684567890","address":"Hay Charaf, Agadir","years_exp":5},
  {"name":"Peintre Agadir Founty","service":"painter","city":"Agadir","rating":4.7,"reviews":62,"verified":True,"bio":"Peintre Agadir et region Souss. Interieur, facade, tadelakt, enduits decoratifs. Devis gratuit.","tags":["Souss","Facade","Tadelakt"],"phone":"0685-678901","whatsapp":"212685678901","address":"Quartier Founty, Agadir","years_exp":10},
  {"name":"Menuisier Agadir","service":"carpenter","city":"Agadir","rating":4.6,"reviews":39,"verified":False,"bio":"Menuisier Agadir. Aluminium, PVC, bois. Cuisine, placards, fenetres, portes sur mesure.","tags":["Aluminium","PVC","Sur mesure"],"phone":"0686-789012","whatsapp":"212686789012","address":"Agadir","years_exp":8},
]

def seed_db()

import threading, urllib.request, time

def keep_alive():
    while True:
        try:
            urllib.request.urlopen('https://snay3i-backend.onrender.com/')
        except: pass
        time.sleep(840)

threading.Thread(target=keep_alive, daemon=True).start()


import threading, urllib.request, time

def keep_alive():
    while True:
        try:
            urllib.request.urlopen('https://snay3i-backend.onrender.com/')
        except: pass
        time.sleep(840)

threading.Thread(target=keep_alive, daemon=True).start()

import threading
import urllib.request
import time

def keep_alive():
    while True:
        try:
            urllib.request.urlopen('https://snay3i-backend.onrender.com/')
            print("Keep-alive ping sent!")
        except:
            pass
        time.sleep(840)  # ping every 14 minutes

thread = threading.Thread(target=keep_alive, daemon=True)
thread.start()
:
    db = SessionLocal()
    try:
        if db.query(Worker).count() == 0:
            for w in SEED:
                tags = json.dumps(w.pop("tags"))
                worker = Worker(**w, tags=tags)
                db.add(worker)
            db.commit()
            print(f"Snay3i.ma DB seeded with {len(SEED)} traders!")
    finally:
        db.close()

seed_db()

import threading, urllib.request, time

def keep_alive():
    while True:
        try:
            urllib.request.urlopen('https://snay3i-backend.onrender.com/')
        except: pass
        time.sleep(840)

threading.Thread(target=keep_alive, daemon=True).start()


import threading, urllib.request, time

def keep_alive():
    while True:
        try:
            urllib.request.urlopen('https://snay3i-backend.onrender.com/')
        except: pass
        time.sleep(840)

threading.Thread(target=keep_alive, daemon=True).start()

import threading
import urllib.request
import time

def keep_alive():
    while True:
        try:
            urllib.request.urlopen('https://snay3i-backend.onrender.com/')
            print("Keep-alive ping sent!")
        except:
            pass
        time.sleep(840)  # ping every 14 minutes

thread = threading.Thread(target=keep_alive, daemon=True)
thread.start()


def serialize(w):
    return WorkerOut(id=w.id, name=w.name, service=w.service, city=w.city,
        rating=w.rating, reviews=w.reviews, verified=w.verified,
        bio=w.bio, tags=json.loads(w.tags) if w.tags else [],
        phone=w.phone or "", whatsapp=w.whatsapp or "",
        address=w.address or "", years_exp=w.years_exp or 1)

@app.get("/")
def root(): return {"message": "Snay3i.ma API — صنايعي.ما"}

@app.get("/workers", response_model=list[WorkerOut])
def get_all(city: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Worker)
    if city: q = q.filter(Worker.city.ilike(city))
    return [serialize(w) for w in q.all()]

@app.get("/workers/{service}", response_model=list[WorkerOut])
def get_by_service(service: str, city: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Worker).filter(Worker.service.ilike(service))
    if city: q = q.filter(Worker.city.ilike(city))
    workers = q.all()
    if not workers: raise HTTPException(404, f"No traders for: {service}")
    return [serialize(w) for w in workers]

@app.post("/workers", response_model=WorkerOut, status_code=201)
def create_worker(data: WorkerCreate, db: Session = Depends(get_db)):
    d = data.model_dump(); d["tags"] = json.dumps(d["tags"])
    w = Worker(**d); db.add(w); db.commit(); db.refresh(w)
    return serialize(w)

@app.delete("/workers/{wid}", status_code=204)
def delete_worker(wid: int, db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.id == wid).first()
    if not w: raise HTTPException(404, "Not found")
    db.delete(w); db.commit()


# ══ CHAT SYSTEM ══════════════════════════════════════════════════════════════
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"
    id         = Column(Integer, primary_key=True, index=True)
    worker_id  = Column(Integer, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    sender     = Column(String, nullable=False)  # "client" or "worker"
    text       = Column(String, nullable=False)
    timestamp  = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class MessageOut(BaseModel):
    id: int; worker_id: int; session_id: str
    sender: str; text: str; timestamp: str
    model_config = {"from_attributes": True}

class MessageIn(BaseModel):
    worker_id: int; session_id: str; sender: str; text: str

@app.get("/chat/{worker_id}/{session_id}", response_model=list[MessageOut])
def get_messages(worker_id: int, session_id: str, db: Session = Depends(get_db)):
    return db.query(Message).filter(
        Message.worker_id == worker_id,
        Message.session_id == session_id
    ).order_by(Message.id).all()

@app.post("/chat", response_model=MessageOut, status_code=201)
def send_message(data: MessageIn, db: Session = Depends(get_db)):
    msg = Message(
        worker_id=data.worker_id,
        session_id=data.session_id,
        sender=data.sender,
        text=data.text,
        timestamp=datetime.now().strftime("%H:%M")
    )
    db.add(msg); db.commit(); db.refresh(msg)
    return msg
