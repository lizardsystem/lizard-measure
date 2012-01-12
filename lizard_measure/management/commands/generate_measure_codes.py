# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from lizard_krw.models import MeasureCode


codes = (
    ('BE01', 'Beheermaatregelen uitvoeren'
             ' actief visstands- of schelpdierstandsbeheer'),
    ('BE02', 'Beheermaatregelen uitvoeren'
             ' actief vegetatiebeheer (enten, zaaien, planten)'),
    ('BE03', 'Beheermaatregelen uitvoeren op waterkwaliteit'
             '  gericht onderhouds-/maaibeheer (water & natte oever)'),
    ('BE04', 'Beheermaatregelen Verwijderen'
             ' eutrofe bagger'),
    ('BE05', 'Beheermaatregelen verwijderen'
             ' vervuilde bagger (m.u.v. eutrofe bagger)'),
    ('BE06', 'Beheermaatregelen aanpassen'
             ' begroeiing langs water'),
    ('BE07', 'Beheermaatregelen Beheren'
             ' van grootschalige grondwaterverontreinigingen'),
    ('BE08', 'Beheermaatregelen overige'
             ' beheermaatregelen'),
    ('BR01', 'Bronmaatregelen verminderen'
             ' emissie nutriënten landbouw'),
    ('BR02', 'Bronmaatregelen verminderen emissie zware'
             ' metalen en overige microverontreinigingen landbouw'),
    ('BR03', 'Bronmaatregelen verminderen'
             ' emissie gewasbeschermingsmiddelen landbouw'),
    ('BR04', 'Bronmaatregelen verminderen'
             ' emissie scheepvaart'),
    ('BR05', 'Bronmaatregelen verminderen'
             ' emissie verkeer'),
    ('BR06', 'Bronmaatregelen verminderen'
             ' diffuse emissie industrie'),
    ('BR07', 'Bronmaatregelen saneren'
             ' uitlogende oeverbescherming'),
    ('BR08', 'Bronmaatregelen verminderen'
             ' emissies bouwmaterialen'),
    ('BR09', 'Bronmaatregelen verminderen'
             ' emissie gewasbeschermingsmiddelen stad'),
    ('BR10', 'Bronmaatregelen overige'
             ' bronmaatregelen'),
    ('GGOR', 'Overige maatregelen'
             ' GGOR maatregelen'),
    ('IM01', 'Immissiemaatregelen'
             ' verminderen belasting RWZI – nutriënten'),
    ('IM02', 'Immissiemaatregelen'
             ' verminderen belasting RWZI – overige stoffen'),
    ('IM03', 'Immissiemaatregelen'
             ' aanpakken overstorten gemengde stelsels'),
    ('IM04', 'Immissiemaatregelen'
             ' zuiveren + afkoppelen verhard oppervlak'),
    ('IM05', 'Immissiemaatregelen'
             ' herstellen lekke riolen'),
    ('IM06', 'Immissiemaatregelen'
             ' opheffen ongezuiverde lozingen'),
    ('IM07', 'Immissiemaatregelen'
             ' spuitvrije zones'),
    ('IM08', 'Immissiemaatregelen'
             ' mestvrije zones'),
    ('IM09', 'Immissiemaatregelen'
             ' aanleg zuiveringsmoeras bij lozings- en/of innamepunt'),
    ('IM10', 'Immissiemaatregelen'
             ' saneren verontreinigde landbodems'),
    ('IM11', 'Immissiemaatregelen'
             ' saneren verontreinigde landbodem en/of grondwater'),
    ('IM12', 'Immissiemaatregelen'
             ' overige emissiereducerende maatregelen'),
    ('IN01', 'Inrichtingsmaatregelen'
             ' vasthouden water in haarvaten van het systeem'),
    ('IN02', 'Inrichtingsmaatregelen'
             ' omleiden/scheiden waterstromen'),
    ('IN03', 'Inrichtingsmaatregelen'
             ' invoeren/wijzigen doorspoelen'),
    ('IN04', 'Inrichtingsmaatregelen verbreden'
             ' (snel) stromend water/hermeanderen, NVO < 3 m'),
    ('IN05', 'Inrichtingsmaatregelen verbreden'
             ' (snel) stromend water/hermeanderen, 3m < NVO < 10 m'),
    ('IN06', 'Inrichtingsmaatregelen verbreden'
             ' (snel) stromend water/ hermeanderen , NVO >10 m'),
    ('IN07', 'Inrichtingsmaatregelen verbreden watergang/-systeem'
             ' langzaam stromend of stilstaand: NVO < 3 m'),
    ('IN08', 'Inrichtingsmaatregelen verbreden watergang/-systeem'
             ' langzaam stromend of stilstaand: 3m < NVO < 10 m'),
    ('IN09', 'Inrichtingsmaatregelen verbreden watergang/-systeem'
             ' langzaam stromend of stilstaand: NVO >10 m '),
    ('IN10', 'Inrichtingsmaatregelen verbreden watergang/-systeem:'
             ' aansluiten wetland of verlagen uiterwaard'),
    ('IN11', 'Inrichtingsmaatregelen'
             ' aanleg nevengeul/herstel verbinding'),
    ('IN12', 'Inrichtingsmaatregelen'
             ' verdiepen watergang/-systeem (overdimensioneren)'),
    ('IN13', 'Inrichtingsmaatregelen'
             ' verondiepen watergang/-systeem'),
    ('IN14', 'Inrichtingsmaatregelen'
             ' aanpassen streefpeil'),
    ('IN15', 'Inrichtingsmaatregelen'
             ' Vispasseerbaar maken kunstwerken'),
    ('IN16', 'Inrichtingsmaatregelen'
             ' verwijderen stuw'),
    ('IN17', 'Inrichtingsmaatregelen'
             ' aanleg speciale leefgebieden voor vis'),
    ('IN18', 'Inrichtingsmaatregelen'
             ' aanleg speciale leefgebieden flora en fauna'),
    ('IN19', 'Inrichtingsmaatregelen'
             ' aanleg zuiveringsmoeras'),
    ('IN20', 'Inrichtingsmaatregelen'
             ' overige inrichtingsmaatregelen'),
    ('RO01', 'RO-maatregelen wijzigen landbouwfunctie'),
    ('RO02', 'RO-maatregelen beperken recreatie'),
    ('RO03', 'RO-maatregelen beperken scheepvaart'),
    ('RO04', 'RO-maatregelen wijzigen visserij'),
    ('RO05', 'RO-maatregelen wijzigen stedelijke functie'),
    ('RO06', 'RO-maatregelen'
             ' mijden risicovolle functies in grondwaterbeschermingsgebieden'),
    ('RO07', 'RO-maatregelen'
             ' verminderen/verplaatsen van de grondwaterwinning'),
    ('RO08', 'RO-maatregelen'
             ' Stopzetten van kleine winningen (campings)'),
    ('RO09', 'RO-maatregelen'
             ' overige RO-maatregelen'),
    ('S01', 'Instrumentele maatregelen'
             ' uitvoeren onderzoek'),
    ('S02', 'Instrumentele maatregelen'
             ' geven van voorlichting'),
    ('S03', 'Instrumentele maatregelen'
             ' aanpassen/introduceren (nieuwe) wetgeving'),
    ('S04', 'Instrumentele maatregelen'
             ' opstellen nieuw plan'),
    ('S05', 'Instrumentele maatregelen'
             ' financiële maatregelen'),
    ('S06', 'Instrumentele maatregelen'
             ' overige instrumentele maatregelen'),
    ('WB21', 'Overige maatregelen WB21 maatregelen'),
)


class Command(BaseCommand):
    args = ''
    help = 'Generates initial measure codes for hhnk'

    def handle(self, *args, **options):
        for code, desc in codes:
            mc, created = MeasureCode.objects.get_or_create(
                code=code, description=desc)
            if created:
                print 'created %s %s' % (code, desc)
            else:
                print 'ignored existing %s %s' % (code, desc)
