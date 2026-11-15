# NCBI Data Access and Provenance

- Use NCBI E-utilities and documented interfaces rather than scraping web pages.
- Configure a contact email using NCBI_EMAIL.
- Optionally configure NCBI_API_KEY as an environment variable; never commit it.
- Respect NCBI rate limits, usage policies, and service availability.
- Cache repeated requests in a future release to reduce unnecessary traffic.
- Store database name, accession/version, retrieval timestamp, and record format with each result.
- Cite the original NCBI record in reports.
- Database annotation is not necessarily experimentally confirmed for every context.
- This application is not intended for clinical diagnosis, treatment selection, or personal medical interpretation.

Useful documentation:
- https://www.ncbi.nlm.nih.gov/books/NBK25501/
- https://www.ncbi.nlm.nih.gov/datasets/docs/
- https://blast.ncbi.nlm.nih.gov/doc/blast-help/
