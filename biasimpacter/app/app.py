from dataprovider import Date, Validator, RSSReader, StoryRSS
from models import ModelRSS
from threading import Thread
import logging
import schedule
import time
import json
import os


logging.basicConfig(filename=os.getenv("BIASIMPACTER_OUTPUT"), 
                    level=logging.INFO, 
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())


def set_up_mongo():
    try:
        mongo_host = os.getenv("BIASIMPACTER_DC_MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        mongo_db = os.getenv("APP_MONGO_DB")
        mongo_user = os.getenv("APP_MONGO_USER")
        mongo_pw = os.getenv("APP_MONGO_PASS")
        mongo_uri = "mongodb://{}:{}@{}:{}/{}".format(
            mongo_user, mongo_pw, mongo_host, mongo_port, mongo_db)
        logging.info(mongo_uri)
        return  mongo_uri
    except Exception() as e:
        logging.error(e)

if __name__ == "__main__":
    uri = set_up_mongo()
    mongo = ModelRSS(uri).client
    urls = [
        ("20minutes_fr", "https://www.20minutes.fr/feeds/rss-une.xml"),
        ("atlantico_fr", "http://www.atlantico.fr/rss.xml"),
        ("bastamag_fr", "https://www.bastamag.net/spip.php?page=backend"),
        ("bfmtv_fr", "http://www.bfmtv.com/rss/info/flux-rss/flux-toutes-les-actualites/"),
        ("capital_fr", "https://feed.prismamediadigital.com/v1/cap/rss?sources=capital,polemik,xerfi,capital-avec-agence-france-presse,capital-avec-aof,capital-avec-reuters,capital-avec-optimaretraite"),
        ("challenges_fr", "https://www.challenges.fr/rss.xml"),
        ("contexte_fr", "https://www.contexte.com/articles/rss"),
        ("courrier_international_fr",
         "https://www.courrierinternational.com/feed/all/rss.xml"),
        ("dna_fr", "http://www.dna.fr/rss"),
        ("europe1_fr", "http://www.europe1.fr/var/export/rss/europe1/actus.xml"),
        ("francebleu_fr", "https://www.francebleu.fr/rss/infos.xml"),
        ("franceculture_fr", "https://www.franceculture.fr/rss"),
        ("franceinter_fr", "https://www.franceinter.fr/rss/a-la-une.xml"),
        ("francetvinfo_fr", "https://www.francetvinfo.fr/titres.rss"),
        ("huffingtonpost_fr", "http://www.huffingtonpost.fr/feeds/index.xml"),
        ("konbini_fr", "http://www.konbini.com/fr/feed/"),
        ("lalsace_fr", "http://www.lalsace.fr/rss"),
        ("lequipe_fr", "http://www.lequipe.fr/rss/actu_rss.xml"),
        ("lexpress_fr", "https://www.lexpress.fr/rss/alaune.xml"),
        ("lhumanite_fr", "https://humanite.fr/rss/actu.rss"),
        ("limportant_fr", "https://limportant.fr/rss"),
        ("linternaute_fr", "http://www.linternaute.com/rss/"),
        ("nouvelobs_fr", "http://www.nouvelobs.com/atom.xml"),
        ("lopinion_fr", "http://www.lopinion.fr/rss.xml"),
        ("lacroix_fr", "http://www.la-croix.com/RSS/UNIVERS"),
        ("ladepeche_fr", "https://www.ladepeche.fr/rss/home.rss"),
        ("lanouvellerepublique_fr",
         "https://www.lanouvellerepublique.fr/api/v1/rss/592bf255489a4555008b4568"),
        ("latribune_fr", "https://www.latribune.fr/feed.xml"),
        ("lavoixdunord", "http://www.lavoixdunord.fr/rss.xml"),
        ("ledauphine", "http://www.ledauphine.com/rss"),
        ("lefigaro_fr", "http://www.lefigaro.fr/rss/figaro_actualites.xml"),
        ("lemonde_fr", "http://www.lemonde.fr/rss/une.xml"),
        ("leparisien_fr", "http://www.leparisien.fr/actualites-a-la-une.rss.xml"),
        ("lepoint_fr", "http://www.lepoint.fr/24h-infos/rss.xml"),
        ("leprogres_fr", "http://www.leprogres.fr/rss"),
        ("republicainlorrain_fr", "http://www.republicain-lorrain.fr/rss"),
        ("letelegramme_fr", "http://www.letelegramme.fr/rss.xml"),
        ("lesechos_fr", "https://www.lesechos.fr/rss/rss_une.xml"),
        ("lesinrocks_fr", "https://www.lesinrocks.com/actualite/feed/"),
        ("lesjours_fr", "https://lesjours.fr/rss.xml"),
        ("liberation_fr", "http://rss.liberation.fr/rss/latest/"),
        ("marianne_fr", "https://www.marianne.net/rss.xml"),
        ("mediapart_fr", "https://www.mediapart.fr/articles/feed"),
        ("nicematin_fr", "http://www.nicematin.com/rss"),
        ("ouestfrance_fr", "https://www.ouest-france.fr/rss-en-continu.xml"),
        ("parismatch_fr", "http://cdn1-parismatch.ladmedia.fr/var/exports/rss/rss-actu.xml"),
        ("politis_fr", "https://www.politis.fr/rss.xml"),
        ("reporterre_fr", "https://reporterre.net/spip.php?page=backend-simple"),
        ("rfi_fr", "http://www.rfi.fr/general/rss"),
        ("rt_fr", "https://francais.rt.com/rss"),
        ("rtl_fr", "http://www.rtl.fr/flux/une.rss"),
        ("slate_fr", "https://www.slate.fr/rss.xml"),
        ("sputiknews_fr", "https://fr.sputniknews.com/export/rss2/archive/index.xml"),
        ("streetpress_fr", "https://www.streetpress.com/rss.xml"),
        ("sudouest_fr", "http://www.sudouest.fr/essentiel/rss.xml"),
        ("theconversation_fr", "https://theconversation.com/articles.atom?language=fr"),
        ("vice_fr", "https://www.vice.com/fr/rss"),
        ("eurosport_fr", "https://www.eurosport.fr/rss.xml"),
        ("france24_fr", "http://www.france24.com/fr/actualites/rss"),
        ("fdesouche_fr", "http://www.fdesouche.com/feed"),
        ("lamediapress_fr", "https://lemediapresse.fr/feed/"),
        ("mediacite_fr", "https://www.mediacites.fr/feed/"),
        ("regards_fr", "http://www.regards.fr/spip.php?page=backend"),
    ]
    for name, url in urls:
        try:
            logging.info("Reading story: {}".format(name))
            story = StoryRSS(logging, name, url, mongo.database)
            story.save_story()
        except Exception as e:
            logging.error(e)