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
  # ══ RABAT ════════════════════════════════════════════════════════
  {"name":"Plombier Agdal Rabat","service":"plumber","city":"Rabat","rating":4.8,"reviews":92,"verified":True,"bio":"Plombier Agdal et Hay Riad. Fuites, debouchage, chauffe-eau, sanitaires. Devis gratuit.","tags":["Agdal","Hay Riad","Urgent"],"phone":"0661-234501","whatsapp":"212661234501","address":"Agdal, Rabat","years_exp":12},
  {"name":"Hassan Plomberie Rabat","service":"plumber","city":"Rabat","rating":4.7,"reviews":63,"verified":True,"bio":"Plombier experimente Rabat-Sale. Installations sanitaires, fuites, debouchage canalisations.","tags":["Rabat-Sale","Canalisations","Installations"],"phone":"0662-345612","whatsapp":"212662345612","address":"Rabat","years_exp":15},
  {"name":"Depannage Plomberie Rabat","service":"plumber","city":"Rabat","rating":4.6,"reviews":44,"verified":False,"bio":"Intervention rapide plomberie Rabat. Disponible 7j/7. Fuites, robinetterie, WC.","tags":["7j/7","Rapide","WC"],"phone":"0663-456723","whatsapp":"212663456723","address":"Rabat","years_exp":8},
  {"name":"Plombier Souissi Rabat","service":"plumber","city":"Rabat","rating":4.9,"reviews":118,"verified":True,"bio":"Plombier Souissi, Aviation, Hay Nahda. Urgences 24h. Chauffe-eau solaire, salle de bain.","tags":["Souissi","Solaire","24h"],"phone":"0664-567834","whatsapp":"212664567834","address":"Souissi, Rabat","years_exp":18},
  {"name":"Electricien Agdal Rabat","service":"electrician","city":"Rabat","rating":4.8,"reviews":87,"verified":True,"bio":"Electricien certifie Agdal. Tableau electrique, prises, interphone, domotique. Devis gratuit.","tags":["Agdal","Tableau","Domotique"],"phone":"0665-678945","whatsapp":"212665678945","address":"Agdal, Rabat","years_exp":10},
  {"name":"Mohamed Electricite Rabat","service":"electrician","city":"Rabat","rating":4.7,"reviews":55,"verified":False,"bio":"Electricien Rabat ville. Depannage, installation, mise aux normes. Intervention rapide.","tags":["Mise aux normes","Depannage","Rapide"],"phone":"0666-789056","whatsapp":"212666789056","address":"Rabat","years_exp":13},
  {"name":"Electricien Hay Riad","service":"electrician","city":"Rabat","rating":4.9,"reviews":134,"verified":True,"bio":"Electricien Hay Riad et Ryad. Climatisation, panneaux solaires, domotique, alarme.","tags":["Hay Riad","Solaire","Alarme"],"phone":"0667-890167","whatsapp":"212667890167","address":"Hay Riad, Rabat","years_exp":16},
  {"name":"Macon Batiment Rabat","service":"builder","city":"Rabat","rating":4.7,"reviews":78,"verified":True,"bio":"Entrepreneur batiment Rabat. Construction, renovation, extension, carrelage, peinture.","tags":["Construction","Extension","Renovation"],"phone":"0668-901278","whatsapp":"212668901278","address":"Rabat","years_exp":20},
  {"name":"Renovation Maison Rabat","service":"builder","city":"Rabat","rating":4.6,"reviews":52,"verified":False,"bio":"Renovation complete Rabat-Sale-Kenitra. Gros oeuvre, second oeuvre, finitions. Devis gratuit.","tags":["Gros oeuvre","Finitions","Devis"],"phone":"0669-012389","whatsapp":"212669012389","address":"Rabat-Sale-Kenitra","years_exp":14},
  {"name":"Peintre Decorateur Rabat","service":"painter","city":"Rabat","rating":4.8,"reviews":96,"verified":True,"bio":"Peintre decorateur Rabat. Tadelakt, beton cire, stuc, peinture interieure exterieure.","tags":["Tadelakt","Beton cire","Stuc"],"phone":"0661-123490","whatsapp":"212661123490","address":"Rabat","years_exp":11},
  {"name":"Peintre Agdal Rabat","service":"painter","city":"Rabat","rating":4.7,"reviews":67,"verified":False,"bio":"Peintre professionnel Agdal et Hay Riad. Interieur, facades, enduits. Tarifs competitifs.","tags":["Agdal","Facades","Competitif"],"phone":"0662-234501","whatsapp":"212662234501","address":"Agdal, Rabat","years_exp":9},
  {"name":"Menuisier Aluminium Rabat","service":"carpenter","city":"Rabat","rating":4.8,"reviews":83,"verified":True,"bio":"Menuisier aluminium et PVC Rabat. Fenetres, portes, verandas, moustiquaires sur mesure.","tags":["Aluminium","PVC","Verandas"],"phone":"0663-345612","whatsapp":"212663345612","address":"Rabat","years_exp":15},
  {"name":"Menuisier Bois Rabat","service":"carpenter","city":"Rabat","rating":4.6,"reviews":49,"verified":False,"bio":"Menuisier bois Rabat. Cuisines, placards, portes, escaliers sur mesure. Artisan qualifie.","tags":["Cuisine","Placards","Sur mesure"],"phone":"0664-456723","whatsapp":"212664456723","address":"Rabat","years_exp":12},
  {"name":"Bricoleur Rabat Multi","service":"handyman","city":"Rabat","rating":4.7,"reviews":71,"verified":True,"bio":"Bricoleur polyvalent Rabat. Montage meubles, reparations, petits travaux, climatisation.","tags":["Montage","Reparations","Climatisation"],"phone":"0665-567834","whatsapp":"212665567834","address":"Rabat","years_exp":8},
  # ══ MARRAKECH ════════════════════════════════════════════════════
  {"name":"Plombier Gueliz Marrakech","service":"plumber","city":"Marrakech","rating":4.8,"reviews":103,"verified":True,"bio":"Plombier Gueliz et Hivernage. Fuites, debouchage, chauffe-eau, salle de bain complete.","tags":["Gueliz","Hivernage","Salle de bain"],"phone":"0524-123401","whatsapp":"212524123401","address":"Gueliz, Marrakech","years_exp":14},
  {"name":"Plombier Medina Marrakech","service":"plumber","city":"Marrakech","rating":4.7,"reviews":58,"verified":False,"bio":"Plombier medina et ville nouvelle. Debouchage, fuites, installation sanitaires. Rapide.","tags":["Medina","Ville nouvelle","Rapide"],"phone":"0661-234512","whatsapp":"212661234512","address":"Medina, Marrakech","years_exp":10},
  {"name":"Plombier Urgence Marrakech","service":"plumber","city":"Marrakech","rating":4.9,"reviews":156,"verified":True,"bio":"Plombier urgence 24h/7j Marrakech. Intervention 30 min. Fuites, debouchage, chauffe-eau.","tags":["24h/7j","30 min","Urgence"],"phone":"0662-345623","whatsapp":"212662345623","address":"Marrakech","years_exp":16},
  {"name":"Plombier Palmeraie Marrakech","service":"plumber","city":"Marrakech","rating":4.6,"reviews":39,"verified":True,"bio":"Plombier Palmeraie et Amelkis. Piscines, arrosage, installation sanitaires haut de gamme.","tags":["Palmeraie","Piscines","Haut de gamme"],"phone":"0663-456734","whatsapp":"212663456734","address":"Palmeraie, Marrakech","years_exp":12},
  {"name":"Electricien Marrakech Gueliz","service":"electrician","city":"Marrakech","rating":4.8,"reviews":89,"verified":True,"bio":"Electricien Gueliz et Hivernage. Tableau, prises, eclairage LED, climatisation, alarme.","tags":["Gueliz","LED","Alarme"],"phone":"0664-567845","whatsapp":"212664567845","address":"Gueliz, Marrakech","years_exp":11},
  {"name":"Electricien Urgence Marrakech","service":"electrician","city":"Marrakech","rating":4.7,"reviews":72,"verified":False,"bio":"Electricien urgence Marrakech. Court-circuit, panne totale, tableau. Intervention rapide.","tags":["Urgence","Court-circuit","Panne"],"phone":"0665-678956","whatsapp":"212665678956","address":"Marrakech","years_exp":9},
  {"name":"Electricien Solaire Marrakech","service":"electrician","city":"Marrakech","rating":4.9,"reviews":144,"verified":True,"bio":"Specialiste panneaux solaires Marrakech. Installation, maintenance, onduleurs. Economies garanties.","tags":["Solaire","Panneaux","Onduleurs"],"phone":"0666-789067","whatsapp":"212666789067","address":"Marrakech","years_exp":13},
  {"name":"Macon Marrakech Renovation","service":"builder","city":"Marrakech","rating":4.8,"reviews":121,"verified":True,"bio":"Renovation riads et villas Marrakech. Zellige, tadelakt, stuc, bejmat. Artisan qualifie.","tags":["Riad","Zellige","Bejmat"],"phone":"0667-890178","whatsapp":"212667890178","address":"Marrakech","years_exp":22},
  {"name":"Construction Marrakech","service":"builder","city":"Marrakech","rating":4.7,"reviews":84,"verified":True,"bio":"Entrepreneur construction Marrakech et region. Villas, immeubles, renovation. Devis gratuit.","tags":["Villas","Immeubles","Renovation"],"phone":"0668-901289","whatsapp":"212668901289","address":"Marrakech","years_exp":18},
  {"name":"Peintre Tadelakt Marrakech","service":"painter","city":"Marrakech","rating":4.9,"reviews":167,"verified":True,"bio":"Specialiste tadelakt et stuc marocain Marrakech. Riads, villas, hotels. Artisan certifie.","tags":["Tadelakt","Stuc","Riads"],"phone":"0669-012390","whatsapp":"212669012390","address":"Marrakech","years_exp":20},
  {"name":"Peintre Decorateur Marrakech","service":"painter","city":"Marrakech","rating":4.7,"reviews":93,"verified":False,"bio":"Peintre decorateur Marrakech. Beton cire, moucharabieh, peinture interieure luxe.","tags":["Beton cire","Luxe","Moucharabieh"],"phone":"0661-345623","whatsapp":"212661345623","address":"Marrakech","years_exp":13},
  {"name":"Menuisier Bois Marrakech","service":"carpenter","city":"Marrakech","rating":4.8,"reviews":77,"verified":True,"bio":"Menuisier bois artisanal Marrakech. Portes sculptees, moucharabiehs, meubles sur mesure.","tags":["Portes sculptees","Moucharabieh","Artisanal"],"phone":"0662-456734","whatsapp":"212662456734","address":"Marrakech","years_exp":19},
  {"name":"Menuisier Aluminium Marrakech","service":"carpenter","city":"Marrakech","rating":4.6,"reviews":55,"verified":False,"bio":"Menuisier aluminium et PVC Marrakech. Fenetres, verandas, garde-corps. Devis rapide.","tags":["Aluminium","Verandas","Garde-corps"],"phone":"0663-567845","whatsapp":"212663567845","address":"Marrakech","years_exp":10},
  # ══ FES ══════════════════════════════════════════════════════════
  {"name":"Plombier Fes Ville","service":"plumber","city":"Fes","rating":4.7,"reviews":68,"verified":True,"bio":"Plombier Fes el Bali et Fes Jdid. Fuites, debouchage, chauffe-eau, sanitaires.","tags":["Fes el Bali","Fes Jdid","Urgence"],"phone":"0535-123401","whatsapp":"212535123401","address":"Fes","years_exp":13},
  {"name":"Plombier Narjiss Fes","service":"plumber","city":"Fes","rating":4.8,"reviews":94,"verified":True,"bio":"Plombier Narjiss et Sahrij Gnaoua. Salle de bain, cuisine, debouchage. Devis gratuit.","tags":["Narjiss","Sahrij","Salle de bain"],"phone":"0661-456734","whatsapp":"212661456734","address":"Narjiss, Fes","years_exp":11},
  {"name":"Plombier Urgence Fes","service":"plumber","city":"Fes","rating":4.6,"reviews":47,"verified":False,"bio":"Plombier urgence Fes. Fuites, pannes, debouchage. Disponible week-end et jours feries.","tags":["Week-end","Jours feries","Disponible"],"phone":"0662-567845","whatsapp":"212662567845","address":"Fes","years_exp":8},
  {"name":"Electricien Fes Medina","service":"electrician","city":"Fes","rating":4.8,"reviews":86,"verified":True,"bio":"Electricien Fes medina et ville nouvelle. Tableau, installation, depannage. 24h/7j.","tags":["Medina","Tableau","24h"],"phone":"0663-678956","whatsapp":"212663678956","address":"Fes","years_exp":14},
  {"name":"Electricien Solaire Fes","service":"electrician","city":"Fes","rating":4.7,"reviews":61,"verified":True,"bio":"Electricien et installateur solaire Fes. Panneaux photovoltaiques, chauffe-eau solaire.","tags":["Solaire","Photovoltaique","Chauffe-eau"],"phone":"0664-789067","whatsapp":"212664789067","address":"Fes","years_exp":9},
  {"name":"Macon Renovation Fes","service":"builder","city":"Fes","rating":4.8,"reviews":112,"verified":True,"bio":"Renovation riads et maisons medina Fes. Zellige, bejmat, tadelakt. Expert patrimoine.","tags":["Riad","Zellige","Patrimoine"],"phone":"0665-890178","whatsapp":"212665890178","address":"Fes","years_exp":24},
  {"name":"Construction Fes","service":"builder","city":"Fes","rating":4.6,"reviews":73,"verified":False,"bio":"Entrepreneur construction Fes et region. Maisons, villas, renovation. Qualite garantie.","tags":["Villas","Renovation","Qualite"],"phone":"0666-901289","whatsapp":"212666901289","address":"Fes","years_exp":17},
  {"name":"Peintre Fes Artisan","service":"painter","city":"Fes","rating":4.9,"reviews":138,"verified":True,"bio":"Peintre artisan Fes. Tadelakt, stuc marocain, peinture traditionnelle. Expert medina.","tags":["Tadelakt","Traditionnel","Expert"],"phone":"0667-012390","whatsapp":"212667012390","address":"Fes","years_exp":21},
  {"name":"Menuisier Bois Fes","service":"carpenter","city":"Fes","rating":4.8,"reviews":89,"verified":True,"bio":"Menuisier bois artisanal Fes. Portes cedre, moucharabiehs, meubles traditionnels.","tags":["Cedre","Moucharabieh","Traditionnel"],"phone":"0668-123401","whatsapp":"212668123401","address":"Fes","years_exp":25},
  # ══ TANGER ═══════════════════════════════════════════════════════
  {"name":"Plombier Tanger Malabata","service":"plumber","city":"Tanger","rating":4.7,"reviews":74,"verified":True,"bio":"Plombier Malabata et Marshan. Fuites, debouchage, chauffe-eau, salle de bain.","tags":["Malabata","Marshan","Salle de bain"],"phone":"0539-123401","whatsapp":"212539123401","address":"Malabata, Tanger","years_exp":11},
  {"name":"Plombier Urgence Tanger","service":"plumber","city":"Tanger","rating":4.8,"reviews":98,"verified":True,"bio":"Plombier urgence Tanger 24h/7j. Intervention 20 min. Fuites, debouchage, chauffe-eau.","tags":["24h","20 min","Urgence"],"phone":"0661-678956","whatsapp":"212661678956","address":"Tanger","years_exp":14},
  {"name":"Plombier Tanger Iberia","service":"plumber","city":"Tanger","rating":4.6,"reviews":43,"verified":False,"bio":"Plombier quartier Iberia et California Tanger. Toutes interventions plomberie. Devis gratuit.","tags":["Iberia","California","Devis"],"phone":"0662-789067","whatsapp":"212662789067","address":"Iberia, Tanger","years_exp":9},
  {"name":"Electricien Tanger Centre","service":"electrician","city":"Tanger","rating":4.8,"reviews":91,"verified":True,"bio":"Electricien centre Tanger. Tableau, prises, interphone, camera, alarme. Certifie.","tags":["Centre","Camera","Alarme"],"phone":"0663-890178","whatsapp":"212663890178","address":"Centre, Tanger","years_exp":12},
  {"name":"Electricien Tanger Solaire","service":"electrician","city":"Tanger","rating":4.7,"reviews":66,"verified":True,"bio":"Installateur solaire Tanger. Panneaux photovoltaiques, economies d energie garanties.","tags":["Solaire","Panneaux","Economies"],"phone":"0664-901289","whatsapp":"212664901289","address":"Tanger","years_exp":8},
  {"name":"Macon Tanger Renovation","service":"builder","city":"Tanger","rating":4.7,"reviews":83,"verified":True,"bio":"Renovation villas et appartements Tanger. Construction, extension, carrelage, peinture.","tags":["Villas","Extension","Carrelage"],"phone":"0665-012390","whatsapp":"212665012390","address":"Tanger","years_exp":16},
  {"name":"Peintre Tanger Pro","service":"painter","city":"Tanger","rating":4.8,"reviews":77,"verified":True,"bio":"Peintre professionnel Tanger. Interieur, exterieur, facades, enduits decoratifs.","tags":["Facades","Enduits","Pro"],"phone":"0666-123401","whatsapp":"212666123401","address":"Tanger","years_exp":13},
  {"name":"Menuisier Aluminium Tanger","service":"carpenter","city":"Tanger","rating":4.7,"reviews":62,"verified":True,"bio":"Menuisier aluminium PVC et bois Tanger. Fenetres, verandas, store banne.","tags":["Aluminium","PVC","Store banne"],"phone":"0667-234512","whatsapp":"212667234512","address":"Tanger","years_exp":10},
  # ══ AGADIR ════════════════════════════════════════════════════════
  {"name":"Plombier Agadir Hay Mohammadi","service":"plumber","city":"Agadir","rating":4.7,"reviews":69,"verified":True,"bio":"Plombier Hay Mohammadi et Talborjt. Fuites, debouchage, chauffe-eau solaire, sanitaires.","tags":["Hay Mohammadi","Talborjt","Solaire"],"phone":"0528-123401","whatsapp":"212528123401","address":"Hay Mohammadi, Agadir","years_exp":12},
  {"name":"Plombier Urgence Agadir","service":"plumber","city":"Agadir","rating":4.8,"reviews":107,"verified":True,"bio":"Plombier urgence Agadir 24h. Intervention rapide. Fuites, WC, douche, chauffe-eau.","tags":["24h","Rapide","WC"],"phone":"0661-789067","whatsapp":"212661789067","address":"Agadir","years_exp":15},
  {"name":"Plombier Agadir Marina","service":"plumber","city":"Agadir","rating":4.6,"reviews":38,"verified":False,"bio":"Plombier Marina et Founty Agadir. Villas, appartements, residences. Devis gratuit.","tags":["Marina","Founty","Residences"],"phone":"0662-890178","whatsapp":"212662890178","address":"Marina, Agadir","years_exp":9},
  {"name":"Electricien Agadir Pro","service":"electrician","city":"Agadir","rating":4.8,"reviews":94,"verified":True,"bio":"Electricien Agadir et Inezgane. Tableau, climatisation, solaire, domotique. Certifie.","tags":["Inezgane","Climatisation","Domotique"],"phone":"0663-901289","whatsapp":"212663901289","address":"Agadir","years_exp":14},
  {"name":"Electricien Solaire Agadir","service":"electrician","city":"Agadir","rating":4.9,"reviews":152,"verified":True,"bio":"Specialiste solaire Agadir-Souss. Panneaux, onduleurs, batterie, autoconsommation.","tags":["Souss","Autoconsommation","Batterie"],"phone":"0664-012390","whatsapp":"212664012390","address":"Agadir","years_exp":11},
  {"name":"Macon Agadir Construction","service":"builder","city":"Agadir","rating":4.7,"reviews":88,"verified":True,"bio":"Entrepreneur Agadir. Construction villas, hotels, immeubles. Gros oeuvre et renovation.","tags":["Villas","Hotels","Gros oeuvre"],"phone":"0665-123401","whatsapp":"212665123401","address":"Agadir","years_exp":20},
  {"name":"Peintre Agadir Facade","service":"painter","city":"Agadir","rating":4.7,"reviews":71,"verified":True,"bio":"Peintre facade et interieur Agadir. Enduits, hydrofuge, isolation thermique par exterieur.","tags":["Facade","Hydrofuge","Isolation"],"phone":"0666-234512","whatsapp":"212666234512","address":"Agadir","years_exp":12},
  {"name":"Menuisier Agadir Aluminium","service":"carpenter","city":"Agadir","rating":4.6,"reviews":54,"verified":False,"bio":"Menuisier aluminium Agadir. Fenetres, portes, garde-corps, pergolas sur mesure.","tags":["Pergolas","Garde-corps","Sur mesure"],"phone":"0667-345623","whatsapp":"212667345623","address":"Agadir","years_exp":9},
  # ══ MEKNES ════════════════════════════════════════════════════════
  {"name":"Plombier Meknes Centre","service":"plumber","city":"Meknes","rating":4.7,"reviews":61,"verified":True,"bio":"Plombier Meknes centre et Hamriya. Fuites, debouchage, chauffe-eau, salle de bain.","tags":["Centre","Hamriya","Salle de bain"],"phone":"0535-234512","whatsapp":"212535234512","address":"Meknes","years_exp":13},
  {"name":"Electricien Meknes Pro","service":"electrician","city":"Meknes","rating":4.8,"reviews":79,"verified":True,"bio":"Electricien Meknes. Tableau electrique, climatisation, solaire, alarme. Devis gratuit.","tags":["Tableau","Solaire","Alarme"],"phone":"0661-890178","whatsapp":"212661890178","address":"Meknes","years_exp":11},
  {"name":"Macon Renovation Meknes","service":"builder","city":"Meknes","rating":4.7,"reviews":84,"verified":True,"bio":"Renovation maisons et riads Meknes. Zellige, tadelakt, renovation complete.","tags":["Riad","Zellige","Renovation"],"phone":"0662-901289","whatsapp":"212662901289","address":"Meknes","years_exp":18},
  {"name":"Peintre Meknes Artisan","service":"painter","city":"Meknes","rating":4.8,"reviews":93,"verified":True,"bio":"Peintre artisan Meknes. Tadelakt, stuc, peinture traditionnelle et moderne.","tags":["Tadelakt","Stuc","Traditionnel"],"phone":"0663-012390","whatsapp":"212663012390","address":"Meknes","years_exp":16},
  {"name":"Menuisier Meknes Bois","service":"carpenter","city":"Meknes","rating":4.7,"reviews":67,"verified":False,"bio":"Menuisier bois Meknes. Portes, fenetres, cuisines, meubles sur mesure.","tags":["Bois","Cuisine","Sur mesure"],"phone":"0664-123401","whatsapp":"212664123401","address":"Meknes","years_exp":14},
  # ══ OUJDA ═════════════════════════════════════════════════════════
  {"name":"Plombier Oujda Centre","service":"plumber","city":"Oujda","rating":4.6,"reviews":52,"verified":True,"bio":"Plombier Oujda centre. Fuites, debouchage, chauffe-eau, installation sanitaires.","tags":["Centre","Fuites","Chauffe-eau"],"phone":"0536-123401","whatsapp":"212536123401","address":"Oujda","years_exp":10},
  {"name":"Electricien Oujda Pro","service":"electrician","city":"Oujda","rating":4.7,"reviews":68,"verified":True,"bio":"Electricien Oujda et region. Tableau, installation, solaire, climatisation.","tags":["Tableau","Solaire","Climatisation"],"phone":"0661-901289","whatsapp":"212661901289","address":"Oujda","years_exp":12},
  {"name":"Macon Oujda Construction","service":"builder","city":"Oujda","rating":4.6,"reviews":71,"verified":True,"bio":"Entrepreneur construction Oujda-Oriental. Villas, renovation, carrelage, finitions.","tags":["Oriental","Villas","Finitions"],"phone":"0662-012390","whatsapp":"212662012390","address":"Oujda","years_exp":16},
  {"name":"Peintre Oujda","service":"painter","city":"Oujda","rating":4.7,"reviews":58,"verified":False,"bio":"Peintre Oujda. Interieur, exterieur, facade, tadelakt. Devis gratuit sur place.","tags":["Facade","Tadelakt","Devis"],"phone":"0663-123401","whatsapp":"212663123401","address":"Oujda","years_exp":11},
  # ══ AUTRES VILLES ═════════════════════════════════════════════════
  {"name":"Plombier Nador","service":"plumber","city":"Nador","rating":4.6,"reviews":44,"verified":True,"bio":"Plombier Nador et Selouane. Fuites, debouchage, chauffe-eau, salle de bain.","tags":["Nador","Selouane","Urgent"],"phone":"0536-234512","whatsapp":"212536234512","address":"Nador","years_exp":9},
  {"name":"Electricien Nador","service":"electrician","city":"Nador","rating":4.7,"reviews":57,"verified":True,"bio":"Electricien Nador. Tableau, installation, depannage, solaire. Intervention rapide.","tags":["Tableau","Solaire","Rapide"],"phone":"0661-012390","whatsapp":"212661012390","address":"Nador","years_exp":11},
  {"name":"Macon Nador","service":"builder","city":"Nador","rating":4.6,"reviews":62,"verified":False,"bio":"Macon Nador et region. Construction, renovation, carrelage, peinture. Devis gratuit.","tags":["Construction","Renovation","Carrelage"],"phone":"0662-123401","whatsapp":"212662123401","address":"Nador","years_exp":13},
  {"name":"Plombier Tetouan","service":"plumber","city":"Tetouan","rating":4.7,"reviews":59,"verified":True,"bio":"Plombier Tetouan et Martil. Fuites, debouchage, chauffe-eau, salle de bain complete.","tags":["Tetouan","Martil","Complet"],"phone":"0539-345623","whatsapp":"212539345623","address":"Tetouan","years_exp":12},
  {"name":"Electricien Tetouan","service":"electrician","city":"Tetouan","rating":4.7,"reviews":64,"verified":True,"bio":"Electricien Tetouan. Tableau, installation, climatisation, solaire. Devis gratuit.","tags":["Tableau","Climatisation","Solaire"],"phone":"0661-345634","whatsapp":"212661345634","address":"Tetouan","years_exp":10},
  {"name":"Macon Renovation Tetouan","service":"builder","city":"Tetouan","rating":4.8,"reviews":78,"verified":True,"bio":"Renovation maisons Tetouan et region. Construction, extension, finitions. Expert local.","tags":["Extension","Finitions","Expert"],"phone":"0662-456745","whatsapp":"212662456745","address":"Tetouan","years_exp":17},
  {"name":"Peintre Tetouan","service":"painter","city":"Tetouan","rating":4.7,"reviews":52,"verified":False,"bio":"Peintre Tetouan. Interieur, facade, tadelakt, stuc. Artisan qualifie.","tags":["Facade","Tadelakt","Qualifie"],"phone":"0663-567856","whatsapp":"212663567856","address":"Tetouan","years_exp":13},
  {"name":"Plombier Kenitra","service":"plumber","city":"Kenitra","rating":4.7,"reviews":63,"verified":True,"bio":"Plombier Kenitra. Fuites, debouchage, chauffe-eau, sanitaires. Intervention rapide.","tags":["Kenitra","Fuites","Rapide"],"phone":"0537-123401","whatsapp":"212537123401","address":"Kenitra","years_exp":11},
  {"name":"Electricien Kenitra","service":"electrician","city":"Kenitra","rating":4.6,"reviews":48,"verified":False,"bio":"Electricien Kenitra et Sale. Tableau, installation, depannage. Tarifs competitifs.","tags":["Sale","Tableau","Competitif"],"phone":"0661-678967","whatsapp":"212661678967","address":"Kenitra","years_exp":9},
  {"name":"Plombier Sale Tabriquet","service":"plumber","city":"Sale","rating":4.7,"reviews":67,"verified":True,"bio":"Plombier Sale Tabriquet et Bettana. Fuites, debouchage, chauffe-eau. Devis gratuit.","tags":["Tabriquet","Bettana","Devis"],"phone":"0537-234512","whatsapp":"212537234512","address":"Sale","years_exp":12},
  {"name":"Electricien Sale","service":"electrician","city":"Sale","rating":4.7,"reviews":54,"verified":True,"bio":"Electricien Sale. Tableau, installation, climatisation, solaire. Certifie.","tags":["Tableau","Climatisation","Certifie"],"phone":"0661-789078","whatsapp":"212661789078","address":"Sale","years_exp":10},
  {"name":"Macon Sale","service":"builder","city":"Sale","rating":4.6,"reviews":61,"verified":False,"bio":"Macon Sale et environs. Renovation, construction, carrelage, peinture.","tags":["Renovation","Carrelage","Peinture"],"phone":"0662-890189","whatsapp":"212662890189","address":"Sale","years_exp":14},
  {"name":"Plombier El Jadida","service":"plumber","city":"El Jadida","rating":4.7,"reviews":49,"verified":True,"bio":"Plombier El Jadida et Azemmour. Fuites, debouchage, chauffe-eau. Rapide.","tags":["El Jadida","Azemmour","Rapide"],"phone":"0523-123401","whatsapp":"212523123401","address":"El Jadida","years_exp":11},
  {"name":"Electricien El Jadida","service":"electrician","city":"El Jadida","rating":4.6,"reviews":43,"verified":False,"bio":"Electricien El Jadida. Tableau, installation, solaire. Devis gratuit.","tags":["Tableau","Solaire","Devis"],"phone":"0661-901290","whatsapp":"212661901290","address":"El Jadida","years_exp":9},
  {"name":"Plombier Safi","service":"plumber","city":"Safi","rating":4.6,"reviews":38,"verified":True,"bio":"Plombier Safi. Fuites, debouchage, chauffe-eau, sanitaires. Devis gratuit.","tags":["Safi","Fuites","Devis"],"phone":"0524-456734","whatsapp":"212524456734","address":"Safi","years_exp":10},
  {"name":"Electricien Safi","service":"electrician","city":"Safi","rating":4.7,"reviews":44,"verified":True,"bio":"Electricien Safi. Tableau, installation, solaire, climatisation.","tags":["Tableau","Solaire","Climatisation"],"phone":"0661-012401","whatsapp":"212661012401","address":"Safi","years_exp":11},
  {"name":"Plombier Beni Mellal","service":"plumber","city":"Beni Mellal","rating":4.6,"reviews":41,"verified":True,"bio":"Plombier Beni Mellal. Fuites, debouchage, chauffe-eau. Intervention rapide.","tags":["Beni Mellal","Fuites","Rapide"],"phone":"0523-234512","whatsapp":"212523234512","address":"Beni Mellal","years_exp":11},
  {"name":"Electricien Beni Mellal","service":"electrician","city":"Beni Mellal","rating":4.7,"reviews":52,"verified":True,"bio":"Electricien Beni Mellal. Tableau, installation, solaire. Certifie.","tags":["Tableau","Solaire","Certifie"],"phone":"0661-123412","whatsapp":"212661123412","address":"Beni Mellal","years_exp":12},
  {"name":"Macon Beni Mellal","service":"builder","city":"Beni Mellal","rating":4.6,"reviews":58,"verified":False,"bio":"Macon Beni Mellal. Construction, renovation, carrelage. Devis gratuit.","tags":["Construction","Carrelage","Devis"],"phone":"0662-234523","whatsapp":"212662234523","address":"Beni Mellal","years_exp":15},
  {"name":"Plombier Al Hoceima","service":"plumber","city":"Al Hoceima","rating":4.6,"reviews":38,"verified":True,"bio":"Plombier Al Hoceima. Fuites, debouchage, chauffe-eau, salle de bain.","tags":["Urgent","Fuites","Salle de bain"],"phone":"0539-456734","whatsapp":"212539456734","address":"Al Hoceima","years_exp":10},
  {"name":"Electricien Al Hoceima","service":"electrician","city":"Al Hoceima","rating":4.7,"reviews":47,"verified":True,"bio":"Electricien Al Hoceima. Tableau, installation, solaire. Intervention rapide.","tags":["Tableau","Solaire","Rapide"],"phone":"0661-345645","whatsapp":"212661345645","address":"Al Hoceima","years_exp":9},
  {"name":"Plombier Chefchaouen","service":"plumber","city":"Chefchaouen","rating":4.7,"reviews":34,"verified":True,"bio":"Plombier Chefchaouen. Fuites, debouchage, chauffe-eau. Artisan local qualifie.","tags":["Local","Qualifie","Artisan"],"phone":"0539-567845","whatsapp":"212539567845","address":"Chefchaouen","years_exp":12},
  {"name":"Macon Chefchaouen","service":"builder","city":"Chefchaouen","rating":4.8,"reviews":42,"verified":True,"bio":"Macon Chefchaouen. Renovation maisons traditionnelles, pierre, zellige. Expert local.","tags":["Pierre","Zellige","Traditionnel"],"phone":"0661-456756","whatsapp":"212661456756","address":"Chefchaouen","years_exp":18},
  {"name":"Plombier Ouarzazate","service":"plumber","city":"Ouarzazate","rating":4.7,"reviews":33,"verified":True,"bio":"Plombier Ouarzazate. Fuites, chauffe-eau solaire, sanitaires. Expert region.","tags":["Solaire","Expert","Region"],"phone":"0524-234512","whatsapp":"212524234512","address":"Ouarzazate","years_exp":12},
  {"name":"Electricien Ouarzazate","service":"electrician","city":"Ouarzazate","rating":4.8,"reviews":41,"verified":True,"bio":"Electricien Ouarzazate. Solaire, tableau, climatisation. Hotels et villas.","tags":["Hotels","Villas","Solaire"],"phone":"0661-567867","whatsapp":"212661567867","address":"Ouarzazate","years_exp":13},
  {"name":"Macon Ouarzazate","service":"builder","city":"Ouarzazate","rating":4.7,"reviews":47,"verified":True,"bio":"Macon Ouarzazate. Construction kasbahs, villas, renovation. Artisan qualifie.","tags":["Kasbahs","Villas","Artisan"],"phone":"0662-678978","whatsapp":"212662678978","address":"Ouarzazate","years_exp":19},
  {"name":"Plombier Essaouira","service":"plumber","city":"Essaouira","rating":4.7,"reviews":36,"verified":True,"bio":"Plombier Essaouira. Fuites, debouchage, chauffe-eau. Riad et villas.","tags":["Riad","Villas","Fuites"],"phone":"0524-345623","whatsapp":"212524345623","address":"Essaouira","years_exp":11},
  {"name":"Macon Renovation Essaouira","service":"builder","city":"Essaouira","rating":4.8,"reviews":53,"verified":True,"bio":"Renovation riads Essaouira. Pierre bleue, bois thuya, tadelakt. Expert patrimoine.","tags":["Riad","Thuya","Pierre bleue"],"phone":"0661-789089","whatsapp":"212661789089","address":"Essaouira","years_exp":20},
  {"name":"Plombier Laayoune","service":"plumber","city":"Laayoune","rating":4.6,"reviews":29,"verified":True,"bio":"Plombier Laayoune. Fuites, debouchage, chauffe-eau, sanitaires. Devis gratuit.","tags":["Laayoune","Fuites","Devis"],"phone":"0528-678956","whatsapp":"212528678956","address":"Laayoune","years_exp":10},
  {"name":"Electricien Laayoune","service":"electrician","city":"Laayoune","rating":4.7,"reviews":36,"verified":True,"bio":"Electricien Laayoune. Tableau, installation, solaire, climatisation.","tags":["Solaire","Tableau","Climatisation"],"phone":"0661-890190","whatsapp":"212661890190","address":"Laayoune","years_exp":11},
  {"name":"Macon Laayoune","service":"builder","city":"Laayoune","rating":4.6,"reviews":31,"verified":False,"bio":"Macon Laayoune. Construction, renovation, carrelage. Devis gratuit.","tags":["Construction","Renovation","Carrelage"],"phone":"0662-901201","whatsapp":"212662901201","address":"Laayoune","years_exp":13},
  {"name":"Plombier Dakhla","service":"plumber","city":"Dakhla","rating":4.6,"reviews":22,"verified":True,"bio":"Plombier Dakhla. Fuites, debouchage, chauffe-eau. Intervention rapide.","tags":["Dakhla","Fuites","Rapide"],"phone":"0528-789067","whatsapp":"212528789067","address":"Dakhla","years_exp":8},
  {"name":"Electricien Dakhla","service":"electrician","city":"Dakhla","rating":4.7,"reviews":27,"verified":True,"bio":"Electricien Dakhla. Tableau, installation, solaire. Devis gratuit.","tags":["Solaire","Tableau","Devis"],"phone":"0661-012312","whatsapp":"212661012312","address":"Dakhla","years_exp":9},
  {"name":"Plombier Guelmim","service":"plumber","city":"Guelmim","rating":4.5,"reviews":18,"verified":True,"bio":"Plombier Guelmim. Fuites, debouchage, chauffe-eau, sanitaires.","tags":["Guelmim","Fuites","Sanitaires"],"phone":"0528-890178","whatsapp":"212528890178","address":"Guelmim","years_exp":9},
  {"name":"Electricien Guelmim","service":"electrician","city":"Guelmim","rating":4.6,"reviews":24,"verified":False,"bio":"Electricien Guelmim. Tableau, installation, solaire.","tags":["Tableau","Solaire","Installation"],"phone":"0661-123423","whatsapp":"212661123423","address":"Guelmim","years_exp":8},
  {"name":"Plombier Tiznit","service":"plumber","city":"Tiznit","rating":4.6,"reviews":22,"verified":True,"bio":"Plombier Tiznit. Fuites, chauffe-eau solaire, sanitaires. Expert local.","tags":["Solaire","Expert","Local"],"phone":"0528-567845","whatsapp":"212528567845","address":"Tiznit","years_exp":10},
  {"name":"Electricien Tiznit","service":"electrician","city":"Tiznit","rating":4.7,"reviews":27,"verified":False,"bio":"Electricien Tiznit. Tableau, solaire, installation. Devis gratuit.","tags":["Tableau","Solaire","Devis"],"phone":"0661-234534","whatsapp":"212661234534","address":"Tiznit","years_exp":9},
  {"name":"Plombier Taroudannt","service":"plumber","city":"Taroudannt","rating":4.6,"reviews":27,"verified":True,"bio":"Plombier Taroudannt. Fuites, chauffe-eau solaire, sanitaires. Devis gratuit.","tags":["Solaire","Fuites","Devis"],"phone":"0528-456734","whatsapp":"212528456734","address":"Taroudannt","years_exp":10},
  {"name":"Electricien Taroudannt","service":"electrician","city":"Taroudannt","rating":4.7,"reviews":32,"verified":False,"bio":"Electricien Taroudannt. Tableau, installation, solaire. Tarifs competitifs.","tags":["Tableau","Solaire","Competitif"],"phone":"0661-345645","whatsapp":"212661345645","address":"Taroudannt","years_exp":9},
  {"name":"Plombier Errachidia","service":"plumber","city":"Errachidia","rating":4.6,"reviews":24,"verified":True,"bio":"Plombier Errachidia. Fuites, chauffe-eau, sanitaires. Expert region.","tags":["Expert","Fuites","Region"],"phone":"0535-345623","whatsapp":"212535345623","address":"Errachidia","years_exp":11},
  {"name":"Electricien Errachidia","service":"electrician","city":"Errachidia","rating":4.6,"reviews":29,"verified":False,"bio":"Electricien Errachidia. Tableau, solaire, installation. Devis gratuit.","tags":["Solaire","Tableau","Devis"],"phone":"0661-456756","whatsapp":"212661456756","address":"Errachidia","years_exp":10},
  {"name":"Plombier Settat","service":"plumber","city":"Settat","rating":4.6,"reviews":33,"verified":True,"bio":"Plombier Settat. Fuites, debouchage, chauffe-eau, sanitaires.","tags":["Settat","Fuites","Sanitaires"],"phone":"0523-345623","whatsapp":"212523345623","address":"Settat","years_exp":9},
  {"name":"Electricien Settat","service":"electrician","city":"Settat","rating":4.6,"reviews":39,"verified":False,"bio":"Electricien Settat. Tableau, installation, solaire. Devis gratuit.","tags":["Tableau","Solaire","Devis"],"phone":"0661-567867","whatsapp":"212661567867","address":"Settat","years_exp":10},
  {"name":"Plombier Taza","service":"plumber","city":"Taza","rating":4.5,"reviews":28,"verified":True,"bio":"Plombier Taza. Fuites, debouchage, chauffe-eau. Artisan local.","tags":["Taza","Local","Fuites"],"phone":"0535-456734","whatsapp":"212535456734","address":"Taza","years_exp":10},
  {"name":"Plombier Larache","service":"plumber","city":"Larache","rating":4.6,"reviews":31,"verified":True,"bio":"Plombier Larache. Fuites, debouchage, chauffe-eau. Devis gratuit.","tags":["Larache","Fuites","Devis"],"phone":"0539-678956","whatsapp":"212539678956","address":"Larache","years_exp":10},
  {"name":"Plombier Berkane","service":"plumber","city":"Berkane","rating":4.6,"reviews":26,"verified":True,"bio":"Plombier Berkane. Fuites, chauffe-eau, sanitaires. Intervention rapide.","tags":["Berkane","Fuites","Rapide"],"phone":"0536-345623","whatsapp":"212536345623","address":"Berkane","years_exp":9},

]

def seed_db():
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

# ── REVIEWS ──────────────────────────────────────────────────────
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, nullable=False)
    author = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

class ReviewIn(BaseModel):
    worker_id: int
    author: str
    rating: int
    comment: str

class ReviewOut(BaseModel):
    id: int
    worker_id: int
    author: str
    rating: int
    comment: str
    created_at: str
    class Config: from_attributes = True

@app.get("/reviews/{worker_id}", response_model=list[ReviewOut])
def get_reviews(worker_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.worker_id == worker_id).order_by(Review.id.desc()).all()

@app.post("/reviews", response_model=ReviewOut, status_code=201)
def add_review(data: ReviewIn, db: Session = Depends(get_db)):
    review = Review(**data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
