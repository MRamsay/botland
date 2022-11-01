from django.core.management.base import BaseCommand

from pprint import pprint
from astroquery.esa.jwst import Jwst


class Command(BaseCommand):

    def handle(self, *args, **options):

        query = """select o.observationid, a.artifactid, a.filename

from jwst.observation o join jwst.artifact a on a.obsid = o.obsid

where o.proposal_id = '01166' and o.intent = 'science'"""

        # query = """select o.observationid, o.proposal_id from jwst.observation o where o. order by o.proposal_id"""
        query = """select o.observationid, a.*
        from 
            jwst.observation o 
            join jwst.artifact a on a.obsid = o.obsid 
        where 
            (
                a.filename like 'miri%fits' or
                a.filename like 'nirc%fits'
            ) and
            o.proposal_id in (
                select top 1 p.proposal_id 
                from jwst.observation p 
                    join jwst.artifact b on p.obsid = b.obsid 
                where (
                    b.filename like 'miri%cal%fits' or
                    b.filename like 'nirca%cal%fits'
                ) 
                order by p.proposal_id 
            ) 
        """

        query = """select distinct o.proposal_id, o.proposal_title, o.proposal_pi
        from 
            jwst.observation o where o.proposal_pi <> '' and o.proposal_title <> '' and o.proposal_pi <> 'UNKNOWN' and o.proposal_title <> 'UNKNOWN'
        """

        job = Jwst.launch_job(query, async_job=True)
        print(job.get_results())
        #
