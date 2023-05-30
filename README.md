# CAP
Company Analytics with Python (SermanLTD on MoiSklad)

This project is for analytics automation in SermanLTD Company
It includes Telegram bot and Django website to maximize data represent. 

This project is for build functional analytics from any ARM, because it has own SQL database that updating with data from ARM
For example: MoiSklad have some restrictions for number of parallel requests and cant be used as a base for multiple requests. We need to provide transitional Database. 
In this case I build my program in that way: MoiSklad -> SQL -> Django -> WWW + Telegram


1. Main - main module 
2. API_MS - module for work with API MoiSklad https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api
3. API_Tbot - module for work with API Telegram https://core.telegram.org
4. API_GS - module for work with API GoogleSheet https://developers.google.com/sheets/api/guides/concepts
5. Django - module for service website on Django https://www.djangoproject.com
6. Pgsql - module for synchronizing MS -> Postgresql 
7. SQLAlchemy - module for sql requests from my Project 
8. SocService - module for messaging inside project and send messages to Telegram from any module 
9. API_Docker - module for automatically creation Pgsql base in docker image


